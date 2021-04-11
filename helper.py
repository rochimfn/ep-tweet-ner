from pathlib import Path
import os
import pickle
from datetime import datetime
import json

def spliter(list_of_tweets, path):
    test = list_of_tweets[:87]
    train = list_of_tweets[87:]
    with open(path / f'train_data_{datetime.today().strftime("%Y-%m-%d")}.json', 'w') as target:
            target.write(json.dumps([[tweet,[]] for tweet in train], indent=4, sort_keys=True))
    with open(path / f'test_data_{datetime.today().strftime("%Y-%m-%d")}.json', 'w') as target:
            target.write(json.dumps([tweet for tweet in test], indent=4, sort_keys=True))
    return train, test

def convert(labeled_tweets, path):
    temp = []

    for arr in labeled_tweets:
        temp_arr = []
        temp_arr.append(arr[0])
        if len(arr[1]) > 0:
            ent = []
            for i in arr[1]:
                start = arr[0].index(i)
                end = arr[0].index(i) + len(i)
                ent.append((start, end, 'LOCATION'))
            temp_arr.append({'entities': ent})
            temp.append(tuple(temp_arr))
        else:
            continue
    print(temp)
    with open(path, 'wb') as target:
            target.write(pickle.dumps(temp))


def main():
    # with open(Path(os.path.dirname(os.path.realpath(__file__))) / 'Data' / f'clean_data_{datetime.today().strftime("%Y-%m-%d")}.json', 'r') as f:
    #     clean_data = json.load(f)

    # train, test = spliter(clean_data, Path(os.path.dirname(os.path.realpath(__file__))) / 'Data')

    with open(Path(os.path.dirname(os.path.realpath(__file__))) / 'Data' / f'train_data_{datetime.today().strftime("%Y-%m-%d")}_labeled.json', 'r') as f:
        labeled_data = json.load(f)
    
    path = Path(os.path.dirname(os.path.realpath(__file__))) / 'Data' / f'train_data_{datetime.today().strftime("%Y-%m-%d")}_labeled.pickle'
    convert(labeled_data, path)


    

if __name__ == '__main__':
    main()