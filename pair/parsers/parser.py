from abc import abstractmethod
#! /usr/bin/python

__author__="Aaron"
__date__ ="$Aug 25, 2015 7:39:12 PM$"

from abc import ABCMeta, abstractmethod

class Parser:
    """Defines the API for parsers that grab data from external sources"""
    __metaclass__ = ABCMeta

    def __init__(self):
        self.users = set([])

    @abstractmethod
    def parse(self):
        """Call this to have the parser grab the external data"""
        raise NotImplementedError()

    def get_users(self):
        print "Total Num Users:", len(self.users)
        return self.users

