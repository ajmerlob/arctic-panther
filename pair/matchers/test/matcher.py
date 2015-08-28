# To change this template, choose Tools | Templates
# and open the template in the editor.

import unittest
from pair.matchers.geog_matcher import GeogMatcher
from core.simulator import Simulator

class  MatcherTestCase(unittest.TestCase):
    """Tests the various Matcher subclasses"""

    all_matchers = [GeogMatcher]

    def setUp(self):
        self.sim = Simulator()
        self.sim.simulate(10, 13579)
        

    def test_matcher(self):
        """Test various matcher subclasses"""
        def test_empty_matcher(MatcherSub):
            """Test empty Matcher returns valid empty results"""
            ## Test that an empty set returns valid, emtpy results
            matcher_sub = MatcherSub(set([]))
            unmatched = matcher_sub.get_unmatched()
            best_matches = matcher_sub.get_best_matches()
            self.assertEqual(unmatched, set([]));
            self.assertEqual(best_matches, set([]));

        def test_matcher_matches(MatcherSub, expected_matches, expected_unmatches):
            """Spin up Matcher subclass and confirm expected results"""
            users = self.sim.get_users()
            self.assertEqual(len(users),10, "Sanity check simulator user count")
            matcher_sub = MatcherSub(users,seed=1234)
            best_matches = set([(tup[0].user_id, tup[1].user_id) for tup in matcher_sub.get_best_matches() ])
            unmatched = set([user.user_id for user in matcher_sub.get_unmatched()])
            print best_matches
            print unmatched

            for match in expected_matches:
                self.assertIn(match, best_matches, "Expected match not found - perhaps the algo or simulator changed?")

            for unmatch in expected_unmatches:
                self.assertIn(unmatch, unmatched, "Expected unmatched not found - perhaps the algo or simulator changed?")

        ## Test empty matcher return valid results
        for MatcherSub in self.all_matchers:
            test_empty_matcher(MatcherSub)

        ## For each Matcher subclass, work out what the answers should be
        ## given the simulator's users, and record the answers here
        geog_matched = [(7736498, 2837615), (5072324, 795755), (4454245, 3882723)]
        geog_unmatched = [1510961, 8148259, 6505708, 2432669]

        ## Feed the expected results into 3-tuples below to be tested
        ## (MatcherSubclass , expected_match_results, expected_unmatched_results)
        test_cases = [
            (GeogMatcher, geog_matched,geog_unmatched)
            ]

        ## Test full matchers return correct results
        for match_case in test_cases:
            test_matcher_matches(*match_case)

if __name__ == '__main__':
    unittest.main()

