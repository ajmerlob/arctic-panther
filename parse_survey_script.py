import math
import sys
import random

__author__="Aaron"
__date__ ="$Mar 18, 2015 9:56:55 AM$"

if __name__ == "__main__":
    pass

class Geog:
    def __init__(self):
        self.easy = set([])
        self.hard = set([])
        self.never = set([])
        self.other = ""

    def print_geog(self,text):
        print text, "Easy", self.easy
        print text, "Hard", self.hard
        print text, "Never", self.never
        print text, "Other", self.other

class Likert:
    expertise = {1: "1 - No Exposure", 2: "2 - Beginner", 3:"3 - Beginner / Intermediate", 4:"4 - Intermediate",5: "5 - Expert"}
    agreement = {1: "Strongly Disagree", 2: "Disagree", 3:"Neutral", 4:"Agree",5: "Strongly Agree"}

    TYPE_EXPERTISE = 0
    TYPE_AGREEMENT = 1
    TYPE = {TYPE_EXPERTISE : expertise, TYPE_AGREEMENT : agreement}

    def __init__(self,type):
        assert(type in self.TYPE)
        self.type = type
        self.r1 = []
        self.r2 = []
        self.r3 = []
        self.r4 = []
        self.r5 = []

    def txt(self,r):
        return self.TYPE[self.type][r]

    def get_levels(self):
        return [1,2,3,4,5]

    def get_level_names(self):
        return map(self.txt,self.get_levels())

    def append_at_level(self,level,app):
        level_map = {1: self.r1, 2:self.r2, 3:self.r3, 4:self.r4, 5:self.r5}
        level_map[level].append(app)

    def get_at_level(self,level):
        level_map = {1: self.r1, 2:self.r2, 3:self.r3, 4:self.r4, 5:self.r5}
        return level_map[level]

class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.name = ""
        self.career_stage = ""
        self.broad_skills = {}
        self.geogs = Geog()
        self.gender = ""
        self.skills = Likert(Likert.TYPE_EXPERTISE)
        self.software = []
        self.methods = Likert(Likert.TYPE_EXPERTISE)
        self.analysis = []
        self.industry = []
        self.prefs = {}

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
        print_dict(self.broad_skills, "Broad Skills:")
        print_geog(self.geogs, "Geographies:")
        print_likert(self.skills, "Skills:")
        print "Software:", self.software
        print_likert(self.methods, "Methods:")
        print "Analysis:",self.analysis
        print "Industry:",self.industry
        print_dict(self.prefs, "Prefs:")
        return

def get_agree(line):
    if "Strongly Agree" in line:
        return 5
    elif "Strongly Disagree" in line:
        return 1
    elif "Disagree" in line:
        return 2
    elif "Neutral" in line:
        return 3
    elif "Agree" in line:
        return 4
    else:
        return -999

users = set([])
with open ("C:/users/aaron/desktop/survey_data.txt") as survey_data:
    current_question = 0
    current_user = None
    for line in survey_data:
        line = line.strip()

        if line[:5] == "PAGE ":
            continue
        # Parse current question
        if line[0] == "Q" and (line[2] == ":" or line[3] == ":"):
            qid = line.split(":")[0][1:]
            try:
                qid = int(qid)
                if qid in [1,2,3,4,5,6,7,8,9,10]:
                    current_question = qid
                else:
                    print "ERROR: Question ID Parse Failed", line
            except:
                print "ERROR: Question ID Parse Failed", line
        # Question 1
        elif "What is your DS ProD member number?" in line:
            user_id = line.split(" ")[-1].replace("/","")
            for x_user in users:
                if x_user.user_id == user_id:
                    print "SOMEONE TOOK THIS TWICE", user_id
                    exit
            current_user = User(user_id)
            users.add(current_user)
        elif "What is your full, real name" in line:
            current_user.name = line[line.find(")")+1:].strip()
