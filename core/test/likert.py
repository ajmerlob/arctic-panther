__author__="Aaron"

import unittest
from core.likert import Likert

class  LikertTestCase(unittest.TestCase):
    def setUp(self):
        self.likert_exp = Likert(Likert.TYPE_EXPERTISE)
        self.likert_agr = Likert(Likert.TYPE_AGREEMENT)
        self.likert_geo = Likert(Likert.TYPE_GEOG)

    def tearDown(self):
        self.likert_exp = None
        self.likert_agr = None
        self.likert_geo = None

    
    def test_likerts(self):
        def test_blank_likert(likert):
            self.assertEqual(likert.get_print_string(),"")
            
        for likert in [self.likert_exp,self.likert_agr,self.likert_geo]:
            test_blank_likert(likert)

    def test_exp(self):
        exp = self.likert_exp
        checks = (
            (exp.get_levels(), [1,2,3,4,5]),
            (exp.get_level_names(), [
                '1 - No Exposure',
                '2 - Beginner',
                '3 - Beginner / Intermediate',
                '4 - Intermediate',
                '5 - Expert'
            ]),
            (exp.txt(1), '1 - No Exposure'),
            (exp.txt(2), '2 - Beginner'),
            (exp.txt(3), '3 - Beginner / Intermediate'),
            (exp.txt(4), '4 - Intermediate'),
            (exp.txt(5), '5 - Expert'),
            (exp.append_at_level(1, "Hello!"), None),
            (exp.get_at_level(1),['Hello!'])
        )

        ## Test that all the checks evaluate to the correct responses
        for expression, expected_result in checks:
            self.assertEqual(expression,expected_result)

        ## Additionally test the append at level and get at level
        exp.append_at_level(2, "Goodbye!")
        exp.append_at_level(1, "Cool!")
        exp.append_at_level(1, "Bad!")
        self.assertEqual(exp.get_at_level(1),['Hello!','Cool!',"Bad!"])
        self.assertEqual(exp.get_at_level(2),['Goodbye!'])

if __name__ == '__main__':
    unittest.main()

