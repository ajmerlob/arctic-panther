"""
This class grabs survey data from the surveymonkey API
and stores it somewhere
"""
__author__="Aaron"
__date__ ="$Aug 23, 2015 1:06:52 PM$"

import requests
import json
import time
import cPickle as pickle
import sys
from config import Config
from user import User
from parsers.parser import Parser

HOST = "https://api.surveymonkey.net"
SURVEY_LIST_ENDPOINT = "/v2/surveys/get_survey_list"
SURVEY_DETAILS_ENDPOINT = "/v2/surveys/get_survey_details"
SURVEY_RESPONDENTS_ENDPOINT = "/v2/surveys/get_respondent_list"
SURVEY_RESPONSES_ENDPOINT = "/v2/surveys/get_responses"

class APIParser(Parser):
    def __init__(self,survey_id):
        print "initing api parser"
        self.users = set([])
        self.conf = Config()
        self.respondent_id_to_user = {}
        self.survey_id = survey_id
        access_token = self.conf.surveymonkey_token
        api_key = self.conf.surveymonkey_api_key

        self.client = requests.session()
        self.client.headers = {
            "Authorization": "bearer %s" % access_token,
            "Content-Type": "application/json"
            }
        self.client.params = {
            "api_key": api_key
            }

    def get_survey_details(self,survey_id):
        uri = "%s%s" % (HOST, SURVEY_DETAILS_ENDPOINT)

        data = {}
        data["survey_id"] = str(survey_id)

        response = self.client.post(uri, data=json.dumps(data))
        response_json = response.json()
        time.sleep(2)
        return response_json
#        pages = response_json["data"]["pages"]
#        for page in pages:
#            questions = page["questions"]
#            for question in questions:
#                position = question["position"]
#                heading = question["heading"]
#                question_id = question["question_id"]
#                print survey_id, question_id, position, heading


#        print survey_id, survey_list_dict
#        survey_id_list = [s.values()[0] for s in survey_list_dict]
#        return survey_id_list

    def get_survey_list(self):
        uri = "%s%s" % (HOST, SURVEY_LIST_ENDPOINT)

        data = {}
        response = self.client.post(uri, data=json.dumps(data))
        response_json = response.json()
        time.sleep(2)
#        print response_json
        survey_list_dict = response_json["data"]["surveys"]
        survey_id_list = [s.values()[0] for s in survey_list_dict]
        return survey_id_list

    def get_respondents_list(self,survey_id):
        uri = "%s%s" % (HOST, SURVEY_RESPONDENTS_ENDPOINT)

        data = {}
        data["survey_id"] = str(survey_id)
        response = self.client.post(uri, data=json.dumps(data))
        response_json = response.json()
        time.sleep(2)
#        print response_json
        respondents_dict = response_json["data"]["respondents"]
        respondents_id_list = [s.values()[0] for s in respondents_dict]
        return respondents_id_list

    def get_responses(self,survey_id,respondent_id_array):
        uri = "%s%s" % (HOST, SURVEY_RESPONSES_ENDPOINT)

        data = {}
        data["survey_id"] = str(survey_id)
        data["respondent_ids"] = respondent_id_array
        response = self.client.post(uri, data=json.dumps(data))
        response_json = response.json()
        time.sleep(2)
        response_dict = response_json["data"]
        return response_dict
#        respondents_id_list = [s.values()[0] for s in respondents_dict]
#        return respondents_id_list

    """A class that grabs survey data from the surveymonkey API"""

    def parse_design(self,details):
        ## Start with details about a survey
        ## Objective: Create a lookup from
        ## (question_id, answer_id) to row_text

        pages = details["data"]["pages"]
        answer_text_dict = {}
        for page in pages:
            questions = page["questions"]
            for question in questions:
                question_id = question["question_id"]
                answers = question["answers"]
                for answer in answers:
                    answer_id = answer["answer_id"]
                    text = answer["text"]
#                    print question_id, answer_id, text
#                    if question_id not in question_answer_text_dict:
#                        question_answer_text_dict[question_id] = {}
#                    question_answer_text_dict[question_id][answer_id] = text
                    answer_text_dict[answer_id] = text
#        print question_answer_text_dict
        return answer_text_dict

    def get_agree(self,agreement_text):
        if "Strongly Agree" in agreement_text:
            return 5
        elif "Strongly Disagree" in agreement_text:
            return 1
        elif "Disagree" in agreement_text:
            return 2
        elif "Neutral" in agreement_text:
            return 3
        elif "Agree" in agreement_text:
            return 4
        else:
            return -999

    def answer_q(self,respondent_id,question_id,answer_text_dict,answers):
#        print "answers",answers
        for answer in answers:
