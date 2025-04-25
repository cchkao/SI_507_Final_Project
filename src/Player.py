import requests
from bs4 import BeautifulSoup, Comment
from Statistics import *
from util import *
import time
import json
import os

class Player:
    '''an all star player in 2000-2024
    
    Class Attributes
    ----------------
    headers: dict
        Header for the url request

    Instance Attributes
    -------------------
    url: str
        the website of the player on basketball reference

    name: str
        the name of the player
    
    award: dict
        award player won before

    __stats: class Statistics
        different statistics the players every year
    
    __teammates: dict
        - key: player url id
        - value: dict of information
            -- key  : name
            -- value: player name
            -- key  : object
            -- value: player object
    
    __tm_detail: dict
        the detail (stats) of the teammates
        - key: player url id
        - value: dict of information
            -- key  : year
            -- value: list of year
            -- key  : team
            -- value: list of team
            -- key  : MP
            -- value: list of MP
            -- key  : PTS (Net PER 100)
            -- value: list of PTS
            
    '''
    headers = {'User-Agent': 'Mozilla/5.0'}
    def __init__(self, player_name, player_url):
        print(f"Add Player: {player_name}")
        self.name = player_name
        self.url = player_url

        self.url_id = player_url.split('/')[-1][:-5]
        self.__stats = None
        self.__teammates = {}
        self.__tm_detail = {}
        self.teammate_tmp_file = "SaveData/Teammates/" + self.url_id + "_teammates.json"        
        self.__fetchTeammates()

    def __fetchStats(self):
        self.__stats = Statistics(self.url, self.name)

    def __fetchTeammates(self):
        if os.path.exists(self.teammate_tmp_file):
            with open(self.teammate_tmp_file, 'r') as f:
                self.__teammates = json.load(f)
        else:
            teammate_url = "https://www.basketball-reference.com/friv/teammates_and_opponents.fcgi?pid=" \
                        + str(self.url_id) + "&type=t"
            print(f"Fetch teammate data from website ...")
            response = None
            while response is None:
                response = requests.get(teammate_url, headers=Player.headers)
                time.sleep(4.5)

            soup = BeautifulSoup(response.text, "html.parser")

            table = soup.find("table", {"id": "teammates-and-opponents"})
            rows = table.find("tbody").find_all("tr")

            for row in rows:
                if row.get("class") == ["thead"]:
                    continue

                name_cell = row.find("td", {"data-stat": "pid2"})
                if name_cell is None or not name_cell.find("a"):
                    continue

                name = name_cell.text.strip()
                if name[-1] == '*':
                    name = name[:-1]
                href = name_cell.find("a")["href"]
                player_id = href.split("/")[-1][:-5]

                self.__teammates[player_id] = {}
                self.__teammates[player_id]["name"] = name
                self.__teammates[player_id]["object"] = None
            
            
            with open(self.teammate_tmp_file, 'w') as f:
                json.dump(self.__teammates, f)

    def findBestDuo(self, topk, update_req):
        self.__fetchTeammatesDetail(update_req)
        duo_eff = []
        for teammate_id, duo_info in self.__tm_detail.items():
            total_time = 0
            total_pt = 0
            for mp, pts in zip(duo_info["MP"], duo_info["PTS"]):
                play_time = mp[0] * 60 + mp[1]
                weight_pt = play_time * pts
                total_time += play_time
                total_pt += weight_pt
            avg_weight_pt = total_pt / total_time
            duo_eff.append([teammate_id, avg_weight_pt])
        
        sorted_duo_eff = sorted(duo_eff, key=lambda x: x[1], reverse=True)
        sorted_tm_id = [tm_data[0] for tm_data in sorted_duo_eff]
        topk = min(topk, len(sorted_tm_id))
        best_duo_info = {tm_id: self.__tm_detail[tm_id] for tm_id in sorted_tm_id[:topk]}
        return best_duo_info
    
    def getDuoInfo(self, teammate_id, update_req):
        self.__fetchTeammatesDetail(update_req)
        return self.__tm_detail.get(teammate_id)

    def __fetchTeammatesDetail(self, update_req):
        if self.__stats is None:
            self.__fetchStats()

        if update_req or (self.__tm_detail == {}):
            print("")
            print(f"Start fetching teammates data details for player {self.name} ...")
            play_years = self.__stats.getYear()
            self.__tm_detail = {}
            for year in play_years:
                self.__fetchTeammatesDetailYear(year)
            print(f"------- End fetching teammates data details ------")
            print("")

    def __fetchTeammatesDetailYear(self, year):
        lineup_url = self.url[:-5] + "/lineups/" + str(year)
        print(f"Check Teammate from Lineups, Year: {year-1}-{year}")
        response = None
        while response is None:
            response = requests.get(lineup_url, headers=Player.headers)
            time.sleep(5.0)
        soup = BeautifulSoup(response.text, 'html.parser')

        comments = soup.find_all(string=lambda text: isinstance(text, Comment))

        for comment in comments:
            if 'id="lineups-2-man"' in comment:
                comment_soup = BeautifulSoup(comment, 'html.parser')
                table = comment_soup.find('table', {'id': 'lineups-2-man'})
                rows = table.find('tbody').find_all('tr')

                for row in rows:
                    if row.get('class') == ['thead']:
                        continue  # skip subheaders

                    lineup_cell = row.find('td', {'data-stat': 'lineup'})
                    links = lineup_cell.find_all('a')

                    # Find the player that is not the visited one
                    for a in links:
                        if self.url_id not in a['href']:
                            teammate = a['href'].split('/')[-1][:-5]
                            break
                    
                    team = row.find('td', {'data-stat': 'team_id'}).text.strip()
                    str_mp = row.find('td', {'data-stat': 'mp'}).text.strip()
                    str_pts = row.find('td', {'data-stat': 'diff_pts'}).text.strip()
                    if teammate in self.__teammates.keys():
                        if teammate not in self.__tm_detail.keys():
                            self.__tm_detail[teammate] = {}
                            self.__tm_detail[teammate] = {}
                            self.__tm_detail[teammate]["year"] = []
                            self.__tm_detail[teammate]["team"] = []
                            self.__tm_detail[teammate]["MP"] = []
                            self.__tm_detail[teammate]["PTS"] = []

                        self.__tm_detail[teammate]["year"].append(year)
                        self.__tm_detail[teammate]["team"].append(team)
                        try:
                            split_mp = str_mp.split(":")
                            mp = [int(split_mp[0]), int(split_mp[1])]
                        except:
                            mp = 0
                            
                        self.__tm_detail[teammate]["MP"].append(mp)
                        try:
                            neg = (str_pts[0] == "-")
                            pts = float(str_pts[1:])
                            if neg:
                                pts = -pts
                        except:
                            pts = 0
                        self.__tm_detail[teammate]["PTS"].append(pts)
                break
    
    def updateTeammate(self, update_player_id, update_player_info):
        self.__teammates[update_player_id] = update_player_info

    def cleanTeammates(self):
        cleaned_teammates = {key: value for key, value in self.__teammates.items() if (value["object"] is not None)}
        self.__teammates = cleaned_teammates
    
    def getPlayerName(self):
        return self.name
    
    def getPlayerUrl(self):
        return self.url
    
    def getPlayerUrlID(self):
        return self.url_id
    
    def getAllTeammates(self):
        return self.__teammates
    
    def getTeammateInfo(self, player_url_id):
        return self.__teammates[player_url_id]
    
    def getNumTeammate(self):
        return len(self.__teammates)

    def getStatsByType(self, year) -> dict:
        if self.__stats is None:
            self.__fetchStats()
        return self.__stats.getStatsByType(year)
    
    def getStatsByYear(self, year) -> dict:
        if self.__stats is None:
            self.__fetchStats()
        return self.__stats.getStatsByYear(year)

    def displayStatsByYear(self, year):
        player_stat = self.getStatsByYear(year)
        if player_stat is None:
            return False
        print("")
        print(f"====================================================================================")
        print("")
        print(f"Player Name: {self.name}, Year: {year} (Season: {year-1}-{year})")
        if player_stat == "Did not play":
            print("-------------------")
            print("   Did not play")
            print("-------------------")
            return True
        p_col_per_row = 12
        PrintStatsTable(player_stat, p_col_per_row)
        print("")
        print(f"====================================================================================")
        print("")
        return True

        '''
        # Not formatted print
        for key, value in player_stat.items():
            print(f"{key}: {value}")
        '''

    def getSpecificStatsByYear(self, stat_type, year):
        return self.__stats.getSpecificStatsByYear(stat_type, year)

