import main
import math
import sys
import os.path

from config import Config
from parse_survey import Parser
from analyze import Analyze
from simulator import Simulator
from messages import Message
from text import Text

import meetup_api_client as meetup

__author__="Aaron Merlob"
__date__ ="$Mar 28, 2015 7:56:55 AM$"

conf = Config()

if conf.api_key == "" or conf.oauth_key == "" or conf.oauth_secret == "":
    print "PLEASE EDIT config.py AND ADD YOUR API KEY AND OAUTH KEY/SECRET"
    sys.exit()

class Main:
    conf = Config()

    def __init__(self, group_id):
        self.group_id = group_id
        self.users = set ([])
        self.user_photos = {}
        self.survey_data_filename = "c:/users/aaron/desktop/survey_data.txt"
        self.meetup_client = meetup.Meetup(conf.api_key)
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

    def get_users(self):
        ## Read in the survey data or simulate new data
        if os.path.isfile(self.survey_data_filename):
            parser = Parser(self.survey_data_filename)
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
            self.users = set([i for i in all_users if int(i.user_id) in opt_ins])
            

            ## Filter out Aaron, as desired
            if not self.aaron_matches:
                for u in set(self.users):
                    if u.user_id in ["87429312","185839888"]:
                        self.users.remove(u)
                        break

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
        ## This is a very basic algorithm that only makes use of geography
        ## TODO: Update algorithm to incorporate more than geography
        analyze = Analyze(self.users)
        analyze.analyze_easy_potentials()
        match_results = analyze.get_best_matches()
        potential_pairs = analyze.get_potential_pairs()

        return match_results

    #    for user in users:
    #        if user.user_id not in potential_pairs:
    #            print "No Matches for:", user.name
    #        print user.user_id,user.name

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
        main.send_pair_assignment_messages("May 29th", pairs,False)