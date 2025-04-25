import requests
from bs4 import BeautifulSoup
import time
    
def FindUrlByName(player_name):
    # Construct the URL to search for the player on Basketball Reference
    base_url = "https://www.basketball-reference.com/search/search.fcgi?"
    search_name = player_name.replace(' ', '+')
    name_url = "?hint=" + search_name + "&search=" + search_name + "&pid=&idx="
    search_url = base_url + name_url
    # params = {'search': player_name.replace(' ', '+') + "&pid=&idx="}
    # response = requests.get(base_url, params=params)
    print("")
    print(f"Search Player: {player_name} ...")
    print("")
    response = None
    while response is None:
        response = requests.get(search_url)
        time.sleep(5)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find player link (assuming the first search result is the correct player)
        player_link = soup.find('div', class_='search-item-url')
        if player_link:
            full_url = "https://www.basketball-reference.com" + player_link.text
            return full_url
        else:
            return "FAILURE"
    else:
        return "FAILURE"
    
def PrintStatsTable(stats, col_per_rol):
    header_tmp = []
    data_tmp = []
    len_tmp = []
    col_idx = 0
    for dict_idx, (key, value) in enumerate(stats.items()):
        header_tmp.append(key)
        data = str(value)
        data_tmp.append(data)
        len_tmp.append(max(len(key), len(data)) + 2)
        col_idx += 1
        
        if (col_idx == col_per_rol) \
            or (dict_idx == len(stats) - 1):
            line_pat = "-" * (sum(len_tmp) + len(header_tmp) + 1)

            print(line_pat)
            print_str = "|"
            for i in range(len(header_tmp)):
                print_str = print_str \
                          + header_tmp[i].center(len_tmp[i]) \
                          + "|"
            print(print_str)

            print(line_pat)
            print_str = "|"
            for i in range(len(header_tmp)):
                print_str = print_str \
                          + data_tmp[i].center(len_tmp[i]) \
                          + "|"
            print(print_str)
            print(line_pat)
            
            header_tmp = []
            data_tmp = []
            len_tmp = []
            col_idx = 0

def printDuoInfo(duo_info):

    team_num = 0
    team_list = []
    year_len = 11
    team_len = 7
    mp_len = 12
    pts_len = 12
    total_len = year_len + team_len \
              + mp_len + pts_len + 5
    line_pat = total_len * "-"
    list_len = len(duo_info["year"])
    if list_len > 1:
        multi_year = True
    else:
        multi_year = False

    print(line_pat)
    header_str = "|"
    year_str = "Year"
    header_str += year_str.center(year_len)
    header_str += "|"
    team_str = "Team"
    header_str += team_str.center(team_len)
    header_str += "|"
    mp_str = "MP"
    header_str += mp_str.center(mp_len)
    header_str += "|"
    mp_str = "PTS"
    header_str += mp_str.center(pts_len)
    header_str += "|"

    print(header_str)
    for idx in range(list_len):
        print(line_pat)
        print_str = "|"
        year_str = f"{duo_info["year"][idx]-1}-{duo_info["year"][idx]}"
        print_str += year_str.center(year_len)
        print_str += "|"
        team_str = duo_info["team"][idx]
        if team_str not in team_list:
            team_num += 1
            team_list.append(team_str)
        print_str += team_str.center(team_len)
        print_str += "|"
        mp_str = f"{duo_info["MP"][idx][0]}:{duo_info["MP"][idx][1]}"
        print_str += mp_str.center(mp_len)
        print_str += "|"
        if duo_info["PTS"][idx] >= 0:
            pts_str = "+"
        else:
            pts_str = ""
        pts_str += f"{duo_info["PTS"][idx]}"
        print_str += pts_str.center(pts_len)
        print_str += "|"
        print(print_str)   
    print(line_pat)

    if multi_year:
        ovr_len = year_len + team_len + 1
        total_len = ovr_len + mp_len + pts_len + 4
        header_str = "|"
        ovr_str = "Overall"
        header_str += ovr_str.center(ovr_len)
        header_str += "|"
        mp_str = "Total MP"
        header_str += mp_str.center(mp_len)
        header_str += "|"
        pts_str = "Avg. PTS"
        header_str += pts_str.center(pts_len)
        header_str += "|"
        print(header_str)
        print(line_pat)
        print_str = "|"
        if team_num > 1:
            ovr_str = f"{team_num} Teams"
        else:
            ovr_str = f"{team_num} Team"
        print_str += ovr_str.center(ovr_len)
        print_str += "|"
        total_time = 0
        total_pt = 0
        for mp, pts in zip(duo_info["MP"], duo_info["PTS"]):
            time = mp[0] * 60 + mp[1]
            weight_pt = time * pts
            total_time += time
            total_pt += weight_pt
        avg_weight_pt = round(total_pt / total_time, 1)
        min_time = total_time // 60
        sec_time = total_time - min_time * 60
        mp_str = f"{min_time}:{sec_time}"
        print_str += mp_str.center(mp_len)
        print_str += "|"
        if avg_weight_pt >= 0:
            pts_str = "+"
        else:
            pts_str = ""
        pts_str += f"{avg_weight_pt}"
        print_str += pts_str.center(pts_len)
        print_str += "|"
        print(print_str)
        print(line_pat)
    print("")

def printConnectPath(start_p, end_p, connect_path):
    
    num_degree = connect_path[0]
    if num_degree == 0:
        print(f"There is no teamate connection between {start_p} and {end_p}")
    
    print("")
    print(f"========= Teammate connection from {start_p} to {end_p} =========")
    print(f"Number of the degree: {num_degree}")
    print("Path: ", end="")
    print_idx = 0
    for connect_p in connect_path[1]:
        print(f"{connect_p}", end="")
        print_idx += 1
        if print_idx != (num_degree+1):
            if(print_idx % 3 == 0):
                print("")
                print("  ", end="")
            print(" -> ", end="")
    print("")

def printPlayerList(player_list):
    
    col_idx = 0
    name_len = 25
    for player in sorted(player_list):
        if col_idx % 3 == 0:
            print("")
        print(f" {player.center(name_len)} ", end="")
        col_idx += 1
