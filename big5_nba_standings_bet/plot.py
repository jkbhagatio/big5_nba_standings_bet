import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import nba_api as nba
from urllib.request import urlopen
from bs4 import BeautifulSoup

# <s Initialize predicted standings
jai_pred_east = ('Bucks', 'Nets', '76ers', 'Celtics', 'Raptors', 'Pacers',
                 'Heat', 'Hawks', 'Wizards', 'Knicks', 'Bulls', 'Hornets',
                 'Magic', 'Cavaliers', 'Pistons')
jack_pred_east = ('76ers', 'Nets', 'Bucks', 'Celtics', 'Raptors', 'Pacers',
                  'Knicks', 'Heat', 'Bulls', 'Hornets', 'Hawks', 'Magic',
                  'Cavaliers', 'Wizards', 'Pistons')
jim_pred_east = ('Nets', '76ers', 'Bucks', 'Celtics', 'Raptors', 'Pacers',
                 'Heat', 'Bulls', 'Hornets', 'Hawks', 'Knicks', 'Magic',
                 'Wizards', 'Cavaliers', 'Pistons')
pat_pred_east = ('Nets', '76ers', 'Celtics', 'Bucks', 'Pacers', 'Raptors',
                 'Heat', 'Hornets', 'Hawks', 'Knicks', 'Wizards', 'Bulls',
                 'Magic', 'Cavaliers', 'Pistons')
jai_pred_west = ('Jazz', 'Clippers', 'Nuggets', 'Lakers', 'Suns', 'Blazers',
                 'Spurs', 'Warriors', 'Mavericks', 'Grizzlies', 'Kings',
                 'Pelicans', 'Rockets', 'Thunder', 'Wolves')
jack_pred_west = ('Lakers', 'Clippers', 'Jazz', 'Blazers', 'Nuggets', 'Suns',
                  'Warriors', 'Spurs', 'Mavericks', 'Pelicans', 'Grizzlies',
                  'Kings', 'Rockets', 'Thunder', 'Wolves')
jim_pred_west = ('Jazz', 'Lakers', 'Clippers', 'Nuggets', 'Blazers', 'Suns',
                 'Mavericks', 'Spurs', 'Warriors', 'Kings', 'Grizzlies',
                 'Pelicans', 'Thunder', 'Rockets', 'Wolves')
pat_pred_west = ('Jazz', 'Clippers', 'Blazers', 'Lakers', 'Nuggets', 'Suns',
                 'Warriors', 'Mavericks', 'Grizzlies', 'Spurs', 'Kings',
                 'Pelicans', 'Thunder', 'Rockets', 'Wolves')

pred = {'jai_east': jai_pred_east, 'jack_east': jack_pred_east,
        'jim_east': jim_pred_east, 'pat_east': pat_pred_east,
        'jai_west': jai_pred_west, 'jack_west': jack_pred_west,
        'jim_west': jim_pred_west, 'pat_west': pat_pred_west}
# /s>

# <s Initialize scores: (actual - predicted)
jai_score_east = {'Bucks': 0, 'Nets': 0, '76ers': 0, 'Celtics': 0,
                  'Raptors': 0, 'Pacers': 0, 'Heat': 0, 'Hawks': 0,
                  'Wizards': 0, 'Knicks': 0, 'Bulls': 0, 'Hornets': 0,
                  'Magic': 0, 'Cavaliers': 0, 'Pistons': 0}
jack_score_east = {'Bucks': 0, 'Nets': 0, '76ers': 0, 'Celtics': 0,
                   'Raptors': 0, 'Pacers': 0, 'Heat': 0, 'Hawks': 0,
                   'Wizards': 0, 'Knicks': 0, 'Bulls': 0, 'Hornets': 0,
                   'Magic': 0, 'Cavaliers': 0, 'Pistons': 0}
jim_score_east = {'Bucks': 0, 'Nets': 0, '76ers': 0, 'Celtics': 0,
                  'Raptors': 0, 'Pacers': 0, 'Heat': 0, 'Hawks': 0,
                  'Wizards': 0, 'Knicks': 0, 'Bulls': 0, 'Hornets': 0,
                  'Magic': 0, 'Cavaliers': 0, 'Pistons': 0}
pat_score_east = {'Bucks': 0, 'Nets': 0, '76ers': 0, 'Celtics': 0,
                  'Raptors': 0, 'Pacers': 0, 'Heat': 0, 'Hawks': 0,
                  'Wizards': 0, 'Knicks': 0, 'Bulls': 0, 'Hornets': 0,
                  'Magic': 0, 'Cavaliers': 0, 'Pistons': 0}
