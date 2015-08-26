"""
Holds the survey data about a User (with help from the Likert class)
The user_id must correlate with the Meetup id for the user
"""

from likert import Likert

class User:
    def __init__(self, user_id):
        """The user_id must correlate with the Meetup id for the user"""
        self.user_id = user_id
        self.name = ""
        self.career_stage = ""
        self.broad_skills = Likert(Likert.TYPE_EXPERTISE)
        self.geogs = Likert(Likert.TYPE_GEOG)
        self.gender = ""
        self.skills = Likert(Likert.TYPE_EXPERTISE)
        self.software = []  ## These help me improve the survey and hold events of interest to you
        self.methods = Likert(Likert.TYPE_EXPERTISE)
        self.analysis = []  ## These help me improve the survey and hold events of interest to you
        self.industry = []  ## These help me improve the survey and hold events of interest to you
        self.prefs = Likert(Likert.TYPE_AGREEMENT)

    def __repr__(self):
#        self.to_string()
        return "User " + str(self.user_id) + " " + self.name

    def to_string(self):
        """Prints out the user info"""
        def print_likert(d,text):
            for x in d.get_levels():
                print text, x, d.get_at_level(x)
        def print_dict(d,text):
            for x in d:
                print text, x, d[x]
        def print_geog(d, text):
            return d.print_geog(text)
        print "User ID:",self.user_id,"Name:",self.name, "Gender:", self.gender
        print "Career Stage:",self.career_stage
        print_likert(self.broad_skills, "Broad Skills:")
        print_likert(self.geogs, "Geographies:")
        print_likert(self.skills, "Skills:")
        print "Software:", self.software
        print_likert(self.methods, "Methods:")
        print "Analysis:",self.analysis
        print "Industry:",self.industry
        print_likert(self.prefs, "Prefs:")
        return