class Likert:
    expertise = {1: "1 - No Exposure", 2: "2 - Beginner", 3:"3 - Beginner / Intermediate", 4:"4 - Intermediate",5: "5 - Expert"}
    agreement = {1: "Strongly Disagree", 2: "Disagree", 3:"Neutral", 4:"Agree",5: "Strongly Agree"}
    geog =      {"Never": "Not Interested", "Hard": "Inconvenient", "Easy": "Convenient"}

    TYPE_EXPERTISE = 0
    TYPE_AGREEMENT = 1
    TYPE_GEOG      = 2
    TYPE = {TYPE_EXPERTISE : expertise, TYPE_AGREEMENT : agreement, TYPE_GEOG: geog}

    def __init__(self,type):
        assert(type in self.TYPE)
        self.type = type
        self.data = {}

    def print_string(self):
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
        if level not in self.data:
            self.data[level] = []
        self.data[level].append(app)

    def get_at_level(self,level):
        if level in self.data:
            return self.data[level]
        else:
            return None
