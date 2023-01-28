import numpy as np
import pandas as pd
from scipy.special import logit as lg
from scipy.special import expit as lgst
from sklearn.decomposition import PCA as PCA
from sklearn.linear_model import LinearRegression as LinReg

import os

patch = '12_21'

synergygames = np.load('data/'+patch+'/synergygames.npy')
synergywins = np.load('data/'+patch+'/synergywins.npy')
countergames = np.load('data/'+patch+'/countergames.npy')
counterwins = np.load('data/'+patch+'/counterwins.npy')

wins = np.sum(synergywins, axis =(0,2))/4
games = np.sum(synergygames, axis =(0,2))/4
roledeltas = lg(wins / games)
games4d = np.transpose([[games]*5]*len(games), axes=(2,3,0,1))

picks = np.transpose(synergygames - countergames, axes=(1,3,0,2))
roledeltas += -np.einsum('ijkl,kl->ij', picks / games4d, roledeltas)
basedeltas = np.amax(roledeltas, axis=1)
roledeltas = roledeltas - np.transpose([basedeltas]*5)

wr1 = np.transpose([[lg(wins / games)]*5]*len(games), axes=(2,0,3,1))
wr2 = np.transpose([[lg(wins / games)]*5]*len(games), axes=(0,2,1,3))

totalwins = np.sum(synergywins, axis=(2,3))
totalgames = np.sum(synergygames, axis=(2,3))
expwins = np.einsum('ijkl,ijkl->ij', synergygames, lgst(wr1 + wr2))
synergies = lg((totalwins - expwins) / (totalgames + 1000) + 0.5)

totalwins = np.sum(counterwins, axis=(2,3))
totalgames = np.sum(countergames, axis=(2,3))
expwins = np.einsum('ijkl,ijkl->ij', countergames, lgst(wr1 - wr2))
counters = lg((totalwins - expwins) / (totalgames + 1000) + 0.5)

pcs = PCA(len(games)).fit_transform(synergies)[:, [0, 2]]
synergies += LinReg().fit(pcs, synergies).predict(pcs) * np.identity(len(games))

np.save(os.path.join('data', patch, 'games'), games)
np.save(os.path.join('data', patch, 'total'), np.sum(games)/10)
np.save(os.path.join('data', patch, 'roledeltas'), roledeltas)
np.save(os.path.join('data', patch, 'basedeltas'), basedeltas)
np.save(os.path.join('data', patch, 'synergies'), np.round(synergies,5))
np.save(os.path.join('data', patch, 'counters'), np.round(counters, 5))