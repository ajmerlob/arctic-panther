from core.config import Config

class Text:
    def __init__(self, group_id):
        self.group_id = group_id
        self.take_survey = "%s\nThanks for signing up for Pair Data Science! This is an awesome, game-changing format, and I'm sure you will love it as much as I do.\n\nIn order to match you as best as possible, though, I need some data about you.  Please take this survey and we can get started.\n%s \n\nCheers,\nAaron" % ("%s",Config.groups[self.group_id])
        self.assign_pair = "Hello DS ProDers!\n\nThanks for signing up for \"Pair Data Science!\" Each Thursday I'll give you a new pair!\n\nYour responsibility is to meet in person with your pair, at least once, and for at least 90 minutes, to work together on Data Science exercises. For this round, you have until Friday, %s at Midnight! Go be awesome!\n\n%s and %s - this week you are a pair!\n\nPlease reach out to me if you need additional support.\n\nCheers,\nAaron"

    def get_survey_text(self,name):
        return self.take_survey % (name)

    def assign_pairs(self,datestring,name1,name2):
        return self.assign_pair % (datestring,name1,name2)
