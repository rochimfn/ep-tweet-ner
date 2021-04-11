import spacy
import random
from spacy.util import minibatch, compounding
from spacy import load, displacy
from pathlib import Path

class NER:
    def __init__(self):
        self.__nlp_train = None
        self.__nlp_loaded = None

    def fit(self, dataset):
        self.__dataset = dataset
        self.__nlp_train=spacy.blank("id")
        self.__nlp_train.add_pipe(self.__nlp_train.create_pipe('ner'))
        self.__nlp_train.begin_training()
        ner=self.__nlp_train.get_pipe("ner")
        for _, annotations in self.__dataset:
            for ent in annotations.get("entities"):
                ner.add_label(ent[2])
                break

        pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
        unaffected_pipes = [pipe for pipe in self.__nlp_train.pipe_names if pipe not in pipe_exceptions]

        with self.__nlp_train.disable_pipes(*unaffected_pipes):
            for iteration in range(30):
                random.shuffle(self.__dataset)
                losses = {}
                batches = minibatch(self.__dataset, size=compounding(4.0, 32.0, 1.001))
                for batch in batches:
                    texts, annotations = zip(*batch)
                    self.__nlp_train.update(
                                texts, 
                                annotations,
                                drop=0.5,
                                losses=losses,
                            )
                print("Losses at iteration {}".format(iteration), losses)

    def persist(self, path):
        self.__nlp_train.to_disk(path)
        print("Saved model to", path)

    def load(self, path = None):
        if path is not None:
            print("Loading from", path)
            self.__nlp_loaded = spacy.load(path)
            print('Loaded')
        else:
            print('Loading from training object')
            self.__nlp_loaded = self.__nlp_train
            print('Loaded')

    def analysis(self, text):
        if self.__nlp_loaded is None:
            print('Tidak ada objek, fit atau load terlebih dahulu')
            exit(1)
        else:
            return self.__nlp_loaded(text)