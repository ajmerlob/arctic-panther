"""
This class grabs survey data from the surveymonkey API
and stores it somewhere
"""
__author__="Aaron"
__date__ ="$Aug 23, 2015 1:06:52 PM$"

import requests
import json
from config import Config


class SurveyAPI:
    """A class that grabs survey data from the surveymonkey API"""
    

if __name__ == "__main__":
    ## Configure the client
    conf = Config()
    access_token = conf.surveymonkey_token
    api_key = conf.surveymonkey_api_key

    client = requests.session()
    client.headers = {
        "Authorization": "bearer %s" % access_token,
        "Content-Type": "application/json"
        }
    client.params = {
        "api_key": api_key
        }
    
    ## Use the configured client

    HOST = "https://api.surveymonkey.net"
    SURVEY_LIST_ENDPOINT = "/v2/surveys/get_survey_list"

    uri = "%s%s" % (HOST, SURVEY_LIST_ENDPOINT)

    data = {}
    response = client.post(uri, data=json.dumps(data))
    response_json = response.json()
    survey_list = response_json["data"]["surveys"]
    print survey_list