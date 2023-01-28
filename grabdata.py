import numpy as np
import requests
import json
import time
import os
    
patch = "12_21"

ids = list(np.load('champids.npy'))
names = list(np.load('champnames.npy'))
lanes = ["top", "jungle", "middle", "bottom", "support"]

def collect(syn):
    wins = np.zeros((len(ids), len(ids), 5, 5)).astype(int)
    games = np.zeros((len(ids), len(ids), 5, 5)).astype(int) 
    for n in range(0, len(ids)):
        for mylane in range(5):
            URL = "https://axe.lolalytics.com/mega/?ep="+["champion", "champion2"][syn]+"&p=d&v=1&patch="+patch.replace('_', '.')+"&cid="+str(ids[n])+"&lane="+lanes[mylane]+"&tier=all&queue=420&region=all/"
            page = requests.get(URL, headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 Chrome/98.0.4758.102"})
            data = json.loads(page.content)
            time.sleep(1)
            print(names[n])
            print(URL)
            for lane in range(5):
                if len(data) < 4 or ((lane == mylane) and syn):
                    continue
                for res in data[["enemy_", "team_"][syn]+lanes[lane]]:
                    games[n, ids.index(res[0]), mylane, lane] = res[1]
                    wins[n, ids.index(res[0]), mylane, lane] = res[2]
    return wins, games

synergywins, synergygames = collect(syn = True)
counterwins, countergames = collect(syn = False)

np.save(os.path.join('data', patch, 'synergywins'), synergywins)
np.save(os.path.join('data', patch, 'synergygames'), synergygames)
np.save(os.path.join('data', patch, 'counterwins'), counterwins)
np.save(os.path.join('data', patch, 'countergames'), countergames)