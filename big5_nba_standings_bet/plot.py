from datetime import date, timedelta
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
jack_score_east = jai_score_east.copy()
jim_score_east = jai_score_east.copy()
pat_score_east = jai_score_east.copy()
jai_score_west = {'Jazz': 0, 'Clippers': 0, 'Nuggets': 0, 'Lakers': 0,
                  'Suns': 0, 'Blazers': 0, 'Spurs': 0, 'Warriors': 0,
                  'Mavericks': 0, 'Grizzlies': 0, 'Kings': 0,  'Pelicans': 0,
                  'Rockets': 0, 'Thunder': 0, 'Wolves': 0}
jack_score_west = jai_score_west.copy()
jim_score_west = jai_score_west.copy()
pat_score_west = jai_score_west.copy()
# /s>

# <s Compute (actual - predicted) standings for each day since X (30/04/2021)
# for each person for each team, and create subplots for team diffs day-by-day

# Daily total scores
jai_score_tot = np.zeros(shape=(30,))
jai_score_tot_east = np.zeros(shape=(30,))
jai_score_tot_west = np.zeros(shape=(30,))
jack_score_tot = np.zeros(shape=(30,))
jack_score_tot_east = np.zeros(shape=(30,))
jack_score_tot_west = np.zeros(shape=(30,))
jim_score_tot = np.zeros(shape=(30,))
jim_score_tot_east = np.zeros(shape=(30,))
jim_score_tot_west = np.zeros(shape=(30,))
pat_score_tot = np.zeros(shape=(30,))
pat_score_tot_east = np.zeros(shape=(30,))
pat_score_tot_west = np.zeros(shape=(30,))


# <ss Update scores
dcur = date(year=2021, month=5, day=1)
dfin = date.today()
score_idx = 0
xlabels2 = [str(dcur)]
while dcur <= dfin:
    # Get actual standings for each day since X
    url = "https://www.basketball-reference.com/friv/standings.fcgi"
    url_suffix = f"?month={dcur.month}&day={dcur.day}&year=2021"
    html = urlopen(url + url_suffix)
    soup = BeautifulSoup(html)
    tables = soup.find_all('table')  # East and West conf are 1st and 2nd in set
    east_standings = tables[0].findChildren('tr')[1:]  # skip header row
    west_standings = tables[1].findChildren('tr')[1:]
    assert (len(west_standings) == len(east_standings) == 15), \
        "Error: number of teams"

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

    # Consolidate scores in a single dict
    scores = {'jai': jai_score_east | jai_score_west,
              'jack': jack_score_east | jack_score_west,
              'jim': jim_score_east | jim_score_west,
              'pat': pat_score_east | pat_score_west}

    # Plot bars: grouped team-by-team standings by person for the current day
    xlabels = ('Bucks', 'Nets', '76ers', 'Celtics', 'Raptors', 'Pacers',
               'Heat', 'Hawks', 'Wizards', 'Knicks', 'Bulls', 'Hornets',
               'Magic', 'Cavaliers', 'Pistons',
               'Jazz', 'Clippers', 'Nuggets', 'Lakers', 'Suns', 'Blazers',
               'Spurs', 'Warriors', 'Mavericks', 'Grizzlies', 'Kings',
               'Pelicans', 'Rockets', 'Thunder', 'Wolves')
    x = np.arange(len(xlabels)) * 1.5
    bar_width = 0.25
    fig, ax = plt.subplots()
    ax.bar(x - (bar_width * 2), np.array(list(scores['jai'].values())) + 0.1,
           width=bar_width, color='black')
    ax.bar(x - bar_width, np.array(list(scores['jack'].values())) + 0.1,
           width=bar_width, color='red')
    ax.bar(x, np.array(list(scores['jim'].values())) + 0.1,
           width=bar_width, color='green')
    ax.bar(x + bar_width, np.array(list(scores['pat'].values())) + 0.1,
           width=bar_width, color='blue')
    ax.set_title(str(dcur))
    ax.set_ylabel('True - Pred')
    ax.set_xticks(x)
    ax.set_xticklabels(xlabels, rotation=45)
    ax.legend(['Jai', 'Jack', 'Jim', 'Pat'])

    # Compute total scores
    jai_score_tot_east[score_idx] = \
        sum(abs(np.array(list(jai_score_east.values()))))
    jai_score_tot_west[score_idx] = \
        sum(abs(np.array(list(jai_score_west.values()))))
    jai_score_tot[score_idx] = \
        jai_score_tot_east[score_idx] + jai_score_tot_west[score_idx]
    jack_score_tot_east[score_idx] = \
        sum(abs(np.array(list(jack_score_east.values()))))
    jack_score_tot_west[score_idx] = \
        sum(abs(np.array(list(jack_score_west.values()))))
    jack_score_tot[score_idx] = \
        jack_score_tot_east[score_idx] + jack_score_tot_west[score_idx]
    jim_score_tot_east[score_idx] = \
        sum(abs(np.array(list(jim_score_east.values()))))
    jim_score_tot_west[score_idx] = \
        sum(abs(np.array(list(jim_score_west.values()))))
    jim_score_tot[score_idx] = \
        jim_score_tot_east[score_idx] + jim_score_tot_west[score_idx]
    pat_score_tot_east[score_idx] = \
        sum(abs(np.array(list(pat_score_east.values()))))
    pat_score_tot_west[score_idx] = \
        sum(abs(np.array(list(pat_score_west.values()))))
    pat_score_tot[score_idx] = \
        pat_score_tot_east[score_idx] + pat_score_tot_west[score_idx]

    # Update i vars
    score_idx += 1
    dcur += timedelta(days=1)
    xlabels2.append(str(dcur))

