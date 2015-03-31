from user import User

class Parser:
    def __init__(self, survey_uri):
        self.users = set([])
        self.survey_uri = survey_uri
        self.parse()

    def get_users(self):
        return self.users

    def parse(self):
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

        with open (self.survey_uri) as survey_data:
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
                    for x_user in self.users:
                        if x_user.user_id == user_id:
                            print "SOMEONE TOOK THIS TWICE", user_id
                            exit
                    current_user = User(user_id)
                    self.users.add(current_user)
                elif "what you put on Meetup" in line:
                    current_user.name = line[line.find(")")+1:].strip()
        #        elif "Go change your DS ProD Meetup photo" in line:
        #            self.users[user_id]["photo"] = ... #TODO:hit API to grab pic, to send to match?
                elif current_question == 2:
                    current_user.career_stage = line
                elif current_question == 3:
                    skills = line.split("-")
                    for level in current_user.methods.get_levels():
                        level_txt = current_user.methods.txt(level)
                        if level_txt in line:
                            skill = skills[0].strip()[:-1]
                            current_user.broad_skills.append_at_level(level, skill)
                            continue
                elif current_question == 4:
                    for level in current_user.geogs.get_levels():
                        level_txt = current_user.geogs.txt(level)
                        geog = line[:line.find(level_txt)].strip()
                        if level_txt in line:
                            current_user.geogs.append_at_level(level,geog)
                    if line[:5] == "Other":
                        current_user.geogs.append_at_level("Other", line[line.find(")")+1:].strip())
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
                        current_user.prefs.append_at_level(get_agree(line),"industry")
                    if "That I can mentor" in line:
                        current_user.prefs.append_at_level(get_agree(line),"i_mentor")
                    if "At my skill level" in line:
                        current_user.prefs.append_at_level(get_agree(line),"at_skill_level")
                    if "That will mentor me" in line:
                        current_user.prefs.append_at_level(get_agree(line),"mentor_me")
                    if "That are quite similar to me" in line:
                        current_user.prefs.append_at_level(get_agree(line),"similar")
                    if "That are quite different from me" in line:
                        current_user.prefs.append_at_level(get_agree(line),"different")

        return self.users