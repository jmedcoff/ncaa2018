import pyexcel as pe
from operator import itemgetter
from collections import defaultdict
import numpy as np
np.set_printoptions(threshold=np.nan)

data = pe.get_records(0, file_name="gamedata.xlsx")
n = len(data) # 11824

# "data" is an ordered dictionary
teams = set()
for entry in data:
    teams.add(entry['Team'])

# there are 656 teams in total. we want to mine the top of the pile

teams = list(teams)
num_teams = len(teams)

teamname = dict()
i = 0

for t in teams:
    teamname[i] = t
    i += 1

# each team has a unique numerical key. this is how we will refer to
# teams from now on

teamnum = {v: k for k, v in teamname.items()}

A = np.zeros((num_teams, num_teams))

games_played = defaultdict(lambda: 0)

for entry in data:
    home, away = teamnum[entry['Team']], teamnum[entry['Opponent']]
    result = entry['Team Result']
    games_played[home] += 1
    games_played[away] += 1
    if result == 'Win':
        A[home][away] += 1
    elif result == 'Loss':
        A[away][home] += 1

for i in range(num_teams):
    for j in range(num_teams):
        A[i][j] /= games_played[i]


# now A is the preference matrix; a_ij is the number of times team i
# won against team j

eigvals, eigvecs = np.linalg.eig(A)
maxeig = 0
maxvec = 0
for i in range(len(eigvals)):
    if eigvals[i] > maxeig:
        maxeig = eigvals[i]
        maxvec = eigvecs[:, i]

results = dict()

for i in range(len(maxvec)):
    results[teamname[i]] = np.real(maxvec[i])

results = sorted(results.items(), key=itemgetter(1), reverse=True)

with open('results.txt', 'w') as file:
    for entry in results:
        file.write(str(entry) + "\n")
