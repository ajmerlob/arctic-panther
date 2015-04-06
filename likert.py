class Likert:
    """A dictionary of lists - holding survey data"""
    
    ## These TYPE dictionaries hold the mapping between my internal name and the name in the survey text
    expertise = {1: "1 - No Exposure", 2: "2 - Beginner", 3:"3 - Beginner / Intermediate", 4:"4 - Intermediate",5: "5 - Expert"}
    agreement = {1: "Strongly Disagree", 2: "Disagree", 3:"Neutral", 4:"Agree",5: "Strongly Agree"}
    geog =      {"Never": "Not Interested", "Hard": "Inconvenient", "Easy": "Convenient"}

    ## These are used to assign a type to a Likert (like Likert(Likert.TYPE_EXPERTISE))
    TYPE_EXPERTISE = 0
    TYPE_AGREEMENT = 1
    TYPE_GEOG      = 2
    TYPE = {TYPE_EXPERTISE : expertise, TYPE_AGREEMENT : agreement, TYPE_GEOG: geog}

    def __init__(self,type):
        """This class holds a dictionary of data - keys are the keys from the TYPE dict - values are lists"""
        ## For example, geog data ~= {"Never":["Place 1","Place 3"], "Hard":["Place 4"], "Easy":["Place 2","Place 5"]}
        assert(type in self.TYPE)
        self.type = type
        self.data = {}
        for level in Likert.TYPE[type]:
            self.data[level] = []

    def print_string(self):
        """Prints out the data it holds at each level"""
        return_string = ""
        for x in self.data:
            return_string += x
            return_string += " : ["
            return_string += ",".join(self.data[x])
            return_string += "] , "
        return return_string[:-3]

    def txt(self,r):
        return self.TYPE[self.type][r]

    def get_levels(self):
        return list(self.TYPE[self.type].keys())

    def get_level_names(self):
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
