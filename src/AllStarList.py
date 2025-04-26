import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches   # for legend handles
import requests
from bs4 import BeautifulSoup
from Player import *
from util import *
import time

class AllStarList:
    def __init__(self, start_year, end_year):
        self.__star_list = {}
        self.__all_star = {}
        self.__name_id = {}
        self.__user_add = []
        self.__update_req = {}
        search_range = range(start_year, end_year+1)
        for year in search_range:
            self._getAllStars(year)
        
        for player, player_obj in self.__star_list.items():
            player_teammmates = player_obj.getAllTeammates()
            for url_id, info in player_teammmates.items():
                if url_id in self.__star_list.keys():
                    teammate_info = info
                    teammate_info["object"] = self.__star_list[url_id]
                    player_obj.updateTeammate(url_id, teammate_info)
            player_obj.cleanTeammates()


    def _getAllStars(self, year):

        url = f"https://www.basketball-reference.com/allstar/NBA_{year}.html"
        print("")
        print(f"========================================")
        print(f"    Get All-Star List in {year-1} - {year}  ")
        print(f"========================================")
        print("")

        allstar_tmp_file = f"SaveData/AllStars/AllStar_{year}.json" 
        all_star_dict = {}

        if os.path.exists(allstar_tmp_file):
            with open(allstar_tmp_file, 'r') as f:
                all_star_dict = json.load(f)
            
            self.__all_star[year] = []
            for player_name, player_url in all_star_dict.items():
                self.__all_star[year].append(player_name)
                if player_name.lower() not in self.__name_id.keys():
                    new_player = Player(player_name, player_url)
                    player_url_id = new_player.getPlayerUrlID()
                    self.__star_list[player_url_id] = new_player
                    self.__name_id[player_name.lower()] = player_url_id
                    self.__update_req[player_name.lower()] = False
        
        else:
            # Send request to the All-Star game page on Basketball Reference
            response = None
            while response is None:
                response = requests.get(url)
                time.sleep(5.0)
            soup = BeautifulSoup(response.content, 'html.parser')
            self.__all_star[year] = []
            # Locate the table or section containing the players' names and URLs
            # This part may require adjustment depending on the actual structure of the page
            # Finding the all star player on the website
            for link in soup.find_all('a', href=True):
                if '/players/' in link['href'] and (link.get("title") == None):
                    # Extract the player name and profile URL
                    player_name = link.text
                    if player_name == "Players" or player_name == "...":
                        continue
                    self.__all_star[year].append(player_name)
                    all_star_dict[player_name] = f"https://www.basketball-reference.com{link['href']}"
                    if player_name.lower() not in self.__name_id.keys():
                        player_url = f"https://www.basketball-reference.com{link['href']}"
                        new_player = Player(player_name, player_url)
                        player_url_id = new_player.getPlayerUrlID()
                        self.__star_list[player_url_id] = new_player
                        self.__name_id[player_name.lower()] = player_url_id
                        self.__update_req[player_name.lower()] = False

            with open(allstar_tmp_file, 'w') as f:
                json.dump(all_star_dict, f)

    def CheckInList(self, player_name):
        """
        Check if the player is already recorded in the list.

        Parameters
        ----------
        player_name : str
            The name of the player to be checked.

        Returns
        -------
        bool
            Return True if the player exists in the list; otherwise,
            return False.
        """
        
        if player_name.lower() in self.__name_id.keys():
            return True
        else:
            return False
    
    def FindPlayerObj(self, player_name):
        """
        Extract the player object by the given player name.

        Parameters
        ----------
        player_name : str
            The name of the player.

        Returns
        -------
        Player | None
            Return the corresponding class:Player object when the name
            is found. Otherwise, return None.
        """

        in_list = self.CheckInList(player_name)
        if not in_list:
            print(f"Error! Player ({player_name}) is not in the list!")
            return None
        player_id = self.__name_id[player_name.lower()]
        player_obj = self.__star_list[player_id]
        return player_obj
        
    def addPlayerToList(self, new_player_name):
        """
        Add a single NBA player to the internal All‑Star graph, updating 
        the corresponding structures and bidirectional teammate links.

        Parameters
        ----------
        new_player_name : str
            The player name to be added by user.

        Returns
        -------
        bool
            Return True if the player is sucessfully added or already in 
            the list.
            Return False if the player name could not be resolved after 
            searching at Baseketball Reference.
        """

        if new_player_name.lower() in self.__name_id.keys():
            print("The player is already in the list!")
            return True
        new_player_url = FindUrlByName(new_player_name)
        if new_player_url == "FAILURE":
            print("The player can't be found!")
            return False
        
        new_player = Player(new_player_name.title(), new_player_url)
        new_player_url_id = new_player.getPlayerUrlID()
        self.__star_list[new_player_url_id] = new_player
        self.__name_id[new_player_name.lower()] = new_player_url_id
        self.__user_add.append(new_player_url_id)
        new_teammate = new_player.getAllTeammates()
        for player_id, info in new_teammate.items():
            if player_id in self.__star_list.keys():
                new_p_info = info
                new_p_info["object"] = new_player
                exist_p_info = info
                exist_p_info["name"] = new_player_name.title()
                exist_p_info["object"] = self.__star_list[player_id]
                self.__star_list[player_id].updateTeammate(new_player_url_id, new_p_info)
                self.__star_list[new_player_url_id].updateTeammate(player_id, exist_p_info)
        new_player.cleanTeammates()

        for exist_p in self.__update_req.keys():
            self.__update_req[exist_p] = True
        self.__update_req[new_player_name.lower()] = False

        return True

    def findMinDegree(self, player_1, player_2):
        '''
        Breadth‑first search for the shortest “teammate chain” that connects
        two NBA players in the current All‑Star graph.

        Parameters
        ----------
        player_1 : str
            Name of the starting player.
        player_2 : str
            Name of the target player.

        Returns
        -------
        tuple: (success, result)
            -- success (bool): return True if both players
            -- result (list): [num_degree, connect_path]
                --- num degree (int): the number of the degree from play 1
                to player 2. If theres's no path between these two players, 
                then return -1.
                --- connect_path (list): the shortest path from player 1 to
                player 2. If theres's no path between these two players, then
                return empty list.
        '''

        # Convert names to URL ids
        player_1 = player_1.lower()
        player_2 = player_2.lower()
        result = [-1, []]
        if player_1 not in self.__name_id or player_2 not in self.__name_id:
            print("One or both players not found in the list.")
            return False, result

        start_player = self.__name_id[player_1]
        end_player = self.__name_id[player_2]
        start_p_name = self.__star_list[start_player].getPlayerName()
        end_p_name = self.__star_list[end_player].getPlayerName()

        if start_player == end_player:
            result = [0, [start_p_name]]
            printConnectPath(start_p_name, end_p_name, result)
            return True, result


        queue   = [start_player]
        visited = set([start_player])
        visit_idx = 0
        prev_info = {}
        while visit_idx < len(queue):
            visit_player = queue[visit_idx]
            visit_idx += 1
            if visit_player == end_player:
                current_player = visit_player
                connect_path = [self.__star_list[visit_player].getPlayerName()]
                while current_player != start_player:
                    prev_player = prev_info[current_player]
                    connect_path.append(self.__star_list[prev_player].getPlayerName())
                    current_player = prev_player
                path_length = len(connect_path) - 1
                connect_path.reverse()
                result = [path_length, connect_path]
                break
            
            visit_teammate = self.__star_list[visit_player].getAllTeammates()
            for player_id in visit_teammate.keys():
                if player_id not in visited:
                    visited.add(player_id)
                    prev_info[player_id] = visit_player
                    queue.append(player_id)

        printConnectPath(start_p_name, end_p_name, result)
        print("Do you want to show path in the teammate connection figure? (yes/no)")
        affirm_resp = ['y', 'ye', 'yes']
        neg_resp = ['n', 'no']
        yn_resp = False
        while yn_resp is False:
            print(">> ", end="")
            orig_user_resp = input()
            user_resp = orig_user_resp.strip().lower()

            if user_resp in affirm_resp:
                self.printConnectFig(True, result[1])
                yn_resp = True
            elif user_resp in neg_resp:
                yn_resp = True
            else:
                print("Please enter yes/no.")
                yn_resp = False

        return True

    def findMaxEdge(self, topk):
        """
        Find and display the top-k players with the highest number of 
        teammate connections in the internal All-Star list.

        Parameters
        ----------
        topk : int
            The number of top connected players to display.

        Returns
        -------
        bool
            Always returns True
        """

        max_edge = []
        for player, player_obj in self.__star_list.items():
            player_name = player_obj.getPlayerName()
            max_edge.append([player_name, player_obj.getNumTeammate()])
        sorted_edge_list = sorted(max_edge, key=lambda x: x[1], reverse=True)

        print("")
        print(f"============ Top-{topk} Most Connected Players ============")
        print(f"Player: Number of Connection")
        for edge_info in sorted_edge_list[:topk]:
            print(f"{edge_info[0]}: {edge_info[1]}")
        print(f"======================================================")
        print("")
        return True

    def findPlayerBestDuo(self, player_name, topk):
        """
        Display the top-k best performing teammates (duos) for a given 
        player by user.

        Parameters
        ----------
        player_name : str
            The name of the given player whose best duos are to be searched.
        topk : int
            The number of top duos to return.

        Returns
        -------
        bool
            Return True if the player is in the list; 
            otherwise, return False.
        """

        best_duo = None
        player_obj = self.FindPlayerObj(player_name)
        if player_obj is None:
            return False 
        update_req = self.__update_req[player_name.lower()]
        best_duo = player_obj.findBestDuo(topk, update_req)
        self.__update_req[player_name.lower()] = False
        
        p_name = player_obj.getPlayerName()
        print("")
        if len(best_duo) == 0:
            print(f"{p_name} hasn't played with other players in the list on the court!")
            print("")
            return True
        print(f"============ Top-{topk} Best Teammates for {p_name} ============")
        rank = 1
        for duo_id, duo_info in best_duo.items():
            print(f"Rank {rank}: {self.__star_list[duo_id].getPlayerName()}")
            printDuoInfo(duo_info)
            rank += 1
        
        return True
    
    def compareTwoDuo(self, duo1, duo2):
        """
        Compare two NBA player duos by looking into the average of points 
        minus opponent points per 100 possession weighted by the time playing
        on the courts.

        Parameters
        ----------
        duo1, duo2 : list of str
            The list contains of two player names of the duo

        Returns
        -------
        bool
            Return True if all the players in both duos are found and compared.
            Return False if any player name in the input couldn't be resolved.
        """

        player_0 = self.FindPlayerObj(duo1[0])
        player_1 = self.FindPlayerObj(duo1[1])
        player_2 = self.FindPlayerObj(duo2[0])
        player_3 = self.FindPlayerObj(duo2[1])
        if player_0 is None or player_1 is None \
        or player_2 is None or player_3 is None:
            return False
        
        p0_name = player_0.getPlayerName()
        p1_name = player_1.getPlayerName()
        p2_name = player_2.getPlayerName()
        p3_name = player_3.getPlayerName()

        duo_1_teammate = self.__name_id[duo1[1].lower()]
        duo_1_update = self.__update_req[duo1[0].lower()]
        duo_2_teammate = self.__name_id[duo2[1].lower()]
        duo_2_update = self.__update_req[duo2[0].lower()]
        duo_1_info = player_0.getDuoInfo(duo_1_teammate, duo_1_update)
        time.sleep(1.0)
        duo_2_info = player_2.getDuoInfo(duo_2_teammate, duo_2_update)
        d1_total_time = 0
        d1_total_pt = 0
        for mp, pts in zip(duo_1_info["MP"], duo_1_info["PTS"]):
            play_time = mp[0] * 60 + mp[1]
            weight_pt = play_time * pts
            d1_total_time += play_time
            d1_total_pt += weight_pt
        d1_avg_weight_pt = d1_total_pt / d1_total_time

        print(f"Informtation of Duo 1 ({p0_name}, {p1_name})")
        printDuoInfo(duo_1_info)

        d2_total_time = 0
        d2_total_pt = 0
        for mp, pts in zip(duo_2_info["MP"], duo_2_info["PTS"]):
            play_time = mp[0] * 60 + mp[1]
            weight_pt = play_time * pts
            d2_total_time += play_time
            d2_total_pt += weight_pt
        d2_avg_weight_pt = d2_total_pt / d2_total_time

        print(f"Informtation of Duo 2 ({p2_name}, {p3_name})")
        printDuoInfo(duo_2_info)

        print("---- Comparison Result ----")
        if d1_avg_weight_pt >= d2_avg_weight_pt:
            print("-> Duo 1 has better efficiency than Duo 2.")
        else:
            print("-> Duo 2 has better efficiency than Duo 1.")
        
        print("")
        return True


    def getPlayerStat(self, player_name, year):
        player_obj = self.FindPlayerObj(player_name)
        if player_obj is None:
            return False
        succ = player_obj.displayStatsByYear(year)
        return succ
    
    def printAllStarRoster(self, year):

        if year not in self.__all_star.keys():
            print(f"Year {year} is not recorded!")
            return False
        player_list = self.__all_star[year]
        print("")
        line_pat = 20 * "="
        print(line_pat, end="")
        print(f" Players in the {year-1}-{year} All-Star Roster ", end="")
        print(line_pat)
        printPlayerList(player_list)
        print("")
        print("")
        line_pat = 84 * "="
        print(line_pat)
        return True

    def printAllPlayer(self):
        player_list = [obj.getPlayerName() for key, obj in self.__star_list.items()]
        print("")
        line_pat = 20 * "="
        line_pat = line_pat + " Players in the List (in Alphabetical Order) " + line_pat
        print(line_pat)
        printPlayerList(player_list)
        print("")
        print("")
        line_pat = 85 * "="
        print(line_pat)
        
        print(f"Total Number of Players: {len(player_list)}")
        print("")
        return True

    def printConnectFig(self, showFig, PlayerConnect=None):
        saveFig = False
        FileName = None
        ConnectEdge = []
        ConnectNode = []
        if PlayerConnect is not None:
            for p_idx in range(len(PlayerConnect)-1):
                p1 = PlayerConnect[p_idx]
                p2 = PlayerConnect[p_idx+1]
                p1_id = self.__name_id[p1.lower()]
                p2_id = self.__name_id[p2.lower()]
                ConnectEdge.append((p1_id, p2_id))
                ConnectEdge.append((p2_id, p1_id))
                ConnectNode.append(p1_id)
            ConnectNode.append(self.__name_id[PlayerConnect[-1].lower()])
        else:
            ConnectNode = []

        # Get all edges first
        edges = []
        for player, player_obj in self.__star_list.items():
            teammmates_list = player_obj.getAllTeammates().keys()
            for teammate in teammmates_list:
                if (player, teammate) not in edges and (teammate, player) not in edges:
                    edges.append((player, teammate))
        
        # Nodes and its corresponding position
        nodes = list(self.__star_list.keys())
        loc_angle = np.linspace(0, 2*np.pi, len(nodes)+1)[:-1]
        loc_pos = {}
        rad = 6.5
        for n_idx in range(len(nodes)):
            loc_pos[nodes[n_idx]] = (rad*np.cos(loc_angle[n_idx]), rad*np.sin(loc_angle[n_idx]))

        # Start plotting the figure
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.axis('off')
        color_map = ['tab:blue', 'tab:orange', 'tab:red']
        
        # Plot edges
        for (p1, p2) in edges:
            if (p1, p2) in ConnectEdge:
                ecolor = color_map[2]
                ax.plot([loc_pos[p1][0], loc_pos[p2][0]], [loc_pos[p1][1], loc_pos[p2][1]],
                    linewidth=1.8, zorder=4, color=ecolor)
            else:
                '''
                if p1 in self.__user_add or p2 in self.__user_add:
                    ecolor = color_map[1]
                else:
                    ecolor = color_map[0]
                '''
                ecolor = color_map[0]
                ax.plot([loc_pos[p1][0], loc_pos[p2][0]], [loc_pos[p1][1], loc_pos[p2][1]],
                        linewidth=1.0, color=ecolor)
        
        # Plot nodes
        for node in nodes:
            if node in ConnectNode:
                ncolor = color_map[2]
            else:
                '''
                if node in self.__user_add:
                    ncolor = color_map[1]
                else:
                    ncolor = color_map[0]
                '''
                ncolor = color_map[0]

            ax.scatter(loc_pos[node][0], loc_pos[node][1],
                    s=500, zorder=3, c=ncolor, edgecolors='k')
            
            pname = self.__star_list[node].getPlayerName().replace(" ", "\n")
            ax.text(*loc_pos[node], pname, ha='center', va='center',
                    color='white', weight='bold', zorder=4, fontsize=5)
        if showFig:
            plt.show()

        print("Do you want to save the figure?")
        affirm_resp = ['y', 'ye', 'yes']
        neg_resp = ['n', 'no']
        yn_resp = False
        while yn_resp is False:
            print(">> ", end="")
            orig_user_resp = input()
            user_resp = orig_user_resp.strip().lower()

            if user_resp in affirm_resp:
                saveFig = True
                yn_resp = True
            elif user_resp in neg_resp:
                yn_resp = True
            else:
                print("Please enter yes/no.")
                yn_resp = False
        # Save figure
        if saveFig:
            print("Filename (.png) of the figure: ", end="")
            orig_user_resp = input()
            user_resp = orig_user_resp.strip()
            FileName = "SaveData/Figures/" + user_resp + ".png"
            fig.savefig(FileName, dpi=300, bbox_inches="tight")
            print(f"Figure saved as {FileName}")
