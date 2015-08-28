__author__="Aaron"

from pair.main import Main
from core.config import Config

if __name__ == "__main__":
    spam_missing_surveys = False


    for group_id in Config.groups:
        main = Main(group_id)
        main.get_users()
        if spam_missing_surveys:
            main.send_missing_survey_messages()
        pairs = main.analyze_pairs()
#        main.send_pair_assignment_messages("May 29th", pairs,False)
