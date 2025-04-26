from AllStarList import *
import os

class UserInterface:
    def __init__(self, start_year, end_year):
        print("")
        print("------- Welcome to use the NBA All-Star Network Analyzer -------")
        print("")
        print("Create Folders for Data Saving...")
        folder_path = "SaveData"
        os.makedirs(folder_path, exist_ok=True)
        folder_path = "SaveData/AllStars"
        os.makedirs(folder_path, exist_ok=True)
        folder_path = "SaveData/Figures"
        os.makedirs(folder_path, exist_ok=True)
        folder_path = "SaveData/Statistics"
        os.makedirs(folder_path, exist_ok=True)
        folder_path = "SaveData/Teammates"
        os.makedirs(folder_path, exist_ok=True)
        print("")
        print("Start Initialization for the Fetching Data...")
        self.All_Star = AllStarList(start_year, end_year)
        print("")
        print("Finish Initialization for the Fetching Data...")
        print("")
        self.userAction()
    
    def userAction(self):
        
        is_exit = False
        cmd_succ = True
        while is_exit == False:
            if cmd_succ:
                print("Please enter your command (enter \"help\" if you want to see the command list).")
            print(">> ", end="")
            orig_user_resp = input()
            user_resp = orig_user_resp.strip().lower()
            if self.__isExit(user_resp):
                break

            elif self.__isHelp(user_resp):
                self.cmdHelper()
                cmd_succ = False

            elif user_resp == "add_player":
                is_exit = self.addPlayer()
                cmd_succ = True

            elif user_resp == "best_duo":
                is_exit = self.bestDuo()
                cmd_succ = True

            elif user_resp == "comp_duo":
                is_exit = self.compDuo()
                cmd_succ = True

            elif user_resp == "disp_all":
                self.All_Star.printAllPlayer()
                cmd_succ = True
            
            elif user_resp == "disp_star":
                self.dispStar()
                cmd_succ = True

            elif user_resp == "disp_stat":
                self.dispStat()
                cmd_succ = True

            elif user_resp == "plot_fig":
                self.All_Star.printConnectFig(True, PlayerConnect=None)
                cmd_succ = True

            elif user_resp == "find_min_deg":
                self.findMinDeg()
                cmd_succ = True
            
            elif user_resp == "max_connect":
                self.findMaxEdge()

            else:
                print("Command not found! Please check command list by \"help\".")
                cmd_succ = False
        
        print("")
        print("Exit the program... TAHNK YOU!")
        print("")

    def cmdHelper(self):
        print("")
        print("========================== Command List ==========================")
        print("-- add_player")
        print("   Add a new player in the list for network analyzer.")
        print("-- best_duo")
        print("   Find the best teammates for a specific player in the list.")
        print("-- comp_duo")
        print("   Compare two duos for the specific players in the list.")
        print("-- disp_all")
        print("   Display all players in the list.")
        print("-- disp_star")
        print("   Display the all-star roster in the specific year.")
        print("-- disp_stat")
        print("   Display the statistic of the specific player in the specific year.")
        print("-- find_min_deg")
        print("   Find the minimum degree of teammate connection between two players.")
        print("-- max_connect")
        print("   Find the players with maximum teammate connection in the list.")
        print("-- plot_fig")
        print("   Draw the figure of the teammate relationship between players in the list.")
        print("-- help")
        print("   Show the available command.")
        print("-- exit")
        print("   Exit the program.")
        print("==================================================================")
        print("")
        pass

    def __isExit(self, user_resp):
        return user_resp == "exit"

    def __isBack(self, user_resp):
        return user_resp == "back"
    
    def __isHelp(self, user_resp):
        return user_resp == "help"

    
    def addPlayer(self):
        
        cmd_succ = False
        is_exit = False
        print("")
        while cmd_succ is False:
            print("Please enter the player name: ", end="")
            orig_user_resp = input()
            user_resp = orig_user_resp.strip().lower()
            if self.__isExit(user_resp):
                is_exit = True
                break
            elif self.__isBack(user_resp):
                break

            cmd_succ = self.All_Star.addPlayerToList(user_resp)
        
        return is_exit
    
    def bestDuo(self):
        cmd_succ = False
        is_back = False
        is_exit = False
        topk = 1
        print("")
        print("(Enter \"help\" to view all players in the list.)")
        while cmd_succ is False:
            print("Please enter the player name: ", end="")
            orig_user_resp = input()
            user_resp = orig_user_resp.strip().lower()
            if self.__isExit(user_resp):
                is_exit = True
                break
            elif self.__isBack(user_resp):
                is_back = True
                break
            elif self.__isHelp(user_resp):
                self.All_Star.printAllPlayer()
            elif self.All_Star.CheckInList(user_resp):
                num_valid = False
                player_name = user_resp
                while num_valid is False:
                    print("Enter the number of top teammates to display: ", end="")
                    orig_user_resp = input()
                    user_resp = orig_user_resp.strip().lower()
                    if self.__isExit(user_resp):
                        is_exit = True
                        break
                    elif self.__isBack(user_resp):
                        is_back = True
                        break
                    else:
                        if user_resp.isdigit():
                            topk = int(user_resp)
                            num_valid = True
                            cmd_succ = self.All_Star.findPlayerBestDuo(player_name, topk)
                        else:
                            print("Invalid Number!!")
                if is_back or is_exit:
                    break
            else:
                print(f"Player {user_resp} is not in the list!")
        
        return is_exit
    
    def compDuo(self):
        d_idx = 1
        p_idx = 1
        cmd_succ = False
        p_succ = False
        is_back = False
        is_exit = False
        player_0 = ""
        player_1 = ""
        player_2 = ""
        player_3 = ""
        print("")
        print("(Enter \"help\" to view all players in the list.)")
        while cmd_succ is False:
            while p_succ is False:
                print(f"Please enter the player {p_idx} for duo {d_idx}: ", end="")
                orig_user_resp = input()
                user_resp = orig_user_resp.strip().lower()
                if self.__isExit(user_resp):
                    is_exit = True
                    break
                elif self.__isBack(user_resp):
                    is_back = True
                    break
                elif self.__isHelp(user_resp):
                    self.All_Star.printAllPlayer()
                elif self.All_Star.CheckInList(user_resp):
                    if(p_idx == 1) and (d_idx == 1):
                        p_idx = 2
                        player_0 = user_resp
                    elif(p_idx == 2) and (d_idx == 1):
                        p_idx = 1
                        d_idx = 2
                        player_1 = user_resp
                    elif(p_idx == 1) and (d_idx == 2):
                        p_idx = 2
                        d_idx = 2
                        player_2 = user_resp
                    elif(p_idx == 2) and (d_idx == 2):
                        p_idx = 1
                        d_idx = 1
                        player_3 = user_resp
                        p_succ = True
                else:
                    print(f"Player {user_resp} is not in the list!")
            if is_back or is_exit:
                break
            duo1 = [player_0, player_1]
            duo2 = [player_2, player_3]
            cmd_succ = self.All_Star.compareTwoDuo(duo1, duo2)
        
        return is_exit
    
    def dispStar(self):
        cmd_succ = False
        is_back = False
        is_exit = False
        print("Enter the year of all-star roster to be displayed: ", end="")
        while cmd_succ is False:
            orig_user_resp = input()
            user_resp = orig_user_resp.strip().lower()
            if self.__isExit(user_resp):
                is_exit = True
                break
            elif self.__isBack(user_resp):
                is_back = True
                break
            else:
                if user_resp.isdigit():
                    year = int(user_resp)
                    cmd_succ = self.All_Star.printAllStarRoster(year)
                else:
                    print("Invalid Number!!")
            if is_back or is_exit:
                break
        
        return is_exit
    
    def dispStat(self):
        cmd_succ = False
        is_back = False
        is_exit = False
        year = 0
        print("")
        print("(Enter \"help\" to view all players in the list.)")
        while cmd_succ is False:
            print("Please enter the player name: ", end="")
            orig_user_resp = input()
            user_resp = orig_user_resp.strip().lower()
            if self.__isExit(user_resp):
                is_exit = True
                break
            elif self.__isBack(user_resp):
                is_back = True
                break
            elif self.__isHelp(user_resp):
                self.All_Star.printAllPlayer()
            elif self.All_Star.CheckInList(user_resp):
                num_valid = False
                player_name = user_resp
                while num_valid is False:
                    print("Enter the year: ", end="")
                    orig_user_resp = input()
                    user_resp = orig_user_resp.strip().lower()
                    if self.__isExit(user_resp):
                        is_exit = True
                        break
                    elif self.__isBack(user_resp):
                        is_back = True
                        break
                    else:
                        if user_resp.isdigit():
                            year = int(user_resp)
                            num_valid = True
                            cmd_succ = self.All_Star.getPlayerStat(player_name, year)
                        else:
                            print("Invalid Number!!")
                if is_back or is_exit:
                    break
            else:
                print(f"Player {user_resp} is not in the list!")
        
        return is_exit

    def findMinDeg(self):
        p_idx = 1
        cmd_succ = False
        p_succ = False
        is_back = False
        is_exit = False
        player_0 = ""
        player_1 = ""
        print("")
        print("(Enter \"help\" to view all players in the list.)")
        while cmd_succ is False:
            while p_succ is False:
                print(f"Please enter the player {p_idx}: ", end="")
                orig_user_resp = input()
                user_resp = orig_user_resp.strip().lower()
                if self.__isExit(user_resp):
                    is_exit = True
                    break
                elif self.__isBack(user_resp):
                    is_back = True
                    break
                elif self.__isHelp(user_resp):
                    self.All_Star.printAllPlayer()
                elif self.All_Star.CheckInList(user_resp):
                    if(p_idx == 1):
                        p_idx = 2
                        player_0 = user_resp
                    elif(p_idx == 2):
                        p_idx = 1
                        d_idx = 2
                        player_1 = user_resp
                        p_succ = True
                else:
                    print(f"Player {user_resp} is not in the list!")
            if is_back or is_exit:
                break
            cmd_succ = self.All_Star.findMinDegree(player_0, player_1)
        
        return is_exit
    
    def findMaxEdge(self):
        cmd_succ = False
        is_back = False
        is_exit = False
        num_edge = 1
        print("")
        while cmd_succ is False:
            print("Enter the number of top teammates to display: ", end="")
            orig_user_resp = input()
            user_resp = orig_user_resp.strip().lower()
            if self.__isExit(user_resp):
                is_exit = True
                break
            elif self.__isBack(user_resp):
                is_back = True
                break
            elif user_resp.isdigit():
                num_edge = int(user_resp)
                cmd_succ = self.All_Star.findMaxEdge(num_edge)
            else:
                print("Invalid Number!!")
        
        return is_exit
