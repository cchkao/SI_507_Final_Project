---
title: NBA All-Star Players Network Analysis (SI 507 Final Project)

---

# NBA All-Star Players Network Analysis (SI 507 Final Project)
By Chen-Chien Kao 04/25/2025

## Introduction
This is the final project for the course SI 507. This project explores NBA All-Star players from 2000 to 2025, focusing on their teammate networks and on-court performance.

## Directory Struture
```
├── report
│   ├── Final_Report_CCK.pdf
├── src
│   ├── SaveData
│   │   ├── AllStars
│   │   │   ├── AllStars_{year}.json
│   │   ├── Figures
│   │   │   ├── {filename}.png
│   │   ├── Statistics
│   │   │   ├── {player_id}_stats.json
│   │   ├── Teammates
│   │   │   ├── {player_id}_teammates.json
│   ├── main.py
│   ├── UserInterface.py
│   ├── AllStarList.py
│   ├── Player.py
│   ├── Statistics.py
│   ├── util.py
├── ReadMe.md
```
## Files Discription
- **./report**:
    - Report_CCK.pdf: Final report for this project
- **./src**
    - /SaveData/AllStars: Folder to save the all-star roster files 
    - /SaveData/Figures: Folder to save the figure generated in the project 
    - /SaveData/Statistics*: Folder to save the files for statistics of the players.
    - /SaveData/Teammates: Folder to save the files for the teammmate relationship of the players
    - UserInterface.py: Class to handle the interaction with the user.
    - AllStarList.py: Class to store all the all-star players' objects and execute the function based on user's requests.
    - Player.py: Class to store the teammate information and player's individual data.
    - Statistics.py: Class to store the data of the player's statistic
    - util.py: Useful functions for the program.
- **README.md**: Just readme...

## Package Required
It works correctly with the following package versions:
```
beautifulsoup4==4.13.3
bs4==0.0.2
matplotlib==3.8.4
matplotlib-inline==0.1.6
numpy==1.26.4
requests==2.31.0
```
-- *To run the program, please run `python3 main.py` under the folder of ./src.*

## Command Supported
- **add_player**: Add a new player in the list for network analyzer.
- **best_duo**: Find the best teammates for a specific player in the list.
- **comp_duo**: Compare two duos for the specific players in the list.
- **disp_all**: Display all players in the list."
- **disp_star**: Display the all-star roster in the specific year.
- **disp_stat**: Display the statistic of the specific player in the specific year.
- **find_min_deg**: Find the minimum degree of teammate connection between two players.
- **max_connect**: Find the players with maximum teammate connection in the list.
- **plot_fig**: Draw the figure of the teammate relationship between players in the list.
- **help**: Show the available command.
- **exit**: Exit the program.