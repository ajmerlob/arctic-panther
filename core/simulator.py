__author__="Aaron"

import math
import sys
import random

from user import User
from likert import Likert
import names

class Simulator():
    """Simulates users with filled out survey data.

    Can be called deterministically.
    Needs to be updated with changes to User model.
    """
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
        """Initialize Simulator and set users to empty set"""
        self.users = set([])

    def get_users(self):
        """Return set of simulated users"""
        return self.users

    def clear_users(self):
        self.users = set([])

    def simulate(self, num_users,seed = random.randint(0,1000000)):
        """Simulate a number of new users

        Multiple calls to simulate will continue to grow the set

        Keyword Arguments:
        num_users -- the number of users to be simulated
        seed -- (optional) a random seed for deterministic calling
        """
        ## Sets the random seed (deterministic if specified as arg)
        random.seed(seed)

        ## Calculates the set of unused ids
        possible_ids = set(range(9000000))
        pre_existing_ids = set([user.user_id for user in self.users])
        unused_ids = list(possible_ids - pre_existing_ids)

        ## Draws a set of non-overlapping unique ids for
        ## the simulated users
        user_ids = random.sample(unused_ids,num_users)

        ## Simulates a user for each user_id, and adds
        ## to the set of users
        for user_id in user_ids:
            self.users.add(self.__simulate_one(user_id))

    def __simulate_one(self,user_id):
        """Simulate a single user given a user id"""
        def get_weighted_choice(choices_dict):
            """Return an arbitrary attribute given the appropriate choice proportions"""
            ## Thanks to Maxime for this algo
            list_of_choices = [k for k in choices_dict for dummy in range(choices_dict[k])]
            return random.choice(list_of_choices)

        def get_nested_weighted_choice(likert_dict,likert_type):
            """Return a likert with arbitrary attributes given nested choice proportions

            Some of the attributes have a nested structure, in that
            the top level attribute has several sub-levels.  This
            function iterates over the second level attributes
            """
            likert = Likert(likert_type)
            for app in likert_dict:
                random_level = get_weighted_choice(likert_dict[app])
                likert.append_at_level(random_level, app)
            return likert

        ## Create the User from the user_id
        user = User(user_id)
        ## Assign user a realistic fake name
        user.name = self.__get_unused_name()
        ## Assign attributes based on the proportions of responses
        ## specified by the class variables above
        user.career_stage = get_weighted_choice(Simulator.CAREER_STAGES)
        user.gender = get_weighted_choice(Simulator.GENDERS)
        user.broad_skills = get_nested_weighted_choice(Simulator.BROAD_SKILLS,Likert.TYPE_EXPERTISE)
        user.geogs = get_nested_weighted_choice(Simulator.GEOGS,Likert.TYPE_GEOG)
        user.skills = get_nested_weighted_choice(Simulator.SKILLS,Likert.TYPE_EXPERTISE)
        user.methods = get_nested_weighted_choice(Simulator.METHODS,Likert.TYPE_EXPERTISE)
        user.prefs = get_nested_weighted_choice(Simulator.PREFS,Likert.TYPE_AGREEMENT)

        return user

    def __get_unused_name(self):
        used_names = set([user.name for user in self.users])
        while True:
            name = names.get_full_name()
            if name not in used_names:
                return name
