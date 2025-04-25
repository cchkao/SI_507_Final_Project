import requests
from bs4 import BeautifulSoup, Comment
import time
import json
import os

class Statistics:
    ''' Class Attributes
    ----------------
    stats_table_id: str
        table id to get the stats on
        basketball reference

    stat_type: list

    Instance Attributes
    -------------------

    stats: dict
        different statistics every year
        - Basic Stats:
            - G: Game played
            - GS: Game Start
            - MP: Minutes played
            - FG: Field goal
            - FGA: Field goal attempt
            - FG%: Field goal percentage
            - 3P: Three point
            - 3PA: Three point attempt
            - 3P%: Three point percentage
            - 2P:
            - 2PA:
            - 2P%:
            - eFG%:
            - FT:
            - FTA:
            - FT%:
            - ORB:
            - DRB:
            - TRB:
            - AST:
            - STL:
            - BLK:
            - TOV:
            - PF:
            - P:

        - Advanced Stats:
            - PER: A measure of per minute production standardized
            - WS48:
            - VORP:
    '''

    headers = {'User-Agent': 'Mozilla/5.0'}
    stats_table_id = "per_game_stats"
    basic_stat_type = ["G",  "GS", "MP", "FG", "FGA", "FG%",
                "3P", "3PA", "3P%", "2P", "2PA", "2P%", 
                "eFG%", "FT", "FTA", "FT%", "ORB", "DRB",
                "TRB", "AST", "STL", "BLK", "TOV", "PF", "P"]
    advanced_stat_type = ["PER", "WS48", "VORP"]
    stat_type = basic_stat_type + advanced_stat_type

    def __init__(self, url, player_name):
        url_id = url.split('/')[-1][:-5]
        
        
        self.years = []
        self.stat_headers = []
        self.__stats = {}
        
        self.stat_file = "SaveData/Statistics/" + url_id + "_stats.json"

        # Read file from the previous existed files
        if os.path.exists(self.stat_file):
            with open(self.stat_file, 'r') as f:
                saved_data = json.load(f)
                self.years = [int(year) for year in saved_data["years"]]
                self.stat_headers = saved_data["stat_head"]
                self.__stats = {int(year): stat for year, stat in saved_data["stats"].items()}
        else:
            print(f"Fetch Statistic Data from Website for {player_name} ...")
            self.__fetchData(url)

    def __fetchData(self, url):
        response = None
        while response is None:
            response = requests.get(url, headers=Statistics.headers)
            time.sleep(5.0)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'id': Statistics.stats_table_id})

        for th in table.find('thead').find_all('th'):
            self.stat_headers.append(th.text)

        rows = table.find('tbody').find_all('tr')
            
        for row in rows:
            year_str = row.find('th', class_='left').get('csk')
            try:
                year = int(year_str)
                if year in self.years:
                    continue
                self.years.append(year)
            except:
                year = 0
            
            self.__stats[year] = {}

            cols = row.find_all('td')
            if cols:
                for i, col in enumerate(cols, start=1):
                    stats = self.stat_headers[i]
                    if i < len(self.stat_headers) and stats in Statistics.stat_type:
                        data = col.text.strip()
                        try:
                            self.__stats[year][stats] = float(data)
                        except:
                            self.__stats[year][stats] = data
            if self.__stats[year] == {}:
                self.__stats[year] = "Did not play"

        
        with open(self.stat_file, 'w') as f:
            player_data = {}
            player_data["years"] = self.years
            player_data["stat_head"] = self.stat_headers
            player_data["stats"] = self.__stats
            json.dump(player_data, f)

    
    def getStatsByType(self, stat_type) -> dict:
        if stat_type not in Statistics.type:
            print(f"This type of statistic ({stat_type}) is not recorded")
            return None
        
        req_stats = {key: value[stat_type] for key, value in self.__stats.items()}
        return req_stats
        
    def getStatsByYear(self, year) -> dict:
        if year not in self.__stats.keys():
            print(f"The statistics of this year ({year}) is not recorded")
            return None
        return self.__stats[year]

    def getSpecificStatsByYear(self, stat_type, year):
        if stat_type not in Statistics.type:
            print(f"This type of statistic ({stat_type}) is not recorded")
            return None
        if year not in self.__stats.keys():
            print(f"The statistics of this year ({year}) is not recorded")
            return None
        
        return self.__stats[year][stat_type]
    
    def getYear(self):
        return self.years