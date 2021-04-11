import json
# import re

class Cleaner:
    def __init__(self, raw_data):
        self.__raw_data = raw_data
        self.__clean_data = []

    def clean(self, cleaner_list = []):
        print(f'Panjang data kotor {len(self.__raw_data)}')
        for data in self.__raw_data:
            self.__clean_data.append(data['text'].replace('\n', ' ').replace('\u2026', ''))

        for cleaner in cleaner_list:
            if cleaner == 'duplicate':
                self.__duplicate()
            elif cleaner == 'mention':
                self.__mention()
            elif cleaner == 'tags':
                self.__tags()
            elif cleaner == 'retweet':
                self.__retweet()
            elif cleaner == 'emoji':
                self.__emoji()
            elif cleaner == 'links':
                self.__links()
            self.__clean_data = list(filter(lambda x:x!='', self.__clean_data))
        print(f'Panjang data bersih {len(self.__clean_data)}')
        return True

    def fetch(self):
        return self.__clean_data

    def persist(self, path, mode = 'w'):
        with open(path, mode) as target:
            target.write(json.dumps(self.__clean_data, indent=4, sort_keys=True))

    def __duplicate(self):
        self.__clean_data = list(set(self.__clean_data))
        return True

    def __mention(self):
        temp_data = []
        for tweet in self.__clean_data:
            temp_data.append(" ".join(filter(lambda x:x[0]!='@', tweet.split())))
        self.__clean_data = temp_data

    def __tags(self):
        temp_data = []
        for tweet in self.__clean_data:
            temp_data.append(" ".join(filter(lambda x:x[0]!='#', tweet.split())))
        self.__clean_data = temp_data

    def __links(self):
        temp_data = []
        for tweet in self.__clean_data:
            temp_data.append(" ".join(filter(lambda x:x[:4]!='http', tweet.split())))
        self.__clean_data = temp_data

    def __retweet(self):
        self.__clean_data = list(filter(lambda x:x[:2].lower()!='rt', self.__clean_data))
    
    def __emoji(self):
        temp_data = []
        for tweet in self.__clean_data:
            temp_data.append(self.__de_emojify(tweet))
        self.__clean_data = temp_data

    def __de_emojify(self, text):
        # regrex_pattern = re.compile(pattern = "["
        #     u"\U0001F600-\U0001F64F"  # emoticons
        #     u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        #     u"\U0001F680-\U0001F6FF"  # transport & map symbols
        #     u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        #                     "]+", flags = re.UNICODE)
        # return regrex_pattern.sub(r'',text)
        return text.encode('ascii', 'ignore').decode('ascii')