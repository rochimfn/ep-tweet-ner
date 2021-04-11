import requests
import json

class Twitter:
    def __init__(self, token):
        self.__token = token
        self.__oldest_id = 0
        self.__raw_data = []
        self.__params = {}
        self.__params['max_results'] = 100


    def get(self, params, amount = 1000):
        iteration = round(amount/100)
        params = {**self.__params, **params}

        if amount%100 > 0:
            iteration+=1

        for i in range(iteration):
            if i == 0 and self.__oldest_id == 0:
                json_response = self.__search_twitter(params=params)
                self.__oldest_id = json_response['meta']['oldest_id']
            else:
                params['until_id'] = self.__oldest_id
                json_response = self.__search_twitter(params=params)
            new_data = json_response['data']
            self.__raw_data += new_data
        self.__raw_data=self.__raw_data[:amount]
        return True

    def fetch(self):
        if len(self.__raw_data) == 0:
            return False
        else:
            return self.__raw_data

    def persist(self, path, mode = 'w'):
        with open(path, mode) as target:
            target.write(json.dumps(self.__raw_data, indent=4, sort_keys=True))

    def __search_twitter(self, params):
        if self.__token is None or self.__token == '':
            return false
        headers = {'Authorization': f'Bearer {self.__token}'}
        url = 'https://api.twitter.com/2/tweets/search/recent'
        response = requests.request('GET', url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()
