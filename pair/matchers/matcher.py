import random as rand
from abc import abstractmethod
#! /usr/bin/python

__author__="Aaron"
__date__ ="$Aug 25, 2015 7:39:12 PM$"

from abc import ABCMeta, abstractmethod

class Matcher(object):
    """Defines the API for parsers that grab data from external sources"""
    __metaclass__ = ABCMeta

    def __init__(self, users, seed=rand.randint(100000,999999999)):
        """Initialize a Matcher

        Users are the initial set of users with attributes

        Potential pairs hold a dictionary with the keys being
        each user, and the values being the list of all users
        with whom the key user could potentially be paired

        Match results are a set of tuples (user1, user2) holding the
        algorithm's recommendations for matches.  Users should
        not be listed more than once in the entire set of tuples

        Seed for Random can be chosen for deterministic, reproducable results
        """
        self.users = users
        self.potential_pairs = {}
        self.match_results = set([])
        self.random = rand
        self.random.seed(seed)

    def get_user_by_id(self,user_id):
        """Reverse lookup a user by id from self.users"""
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

#    def get_potential_pairs(self):
#        return self.potential_pairs

    def get_unmatched(self):
        """Return users that weren't matched in the best matches."""
        unmatched_users = set([])
        for user in self.users:
            if user.user_id not in self.potential_pairs:
                unmatched_users.add(user)
        return unmatched_users

    @abstractmethod
    def get_best_matches(self):
        """Return the best matches per algo."""
        raise NotImplementedError()