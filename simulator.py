import math
import sys
import random

from user import User
from likert import Likert
import names

#class User:
#    def __init__(self, user_id):
#        self.user_id = user_id
#        self.name = ""
#        self.career_stage = ""
#        self.broad_skills = Likert(Likert.TYPE_EXPERTISE)
#        self.geogs = Likert(Likert.TYPE_GEOG)
#        self.gender = ""
#        self.skills = Likert(Likert.TYPE_EXPERTISE)
#        self.software = []  ## These help me improve the survey and hold events of interest to you
#        self.methods = Likert(Likert.TYPE_EXPERTISE)
#        self.analysis = []  ## These help me improve the survey and hold events of interest to you
#        self.industry = []  ## These help me improve the survey and hold events of interest to you
#        self.prefs = Likert(Likert.TYPE_AGREEMENT)

class Simulator():
    ## These are the simulated relative proportions of each response
    ## They don't need to add to 100, but they do need to be integers
    CAREER_STAGES = {"Student": 10, "Entry": 15, "Early":25, "Middle": 40, "Late": 10}
    GENDERS = {"Male": 80, "Female": 13, "Female - Female Matches Only": 4, "Other":3 }
    BROAD_SKILLS = {"Top Level Skill A": {1: 40, 2: 20, 3: 10, 4: 20, 5: 10 },
                    "Top Level Skill B": {1: 40, 2: 20, 3: 10, 4: 20, 5: 10 },
                    "Top Level Skill C": {1: 40, 2: 20, 3: 10, 4: 20, 5: 10 },
                    "Top Level Skill D": {1: 60, 2: 5 , 3: 0 , 4:  0, 5: 35 },
                    "Top Level Skill E": {1: 70, 2: 25, 3:  5, 4: 0 , 5: 0  },
                    "Top Level Skill Z": {1: 40, 2: 20, 3: 10, 4: 20, 5: 10 }}
    SKILLS =       {"Skill A": {1: 40, 2: 20, 3: 10, 4: 20, 5: 10 },
                    "Skill B": {1: 40, 2: 20, 3: 10, 4: 20, 5: 10 },
                    "Skill C": {1: 40, 2: 20, 3: 10, 4: 20, 5: 10 },
                    "Skill D": {1: 60, 2: 5 , 3: 0 , 4:  0, 5: 35 },
                    "Skill E": {1: 70, 2: 25, 3:  5, 4: 0 , 5: 0  },
                    "Skill Z": {1: 40, 2: 20, 3: 10, 4: 20, 5: 10 }}
    METHODS =      {"Method A": {1: 40, 2: 20, 3: 10, 4: 20, 5: 10 },
                    "Method B": {1: 40, 2: 20, 3: 10, 4: 20, 5: 10 },
                    "Method C": {1: 40, 2: 20, 3: 10, 4: 20, 5: 10 },
                    "Method D": {1: 60, 2: 5 , 3: 0 , 4:  0, 5: 35 },
                    "Method E": {1: 70, 2: 25, 3:  5, 4: 0 , 5: 0  },
                    "Method Z": {1: 40, 2: 20, 3: 10, 4: 20, 5: 10 }}
    PREFS =        {"Industry":         {1: 40, 2: 20, 3: 10, 4: 20, 5: 10 },
                    "I_mentor":         {1: 40, 2: 20, 3: 10, 4: 20, 5: 10 },
                    "At_skill_level":   {1: 40, 2: 20, 3: 10, 4: 20, 5: 10 },
                    "Mentor_me":        {1: 60, 2: 5 , 3: 0 , 4:  0, 5: 35 },
                    "Similar":          {1: 70, 2: 25, 3:  5, 4: 0 , 5: 0  },
                    "Different":        {1: 40, 2: 20, 3: 10, 4: 20, 5: 10 }}
    GEOGS =        {"North":    {"Never": 50, "Hard": 30, "Easy": 20},
                    "South":    {"Never": 50, "Hard": 30, "Easy": 20},
                    "East":     {"Never": 50, "Hard": 30, "Easy": 20},
                    "West":     {"Never": 50, "Hard": 30, "Easy": 20},
                    "Middle":   {"Never": 15, "Hard": 30, "Easy": 55},
                    "Outside":  {"Never": 90, "Hard": 7 , "Easy": 3 }}


    def __init__(self):
        self.users = set([])

    def get_users(self):
        return self.users

    def simulate(self, num_users,seed = random.randint(0,1000000)):
        random.seed(seed)
        user_ids = random.sample(range(9000000),num_users)
        for user_id in user_ids:
            self.users.add(self.simulate_one(user_id))

    def simulate_one(self,user_id):
        def get_weighted_choice(choices_dict):
            ## Thanks to Maxime for this algo
            list_of_choices = [k for k in choices_dict for dummy in range(choices_dict[k])]
            return random.choice(list_of_choices)

        def get_nested_weighted_choice(likert_dict,likert_type):
            likert = Likert(likert_type)
            for app in likert_dict:
                random_level = get_weighted_choice(likert_dict[app])
                likert.append_at_level(random_level, app)
            return likert

        user = User(user_id)
        user.name = names.get_full_name()
        user.career_stage = get_weighted_choice(Simulator.CAREER_STAGES)
        user.gender = get_weighted_choice(Simulator.GENDERS)
        user.broad_skills = get_nested_weighted_choice(Simulator.BROAD_SKILLS,Likert.TYPE_EXPERTISE)
        user.geogs = get_nested_weighted_choice(Simulator.GEOGS,Likert.TYPE_GEOG)
        user.skills = get_nested_weighted_choice(Simulator.SKILLS,Likert.TYPE_EXPERTISE)
        user.methods = get_nested_weighted_choice(Simulator.METHODS,Likert.TYPE_EXPERTISE)
        user.prefs = get_nested_weighted_choice(Simulator.PREFS,Likert.TYPE_AGREEMENT)

        return user