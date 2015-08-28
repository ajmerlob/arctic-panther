__author__="Aaron"

import unittest
from core.simulator import Simulator

class  SimulatorTestCase(unittest.TestCase):
    def setUp(self):
        self.sim = Simulator()

    def tearDown(self):
        self.sim = None

    def test_simulator(self):
        self.assertEqual(self.sim.get_users(),set([]))
        self.assertEqual(self.sim.CAREER_STAGES, {"Student": 10, "Entry": 15, "Early":25, "Middle": 40, "Late": 10})

    def test_simulate(self):
        """Tests the simulate and clear_users methods
        
        Since multiple calls to simulate continue to grow the group,
        the test demonstrates that the group grows.  It also tests that
        the users set can be cleared.
        """

        ## Simulate the first 5 users
        self.sim.simulate(5,1234)
        users = list(sorted(
            self.sim.get_users(),
            cmp=lambda x,y : cmp(x.user_id,y.user_id)
            ))
        print users
        expected_results = {
            4 : (8698081,"Melinda Thompson"),
            3 : (8453420, "Freddie Bahlmann"),
            2 : (8198783, "Gary Paddock"),
            1 : (3966593, "Kevin Wilson"),
            0 : (67423, "Scott Lopez")
        }
        for i in range(5):
            self.assertEqual((users[i].user_id,users[i].name),expected_results[i])
        
        ## Clear the simulated users, and resimulate the same users
        self.sim.clear_users()
        self.sim.simulate(5,1234)
        users = list(sorted(
            self.sim.get_users(),
            cmp=lambda x,y : cmp(x.user_id,y.user_id)
            ))
        print users
        expected_results = {
            4 : (8698081,"Melinda Thompson"),
            3 : (8453420, "Freddie Bahlmann"),
            2 : (8198783, "Gary Paddock"),
            1 : (3966593, "Kevin Wilson"),
            0 : (67423, "Scott Lopez")
        }
        for i in range(5):
            self.assertEqual((users[i].user_id,users[i].name),expected_results[i])

        ## Add 5 more users on top of existing users.
        ## Since the same seed is used, it should be tempted
        ## to duplicate the previous users, but the simulate
        ## method should prevent this from happening
        self.sim.simulate(5,1234)
        users = list(sorted(
            self.sim.get_users(),
            cmp=lambda x,y : cmp(x.user_id,y.user_id)
            ))
        print users
        expected_results = {
            9 : (8698081,"Melinda Thompson"),
            8 : (8698080, "Angela Jones"),
            7 : (8453420, "Freddie Bahlmann"),
            6 : (8453419, "Marilynn Orr"),
            5 : (8198783, "Gary Paddock"),
            4 : (8198781, "Tiffany Mchaney"),
            3 : (3966593, "Kevin Wilson"),
            2 : (3966592, "Donna Yu"),
            1 : (67424, "Patrice Newell"),
            0 : (67423, "Scott Lopez")
        }
        for i in range(5):
            self.assertEqual((users[i].user_id,users[i].name),expected_results[i])

    def test_blank_simulator(self):
        blankSim = Simulator()
        self.assertEqual(blankSim.get_users(),set([]))
        self.assertEqual(blankSim.CAREER_STAGES, {"Student": 10, "Entry": 15, "Early":25, "Middle": 40, "Late": 10})

if __name__ == '__main__':
    unittest.main()

