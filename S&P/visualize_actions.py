import pickle

with open('action/stock_actions.pickle', 'rb') as file:
    activity = pickle.load(file)


for ticker in activity.keys():
    print(ticker)
    print('\n')

    for action in activity[ticker]:
        print('\t{} at {}'.format(action['action'], action['time']))

    print('\n')