#        elif "Go change your DS ProD Meetup photo" in line:
#            users[user_id]["photo"] = ... #TODO:hit API to grab pic, to send to match?
        elif current_question == 2:
            current_user.career_stage = line
        elif current_question == 3:
            skills = line.split("-")
            skill = skills[0].strip()[:-1]
            level = skills[0].strip()[-1]
            current_user.broad_skills[skill] = level
        elif current_question == 4:
            if "Not Int" in line:
                current_user.geogs.never.add(line[:line.find("Not Int")].strip())
            if "Inconvenient" in line:
                current_user.geogs.hard.add(line[:line.find("Inconvenient")].strip())
            if "Convenient" in line:
                current_user.geogs.easy.add(line[:line.find("Convenient")].strip())
            if line[:5] == "Other":
                current_user.geogs.other = line[line.find(")")+1:].strip()
        elif current_question == 5:
            current_user.gender = line
        elif current_question == 6:
            for level in current_user.skills.get_levels():
                level_txt = current_user.skills.txt(level)
                if level_txt in line:
                    skill = line[:line.find(level_txt)].strip()
                    current_user.skills.append_at_level(level,skill)
                    continue
        elif current_question == 7:
            if "Respondent skipped this question" in line:
                continue
            if "n/a" in line:
                continue
            slen = len("Software 1 ")
            package = line[slen:].strip()
            current_user.software.append(package)
        elif current_question == 8:
            for level in current_user.methods.get_levels():
                level_txt = current_user.methods.txt(level)
                if level_txt in line:
                    skill = line[:line.find(level_txt)].strip()
                    current_user.methods.append_at_level(level, skill)
                    continue
        elif current_question == 9:
            response = line[11:]
            if line[:8] == "Analysis":
                current_user.analysis.append(response)
            elif line[:8] == "Industry":
                current_user.industry.append(response)
        elif current_question == 10:
            if "In my industry" in line:
                current_user.prefs["industry"] = get_agree(line)
            if "That I can mentor" in line:
                current_user.prefs["i_mentor"] = get_agree(line)
            if "At my skill level" in line:
                current_user.prefs["at_skill_level"] = get_agree(line)
            if "That will mentor me" in line:
                current_user.prefs["mentor_me"] = get_agree(line)
            if "That are quite similar to me" in line:
                current_user.prefs["similar"] = get_agree(line)
            if "That are quite different from me" in line:
                current_user.prefs["different"] = get_agree(line)
## Print some summaries
for user in users:
    user.to_string()
    break

# Print some descriptive stats
print "# Users", len(users)

loc = {}
def get_easy_potentials(users):
    for user in users:
        user_id = user.user_id
        for easy in user.geogs.easy:
            if easy not in loc:
                loc[easy] = []
            loc[easy].append(user_id)

    potential_pairs = {}
    for easy in loc:
        for user_a in loc[easy]:
            if user_a not in potential_pairs:
                potential_pairs[user_a] = set([])
            for user_b in loc[easy]:
                if user_b not in potential_pairs:
                    potential_pairs[user_b] = set([])
                if user_a != user_b:
                    potential_pairs[user_a].add(user_b)
                    potential_pairs[user_b].add(user_a)
    return potential_pairs

potential_pairs = get_easy_potentials(users)

for user in users:
    if user.user_id not in potential_pairs:
        print "No Matches for:", user.name
    print user.user_id,user.name
#    else:
#        print len(potentials[user.user_id]), "Matches for", user.name
#    if "other" in user.geogs:
#        print user.name,":",user.geogs["other"]


#print potentials

def find_pair(user, potentials,matches):
    if user not in potentials:
        return None
    if (len(potentials[user])) == 0:
        return None
    if len(potentials[user].difference(matches.keys())) == 0:
        return None
    pairs = list(potentials[user].difference(matches.keys()))

    return random.choice(pairs)

match_counts = {}
for x in range(100):
    unmatched = []
    for user in users:
        unmatched.append(user.user_id)

    all_matches = {}
    never_matched = []
    count = 0
    while (len(unmatched)>1 or count > 1000):
        count +=1
        user = random.choice(unmatched)
        pair = find_pair(user,potential_pairs,all_matches)
        if pair is None:
            print user, "had no easy matches left"
            never_matched.append(user)
            unmatched.remove(user)
            continue
        if user == pair:
            print "FAIL"
        unmatched.remove(user)
        unmatched.remove(pair)
        all_matches[user] = pair
        all_matches[pair] = user

    print len(all_matches),all_matches
    match_counts[x] = len(all_matches)
    if len(all_matches) == 8:
        break

print "outcomes", set(match_counts.values())
