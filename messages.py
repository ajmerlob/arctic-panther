import requests
from bs4 import BeautifulSoup as soup
import random
import os
import urllib
import subprocess

class Message:

    endpoint = 'https://secure.meetup.com'

    authEndpoint = 'login'

    newMessageEndpoint = 'muapi/self/conversations/'

    session = False

    token = False

    #sourced from https://techblog.willshouse.com/2012/01/03/most-common-user-agents/
    userAgents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.3.18 (KHTML, like Gecko) Version/8.0.3 Safari/600.3.18', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36']

    userAgent = False

    #authFile should be a file where your username and password are stored, separated by a newline
    def __init__(self, authFile="/tmp/meetup.auth"):
        if not os.path.isfile(authFile):
            raise Exception('authFile must exist!')

        self.authFile = authFile
        self.userAgent = random.choice(self.userAgents)
        self.session = requests.session()
        self.token = self.get_auth_token()
        login = self.login()

        if not login:
            raise Exception('Login failed.')

    def get_auth_token(self):
        url = self.endpoint + '/' + self.authEndpoint
        res = self.session.get(url)
        dom = soup(res.text)
        token = dom.find('input', {'name': 'token'}).get('value')
        self.token = token
        return token

    def get_headers(self, referer):
        headers = {
            'origin': 'https://secure.meetup.com',
            'accept-language': 'en-US,en;q=0.8',
            'user-agent': self.userAgent,
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'referer': referer
        }

        if len(self.session.cookies) == 0:
            headers['cookie'] = 'MEETUP_CSRF='+self.token+'; MEETUP_MEMBER="id=0";'
        else:
            headers['csrf-token'] = self.token

        return headers

    def login(self):
        headers = self.get_headers('https://secure.meetup.com/login/')

        url = self.endpoint + '/' + self.authEndpoint

        auth = open(self.authFile).read().split('\n')

        data = 'email='+auth[0]+'&password='+auth[1]+'&token='+self.token+'&op=login'

        res = self.session.post(url, headers=headers, data=data, allow_redirects=False)

        return res.status_code == 302

    
    def send(self, text, memberid):
        url = self.endpoint + '/' + self.newMessageEndpoint
        data = "title=&text="+text+"&member="+memberid+"&conversation_kind=one_one&photo_host=secure"
        res = self.session.post(url, headers=self.get_headers('https://secure.meetup.com/messages/?new_convo=true'), data=data, allow_redirects=False)
        return res.status_code == 200
