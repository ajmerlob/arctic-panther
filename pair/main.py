import main
import math
import sys
import os.path

from core.config import Config
from parsers.text_parser import TextParser
from parsers.api_parser import APIParser
from analyze import Analyze
from core.simulator import Simulator
from messages import Message
from text import Text

import meetup_api_client as meetup

__author__="Aaron Merlob"
__date__ ="$Mar 28, 2015 7:56:55 AM$"

conf = Config()

if conf.meetup_api_key == "" or conf.meetup_oauth_key == "" or conf.meetup_oauth_secret == "":
    print "PLEASE EDIT config.py AND ADD YOUR API KEY AND OAUTH KEY/SECRET"
    sys.exit()

class Main:
    conf = Config()

    def __init__(self, group_id):
        self.group_id = group_id
        self.users = set ([])
        self.user_photos = {}
        self.survey_data_filename = "c:/users/aaron/desktop/survey_data.txt"
        self.survey_api_survey_id = u"67951656"
        self.meetup_client = meetup.Meetup(conf.meetup_api_key)
        self.message_client = Message()
        self.aaron_matches = False

    def get_weekly_opt_ins(self):
        arg_dict = {}
        arg_dict["group_id"] = self.group_id

        events = self.meetup_client.get_events(**arg_dict).results
        opt_ins = {}
        for x in events:
            if not "Pair Data Science" in x.name:
                print "Skipped",x.name
                continue
            else:
                print "Calculating Pairs -", x.name
            rsvps = x.get_rsvps(self.meetup_client)
            try:
                for rsvp in rsvps.results:
                    opt_ins[rsvp.member["member_id"]] = rsvp.member["name"]
                    try:
                        self.user_photos[rsvp.member["member_id"]] = rsvp.member_photo["highres_link"]
                    except:
                        self.user_photos[rsvp.member["member_id"]] = None
            except:
                print "didn't get 'em"

        return opt_ins

    def get_users_parser(self,parser_type,survey_unique_identifier):
        parser = parser_type(survey_unique_identifier)
        if not parser.parse():
            return None
        all_users = parser.get_users()

        ## Remember all previous matches
        ## TODO: Update analyze function to exclude previous pairs (Don't want the same person each week)
        ## TODO: Persist to a database instead of a file
        previous_pairs = set([])
        previous_pairs_filename = "c:/users/aaron/desktop/previous_pairs.txt"
        if os.path.isfile(previous_pairs_filename):
            with open (previous_pairs_filename) as prev:
                for line in prev:
                    usera, userb = line.strip().split(",")
                    previous_pairs.add((usera,userb))
                    previous_pairs.add((userb,usera))

        ## Grabs the list of people interested in being matched this week
        ## From the Meetup event API
        opt_ins = self.get_weekly_opt_ins()

        missing_surveys = set([str(u) for u in opt_ins.keys()]).difference(set([str(u.user_id) for u in all_users]))
        print "Missing Surveys", len(missing_surveys), missing_surveys

        ## Filter to just opted-in users
        print "Pre-filter # users", len(all_users)
        users = set([i for i in all_users if int(i.user_id) in opt_ins])

        ## Filter out Aaron, as desired
        if not self.aaron_matches:
            for u in set(users):
                if u.user_id in ["87429312","185839888"]:
                    users.remove(u)
                    break
        print "Post-filter # users", len(users)

        return users

    def get_users(self):
        ## Read in the survey data or simulate new data
        self.users = self.get_users_parser(APIParser, self.survey_api_survey_id)
        print self.users
        if self.users is None:
            if os.path.isfile(self.survey_data_filename):
                self.users = self.get_users_parser(TextParser, self.survey_data_filename)
            else:
                print "Simulating data"
                ## Simulate some number of survey responses
                sim = Simulator()
                sim.simulate(200) ## By adding a seed parameter, you can have reproducible sims
                self.users = sim.get_users()

    #    ## Print some summaries
    #    for user in users:
    #        user.to_string()

        # Print some descriptive stats
        print "# Users", len(self.users), [u.name for u in self.users]


    def analyze_pairs(self):
        # Analyze pairs
        ## GeogMatcher is a very basic algorithm that only makes use of geography
        ## TODO: Update algorithm to incorporate more than geography
        analyze = GeogMatcher(self.users)
        match_results = analyze.get_best_matches()

        return match_results

    

    def send_missing_survey_messages(self,debug=True):
        msg_no_name = Text(self.group_id).take_survey

        opt_ins = self.get_weekly_opt_ins()
        user_ids = [u.user_id for u in self.users]

        for opt_in in opt_ins:
            if str(opt_in) not in user_ids:
                msg = msg_no_name % (opt_ins[opt_in])
                if debug:
                    print msg
                else:
                    print "Starting Message:",msg.split("\n")[0]
                    print self.message_client.send(msg,str(opt_in))
                    print msg

    def send_pair_assignment_messages(self,finish_date,pairs,debug=True):
        msg_no_names = Text(self.group_id).assign_pair
        if raw_input('Continue Sending Messages - T or F : ') != "T":
            return
        for pair in pairs:
            msg = msg_no_names % (finish_date,pair[0].name,pair[1].name)
            if raw_input("Send Pair %s -- %s -- T or F: " % (pair[0].name,pair[1].name)) != "T":
                print "Skipping %s -- %s" % (pair[0].name,pair[1].name)
                continue
            else:
                if debug:
                    print "DEBUG ONLY - NOT ACTUALLY SENDING"
                    print msg
                else:
                    self.message_client.send2(msg,[str(p.user_id) for p in pair])


if __name__ == "__main__":
    spam_missing_surveys = False


    for group_id in Config.groups:
        main = Main(group_id)
        main.get_users()
        if spam_missing_surveys:
            main.send_missing_survey_messages()
        pairs = main.analyze_pairs()
#        main.send_pair_assignment_messages("May 29th", pairs,False)