# /ss> /s>

# Plot overall score and conf scores for each person for each day since X
dcur = date(year=2021, month=5, day=1)
dfin = date.today()
xlabels2 = [str(date(year=2021, month=5, day=1))]
dcur += timedelta(days=1)
while dcur <= dfin:
    xlabels2.append(str(dcur))
    dcur += timedelta(days=1)

x = np.arange(len(xlabels2))
fig2, ax2 = plt.subplots(nrows=2, ncols=1)
ax2[0].plot(x, jai_score_tot[0 : len(xlabels2)], color='black',
            marker='v', markersize=10, linewidth=2)
ax2[0].plot(x, jack_score_tot[0 : len(xlabels2)], color='red',
            marker='v', markersize=10, linewidth=2)
ax2[0].plot(x, jim_score_tot[0 : len(xlabels2)], color='green',
            marker='v', markersize=10, linewidth=2)
ax2[0].plot(x, pat_score_tot[0 : len(xlabels2)], color='blue',
            marker='v', markersize=10, linewidth=2)
ax2[0].set_xticks([])
ax2[0].set_title("Sum of Total of Abs Deviations from Actual Standings")
ax2[0].set_ylabel("Sum(Abs(True - Pred))")
ax2[0].legend(['Jai', 'Jack', 'Jim', 'Pat'], loc='lower left')
ax2[1].plot(x, jai_score_tot_east[0 : len(xlabels2)], color='black',
            marker='v', markersize=10, linewidth=2, linestyle='-.')
ax2[1].plot(x, jai_score_tot_west[0 : len(xlabels2)], color='black',
            marker='v', markersize=10, linewidth=2, linestyle=':')
ax2[1].plot(x, jack_score_tot_east[0 : len(xlabels2)], color='red',
            marker='v', markersize=10, linewidth=2, linestyle='-.')
ax2[1].plot(x, jack_score_tot_west[0 : len(xlabels2)], color='red',
            marker='v', markersize=10, linewidth=2, linestyle=':')
ax2[1].plot(x, jim_score_tot_east[0 : len(xlabels2)], color='green',
            marker='v', markersize=10, linewidth=2, linestyle='-.')
ax2[1].plot(x, jim_score_tot_west[0 : len(xlabels2)], color='green',
            marker='v', markersize=10, linewidth=2, linestyle=':')
ax2[1].plot(x, pat_score_tot_east[0 : len(xlabels2)], color='blue',
            marker='v', markersize=10, linewidth=2, linestyle='-.')
ax2[1].plot(x, pat_score_tot_west[0 : len(xlabels2)], color='blue',
            marker='v', markersize=10, linewidth=2, linestyle=':')
ax2[1].set_xticks(x)
ax2[1].set_xticklabels(xlabels2, rotation=0)
ax2[1].set_ylabel("Sum(Abs(True - Pred))")
ax2[1].legend(['East', 'West'], loc='lower left')

