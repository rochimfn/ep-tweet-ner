from Extractor import Twitter
from Transformer import Cleaner
from Loader import NER
from pathlib import Path
from settings import settings
import os
import pickle
from datetime import datetime
import json

def extract(bearer_token, params, amount, path = None):
    scraper = Twitter(bearer_token)
    scraper.get(params, amount)
    if path is not None:
        scraper.persist(path)
    return scraper.fetch()

def transform(raw_data, clean_type, path = None):
    cleaner = Cleaner(raw_data)
    cleaner.clean(clean_type)
    if path is not None:
        cleaner.persist(path)
    return cleaner.fetch()

def load(new=True ,dataset=None, model_path=None):
    ner = NER()
    if new:
        ner.fit(dataset)
        if model_path is not None:
            ner.persist(model_path)
        ner.load()
        return ner
    else:
        if model_path is not None:
            ner.load(model_path)
            return ner
        else:
            print('Masukkan model')
            exit(1)



def main():
    ########################################
    ########    Untuk mining Data   ########
    ########################################
    # bearer_token = settings['bearer_token']
    # params = {}
    # params['query'] = '(@satgascovid19id OR @kemenkesRI) -is:retweet'
    # params['tweet.fields'] = 'text'

    # raw_data_path = Path(os.path.dirname(os.path.realpath(__file__))) / 'Data' / f'raw_data_{datetime.today().strftime("%Y-%m-%d")}.json'
    # raw_data = extract(bearer_token, params, 40000, raw_data_path)

    ########################################
    ########  Untuk cleaning data   ########
    ########################################
    # clean_data_path = Path(os.path.dirname(os.path.realpath(__file__))) / 'Data' / f'clean_data_{datetime.today().strftime("%Y-%m-%d")}.json'
    # clean_type = ['duplicate', 'emoji', 'retweet', 'mention', 'tags', 'links']
    # clean_data = transform(raw_data, clean_type, clean_data_path)
   
    ########################################################
    #################### Untuk NER nya  ####################
    ########################################################
    ######## Manual training dengan model dari blog ########
    ########################################################
    # path_dataset_ori = Path(os.path.dirname(os.path.realpath(__file__))) / 'Data' / 'ner_spacy_fmt_datasets.pickle'
    # open_dataset_ori = open(path_dataset_ori, 'rb')
    # dataset_ori = pickle.load(open_dataset_ori)
    # open_dataset_ori.close()
    # path_model_ori = Path(os.path.dirname(os.path.realpath(__file__))) / 'Model' / f'original_model_{datetime.today().strftime("%Y-%m-%d")}'
    # ner = load(new=True, dataset=dataset_ori, model_path=path_model_ori)

    ########################################################
    ########  Manual training dengan model sendiri  ########
    ########################################################
    # path_dataset_twt = Path(os.path.dirname(os.path.realpath(__file__))) / 'Data' / 'train_data_2021-04-10_labeled.pickle'
    # open_dataset_twt = open(path_dataset_twt, 'rb')
    # dataset_twt = pickle.load(open_dataset_twt)
    # open_dataset_twt.close()
    # path_model_twt = Path(os.path.dirname(os.path.realpath(__file__))) / 'Model' / f'twt_model_{datetime.today().strftime("%Y-%m-%d")}'
    # ner_twt = load(new=True, dataset=dataset_twt, model_path=path_model_twt)

    ################################################
    ################ Load test data ################
    ################################################
    with open(Path(os.path.dirname(os.path.realpath(__file__))) / 'Data' / f'test_data_{datetime.today().strftime("%Y-%m-%d")}.json', 'r') as f:
        tweets = '\n'.join(json.load(f))

    ################################################################
    ##########    Load model yang dibuat dari dataset blog  ########
    ################################################################
    path_model_ori = Path(os.path.dirname(os.path.realpath(__file__))) / 'Model' / f'original_model_{datetime.today().strftime("%Y-%m-%d")}'
    ner_ori = load(new=False, model_path=path_model_ori)

    doc = ner_ori.analysis(tweets)
    results_ori = []
    for ent in doc.ents:
        if ent.label_ == 'LOCATION':
            results_ori.append((ent.text, ent.label_))

    with open(Path(os.path.dirname(os.path.realpath(__file__))) / 'Results' / f'ori_{datetime.today().strftime("%Y-%m-%d")}.json', 'w') as target:
        target.write(json.dumps(results_ori, indent=4, sort_keys=True))

    ################################################################
    ########  Load model yang dibuat dari dataset sendiri   ########
    ################################################################
    path_model_twt = Path(os.path.dirname(os.path.realpath(__file__))) / 'Model' / f'twt_model_{datetime.today().strftime("%Y-%m-%d")}'
    ner_twt = load(new=False, model_path=path_model_twt)

    doc_twt = ner_twt.analysis(tweets)
    results_twt = []
    for ent in doc_twt.ents:
        if ent.label_ == 'LOCATION':
            results_twt.append((ent.text, ent.label_))

    with open(Path(os.path.dirname(os.path.realpath(__file__))) / 'Results' / f'twt_{datetime.today().strftime("%Y-%m-%d")}.json', 'w') as target:
        target.write(json.dumps(results_twt, indent=4, sort_keys=True))

if __name__ == '__main__':
    main()