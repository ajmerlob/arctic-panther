from config import Config

class Text:
    def __init__(self, group_id):
        self.group_id = group_id
        self.take_survey = "%s\nThanks for signing up for Pair Data Science! This is an awesome, game-changing format, and I'm sure you will love it as much as I do.\n\nIn order to match you as best as possible, though, I need some data about you.  Please take this survey and we can get started.\n%s \n\nCheers,\nAaron" % ("%s",Config.groups[self.group_id])
        pass
    