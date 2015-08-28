__author__="Aaron"

class Likert:
    """A dictionary of lists - holding survey data.

    This class holds survey data in a dictionary
    Keys are the levels
    Values are lists of questions with a response at that level
    For example, geog data might be a dictionary like:
    {"Never":["Place 1","Place 3"], "Hard":["Place 4"], "Easy":["Place 2","Place 5"]}
    When defining a Likert, you should use the static TYPEs like Likert.TYPE_GEOG
    """
    
    ## These TYPE dictionaries hold the mapping between my internal name and the name in the survey text
    expertise = {1: "1 - No Exposure", 2: "2 - Beginner", 3:"3 - Beginner / Intermediate", 4:"4 - Intermediate",5: "5 - Expert"}
    agreement = {1: "Strongly Disagree", 2: "Disagree", 3:"Neutral", 4:"Agree",5: "Strongly Agree"}
    geog =      {"Never": "Not Interested", "Hard": "Inconvenient", "Easy": "Convenient"}

    ## These are used to assign a type to a Likert (like Likert(Likert.TYPE_EXPERTISE))
    TYPE_EXPERTISE = 0
    TYPE_AGREEMENT = 1
    TYPE_GEOG      = 2

    ## TYPE is a dictionary that converts from a type constant to a
    ## dictionary mapping internal names to external names
    TYPE = {TYPE_EXPERTISE : expertise, TYPE_AGREEMENT : agreement, TYPE_GEOG: geog}

    def __init__(self,type):
        """This class holds a dictionary of data - keys are the keys from the TYPE dict - values are lists"""
        ## For example, geog data ~= {"Never":["Place 1","Place 3"], "Hard":["Place 4"], "Easy":["Place 2","Place 5"]}
        assert(type in self.TYPE)
        self.type = type
        self.data = {}
        for level in Likert.TYPE[type]:
            self.data[level] = []

    def get_print_string(self):
        """Returns printable copy of data held at each level"""
        return_string = ""
        for x in self.data:
            if len(self.data[x]) > 0:
                return_string += x
                return_string += " : ["
                return_string += ",".join(self.data[x])
                return_string += "] , "
        return return_string[:-3]

    def txt(self,r):
        """Return external name given internal name (and this instance's type)"""
        return self.TYPE[self.type][r]

    def get_levels(self):
        """Return list of all external names (given this instance's type)"""
        return list(self.TYPE[self.type].keys())

    def get_level_names(self):
        """Return map of all external names (given this instance's type)"""
        return map(self.txt,self.get_levels())

    def append_at_level(self,level,app):
        """Add data to a level using this method - don't mess with the data directly"""
        if level not in Likert.TYPE[self.type]:
            self.data[level] = []
        self.data[level].append(app)

    def get_at_level(self,level):
        """Get the list of data at a level using the internal representation for the level (i.e. a key in the TYPE dict)"""
        if level in self.data:
            return self.data[level]
        else:
            return None
