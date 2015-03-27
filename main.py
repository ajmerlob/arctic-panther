import math
import sys
import os.path


from parse_survey import Parser
from analyze import Analyze
from simulator import Simulator

__author__="Aaron Merlob"
__date__ ="$Mar 28, 2015 7:56:55 AM$"

if __name__ == "__main__":
    all_users_filename = "c:/users/aaron/desktop/survey_data_boston.txt"
    if os.path.isfile(all_users_filename):
        parser = Parser(all_users_filename)
        users = parser.get_users()
    else:
        sim = Simulator()
        sim.simulate(200) ## By adding a seed parameter, you can have reproducible sims
        users = sim.get_users()

    previous_pairs_filename = "c:/users/aaron/desktop/previous_pairs.txt"
    if os.path.isfile(all_users_filename):
        with open (previous_pairs_filename) as prev:
            for line in prev:
                usera, userb = line.strip().split(",")

#    ## Print some summaries
#    for user in users:
#        user.to_string()

    # Print some descriptive stats
    print "# Users", len(users)

    # Analyze pairs
    analyze = Analyze(users)
    analyze.analyze_easy_potentials()
    analyze.get_best_matches()
    potential_pairs = analyze.get_potential_pairs()

#    for user in users:
#        if user.user_id not in potential_pairs:
#            print "No Matches for:", user.name
#        print user.user_id,user.name