#            print answer.keys()

            if respondent_id in self.respondent_id_to_user:
                current_user = self.respondent_id_to_user[respondent_id]

            answer_row = answer['row']
            if answer["row"] == u"0":
                question_text = "Other"
            else:
                question_text = answer_text_dict[answer_row]

            answer_text = None
            answer_col = None

            if 'text' in answer:
                answer_text = answer['text']
            if 'col' in answer:
                answer_col = answer['col']
                answer_text = answer_text_dict[answer_col]

            if question_id == 1:
                if "What is your DS ProD member number?" in question_text:
                    user_id = answer_text
                    for x_user in self.users:
                        if x_user.user_id == user_id:
                            print "SOMEONE TOOK THIS TWICE", user_id
                            exit
                    current_user = User(user_id)
                    self.users.add(current_user)
                    self.respondent_id_to_user[respondent_id] = current_user
                elif "what you put on Meetup" in question_text:
                    current_user.name = answer_text
            elif question_id == 2:
                current_user.career_stage = question_text
            elif question_id == 3:
                for level in current_user.methods.get_levels():
                    level_txt = current_user.methods.txt(level)
                    if level_txt in answer_text:
                        skill = question_text
                        current_user.broad_skills.append_at_level(level, skill)
            elif question_id == 4:
                for level in current_user.geogs.get_levels():
                    level_txt = current_user.geogs.txt(level)
                    geog = question_text
                    if level_txt in answer_text:
                        current_user.geogs.append_at_level(level,geog)
                if question_text == "Other":
                    current_user.geogs.append_at_level("Other", question_text)
            elif question_id == 5:
                current_user.gender = question_text
            elif question_id == 6:
                for level in current_user.skills.get_levels():
                    level_txt = current_user.skills.txt(level)
                    if level_txt in answer_text:
                        skill = question_text
                        current_user.skills.append_at_level(level,skill)
            elif question_id == 7:
                package = answer_text
                current_user.software.append(package)
            elif question_id == 8:
                for level in current_user.methods.get_levels():
                    level_txt = current_user.methods.txt(level)
                    if level_txt in answer_text:
                        skill = question_text
                        current_user.methods.append_at_level(level, skill)
            elif question_id == 9:
                if "Analysis" in question_text:
                    current_user.analysis.append(answer_text)
                elif "Industry" in question_text:
                    current_user.industry.append(answer_text)
            elif question_id == 10:
                if "In my industry" in question_text:
                    current_user.prefs.append_at_level(self.get_agree(answer_text),"industry")
                if "That I can mentor" in question_text:
                    current_user.prefs.append_at_level(self.get_agree(answer_text),"i_mentor")
                if "At my skill level" in question_text:
                    current_user.prefs.append_at_level(self.get_agree(answer_text),"at_skill_level")
                if "That will mentor me" in question_text:
                    current_user.prefs.append_at_level(self.get_agree(answer_text),"mentor_me")
                if "That are quite similar to me" in question_text:
                    current_user.prefs.append_at_level(self.get_agree(answer_text),"similar")
                if "That are quite different from me" in question_text:
                    current_user.prefs.append_at_level(self.get_agree(answer_text),"different")

    def parse_responses(self,design,responses):
        for response in responses:

            question_answer_dict = {}
            questions = response["questions"]
            respondent_id = response["respondent_id"]

            ## Load up the question_answer_dict
            for question in questions:
                question_id = question["question_id"]
                answers = question["answers"]
                question_answer_dict[question_id] = answers


            ## Interrogate the question_answer_dict
#            print conf.survey_api_ids
            for survey_name in self.conf.survey_api_ids:
                survey_data = self.conf.survey_api_ids[survey_name]
#                print survey_data
                if "question_ids" in survey_data:
                    api_id_dict = survey_data["question_ids"]
                    for current_qid_lookup in range(1, 11):
                        if current_qid_lookup not in api_id_dict:
                            print "didn't find it ", current_qid_lookup
                            continue
                        survey_qid = api_id_dict[current_qid_lookup]
                        if survey_qid not in question_answer_dict:
                            print "they skipped one", survey_qid
                            continue
                        answers = question_answer_dict[survey_qid]

#                        print "ENTERING answer loop", current_qid_lookup
                        self.answer_q(respondent_id,current_qid_lookup,design,answers)

    def get_users(self):
        print "Total Num Users:", len(self.users)
        return self.users

    def parse(self):
        survey_id = self.survey_id
        respondents_id_list = self.get_respondents_list(survey_id)
        responses = self.get_responses(survey_id, respondents_id_list)
        details = self.get_survey_details(survey_id)
        ## Send responses to be parsed
        design = self.parse_design(details)
        self.parse_responses(design,responses)
        return self.users



    def pickle_or_get_responses(self,filename):
        try:
    #        print "attempting load"
            with open(filename,'rb') as pickleload:
    #            print "opened load"
                responses = pickle.load(pickleload)
                print "loaded pickle"
        except:
            print "getting from web"
            respondents_id_list = sapi.get_respondents_list(self.survey_id)
            print respondents_id_list
            responses = sapi.get_responses(self.survey_id, respondents_id_list)

            with open(filename,'wb') as pickledump:
                pickle.dump(responses,pickledump)
        return responses

    def pickle_or_get_details(self,filename):
        try:
    #        print "attempting load"
            with open(filename,'rb') as pickleload:
    #            print "opened load"
                details = pickle.load(pickleload)
                print "loaded pickle"
        except:
            print "getting from web"
            details = sapi.get_survey_details(self.survey_id)

            with open(filename,'wb') as pickledump:
                pickle.dump(details,pickledump)
        return details




if __name__ == "__main__":
    ## Configure the client
    sapi = APIParser(u"67951656")
    responses = sapi.pickle_or_get_responses("c:/users/aaron/desktop/responses.out")
    details = sapi.pickle_or_get_details("c:/users/aaron/desktop/details{}.out".format(sapi.survey_id))

    design = sapi.parse_design(details)
    sapi.parse_responses(design,responses)