jai_score_west = {'Jazz': 0, 'Clippers': 0, 'Nuggets': 0, 'Lakers': 0,
                  'Suns': 0, 'Blazers': 0, 'Spurs': 0, 'Warriors': 0,
                  'Mavericks': 0, 'Grizzlies': 0, 'Kings': 0,  'Pelicans': 0,
                  'Rockets': 0, 'Thunder': 0, 'Wolves': 0}
jack_score_west = {'Jazz': 0, 'Clippers': 0, 'Nuggets': 0, 'Lakers': 0,
                   'Suns': 0, 'Blazers': 0, 'Spurs': 0, 'Warriors': 0,
                   'Mavericks': 0, 'Grizzlies': 0, 'Kings': 0,  'Pelicans': 0,
                   'Rockets': 0, 'Thunder': 0, 'Wolves': 0}
jim_score_west = {'Jazz': 0, 'Clippers': 0, 'Nuggets': 0, 'Lakers': 0,
                  'Suns': 0, 'Blazers': 0, 'Spurs': 0, 'Warriors': 0,
                  'Mavericks': 0, 'Grizzlies': 0, 'Kings': 0,  'Pelicans': 0,
                  'Rockets': 0, 'Thunder': 0, 'Wolves': 0}
pat_score_west = {'Jazz': 0, 'Clippers': 0, 'Nuggets': 0, 'Lakers': 0,
                  'Suns': 0, 'Blazers': 0, 'Spurs': 0, 'Warriors': 0,
                  'Mavericks': 0, 'Grizzlies': 0, 'Kings': 0,  'Pelicans': 0,
                  'Rockets': 0, 'Thunder': 0, 'Wolves': 0}

scores = {'jai_east': jai_score_east, 'jack_east': jack_score_east,
          'jim_east': jim_score_east, 'pat_east': pat_score_east,
          'jai_west': jai_score_west, 'jack_west': jack_score_west,
          'jim_west': jim_score_west, 'pat_west': pat_score_west}
# /s>

# Get actual standings for each day since X (04/30/2021)
url = "https://www.basketball-reference.com/friv/standings.fcgi"
html = urlopen(url)
soup = BeautifulSoup(html)
tables = soup.find_all('table')  # East and West conf are 1st and 2nd in set
east_standings = tables[0].findChildren('tr')[1:]  # skip header row
west_standings = tables[1].findChildren('tr')[1:]
assert (len(west_standings) == len(east_standings) == 15), \
       "Error: number of teams"

# Compute (actual - predicted) standings for each day since X for each person
# for each team, and create  subplots for team diffs day-by-day

# Eastern conf
for standing, team in enumerate(east_standings):
    pred_standing = 0
    for pred_team in jai_pred_east:
        if pred_team in str(team):
            break
        pred_standing += 1
    jai_score_east[pred_team] = standing - pred_standing
    pred_standing = 0
    for pred_team in jack_pred_east:
        if pred_team in str(team):
            break
        pred_standing += 1
    jack_score_east[pred_team] = standing - pred_standing
    pred_standing = 0
    for pred_team in jim_pred_east:
        if pred_team in str(team):
            break
        pred_standing += 1
    jim_score_east[pred_team] = standing - pred_standing
    pred_standing = 0
    for pred_team in pat_pred_east:
        if pred_team in str(team):
            break
        pred_standing += 1
    pat_score_east[pred_team] = standing - pred_standing

# Western conf
for standing, team in enumerate(west_standings):
    pred_standing = 0
    for pred_team in jai_pred_west:
        if pred_team in str(team):
            break
        pred_standing += 1
    jai_score_west[pred_team] = standing - pred_standing
    pred_standing = 0
    for pred_team in jack_pred_west:
        if pred_team in str(team):
            break
        pred_standing += 1
    jack_score_west[pred_team] = standing - pred_standing
    pred_standing = 0
    for pred_team in jim_pred_west:
        if pred_team in str(team):
            break
        pred_standing += 1
    jim_score_west[pred_team] = standing - pred_standing
    pred_standing = 0
    for pred_team in pat_pred_west:
        if pred_team in str(team):
            break
        pred_standing += 1
    pat_score_west[pred_team] = standing - pred_standing

# Plot overall score for each person for each day since X

