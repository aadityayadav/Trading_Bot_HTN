import pickle
import pandas as pd
from datetime import datetime, timedelta

with open('action/stock_actions.pickle', 'rb') as file:
    activity = pickle.load(file)

actions = 0

for ticker in activity.keys():
    #print(ticker)
    #print('\n')

    for action in activity[ticker]:
        #print('\t{} at {}'.format(action['action'], action['time']))
        actions += 1

    #print('\n')

print(actions)