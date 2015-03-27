import math
import sys
import os.path


from parse_survey import Parser
from analyze import Analyze
from simulator import Simulator

__author__="Aaron Merlob"
__date__ ="$Mar 28, 2015 7:56:55 AM$"

if __name__ == "__main__":
    ## Read in the survey data or simulate new data
    all_users_filename = "c:/users/aaron/desktop/survey_data_boston.txt"
    if os.path.isfile(all_users_filename):
        parser = Parser(all_users_filename)
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

        ## TODO: Grab list of opt-ins from the current Meetup event using API
        ## Grabs the list of people interested in being matched this week
        opt_ins = set([])
        opt_ins_filename = "c:/users/aaron/desktop/weekly_opt_ins.txt"
        if os.path.isfile(opt_ins_filename):
            with open (opt_ins_filename) as opt:
                for line in opt:
                    opt_ins.add(line.strip())
        ## If that list doesn't exist, assign everyone with survey data
        else:
            opt_ins = set([u.user_id for u in all_users])

        ## Filter to just opted-in users
        users = set([])
        for user in all_users:
            if user.user_id in opt_ins:
                users.add(user)
                
    else:
        ## Simulate some number of survey responses
        sim = Simulator()
        sim.simulate(200) ## By adding a seed parameter, you can have reproducible sims
        users = sim.get_users()

#    ## Print some summaries
#    for user in users:
#        user.to_string()

    # Print some descriptive stats
    print "# Users", len(users)

    # Analyze pairs
    ## This is a very basic algorithm that only makes use of geography
    ## TODO: Update algorithm to incorporate more than geography
    analyze = Analyze(users)
    analyze.analyze_easy_potentials()
    analyze.get_best_matches()
    potential_pairs = analyze.get_potential_pairs()

#    for user in users:
#        if user.user_id not in potential_pairs:
#            print "No Matches for:", user.name
#        print user.user_id,user.name