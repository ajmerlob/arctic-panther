import math
import sys
import os.path

from config import Config
from parse_survey import Parser
from analyze import Analyze
from simulator import Simulator

import meetup_api_client as meetup

__author__="Aaron Merlob"
__date__ ="$Mar 28, 2015 7:56:55 AM$"

conf = Config()

if conf.api_key == "" or conf.oauth_key == "" or conf.oauth_secret == "":
    print "PLEASE EDIT config.py AND ADD YOUR API KEY AND OAUTH KEY/SECRET"
    sys.exit()

class Main:
    conf = Config()

    def __init__(self):
        self.users = set ([])
        self.user_photos = {}
        self.survey_data_filename = "c:/users/aaron/desktop/survey_data.txt"

    def get_weekly_opt_ins(self,group_id):
        arg_dict = {}
        arg_dict["group_id"] = group_id

        m = meetup.Meetup(conf.api_key)
        events = m.get_events(**arg_dict).results
        opt_ins = set([])
        for x in events:
            if not "Pair Data Science" in x.name:
                print "Skipped",x.name
                continue
            else:
                print "Calculating Pairs -", x.name
            rsvps = x.get_rsvps(m)
            try:
                for rsvp in rsvps.results:
                    opt_ins.add(rsvp.member["member_id"])
                    try:
                        self.user_photos[rsvp.member["member_id"]] = rsvp.member_photo["highres_link"]
                    except:
                        self.user_photos[rsvp.member["member_id"]] = None
            except:
                print "didn't get 'em"

        return opt_ins

    def get_users(self,group_id):
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
            opt_ins = self.get_weekly_opt_ins(group_id)

            ## Filter to just opted-in users
            self.users = set([i for i in all_users if int(i.user_id) in opt_ins])

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
        analyze.get_best_matches()
        potential_pairs = analyze.get_potential_pairs()

    #    for user in users:
    #        if user.user_id not in potential_pairs:
    #            print "No Matches for:", user.name
    #        print user.user_id,user.name

if __name__ == "__main__":
    for group_id in Config.groups:
        main = Main()
        main.get_users(group_id)
        main.analyze_pairs()