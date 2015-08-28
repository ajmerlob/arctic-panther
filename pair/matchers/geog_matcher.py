import random as rand
from matcher import Matcher


class GeogMatcher(Matcher):
    def __init__(self,users, seed=rand.randint(100000,999999999)):
        """Initialize a Geograpy-based Matcher"""
        super(GeogMatcher, self).__init__(users,seed)
        
    def get_best_matches(self):
        """Return convenient matchers based on geography."""
        def analyze_easy_potentials():
            """Find matches where both participants share a 'convenient' location"""
            loc = {}
            for user in self.users:
                user_id = user.user_id
                easy_geogs = user.geogs.get_at_level("Easy")
                if easy_geogs is None:
                    print "No Easy Matches for :", user.name, user_id, ":-(", user.geogs.get_print_string()
                    continue
                for easy in easy_geogs:
                    if easy not in loc:
                        loc[easy] = []
                    loc[easy].append(user_id)

            for easy in loc:
                for user_a in loc[easy]:
                    if user_a not in self.potential_pairs:
                        self.potential_pairs[user_a] = set([])
                    for user_b in loc[easy]:
                        if user_b not in self.potential_pairs:
                            self.potential_pairs[user_b] = set([])
                        if user_a != user_b:
                            self.potential_pairs[user_a].add(user_b)
                            self.potential_pairs[user_b].add(user_a)

        def find_pair(user, potentials,matches):
            """Select an arbitrary applicable pair"""
            ## If user doesn't have any potential matches
            ## then return None, they have no options
            if user not in potentials:
                return None
            ## If user doesn't have any potential matches
            ## then return None, they have no options
            if (len(potentials[user])) == 0:
                return None
            ## If the only possible matches are people that have
            ## already been assigned a match, then there
            ## are no remaining options, return None
            if len(potentials[user].difference(matches.keys())) == 0:
                return None
            ## Return a random potential match
            pairs = list(potentials[user].difference(matches.keys()))
            return self.random.choice(pairs)

        def calculate():
            """This is the algorithm that assigns matches to users"""
            ## Start with all users as unmatched
            unmatched = [user.user_id for user in self.users]

            all_matches = {}
            never_matched = []
            count = 0
            ## Iterate until everyone is matched
            ## Or the algorithm gets bored
            while (len(unmatched)>1 or count > 1000):
                count +=1
                ## Pick an arbitrary person to start with
                user = self.random.choice(unmatched)
                ## Find a suitable match for that chosen user
                pair = find_pair(user,self.potential_pairs,all_matches)
                ## If chosen use has no matches then indicate
                ## that by adding them to the never_matched list
                ## and taking them out of the unmatched list
                ## (because given the current matches
                ## they have no future chance of matching)
                if pair is None:
#                    print user, "had no easy matches left"
                    never_matched.append(user)
                    unmatched.remove(user)
                    continue
                ## Below are just matched users

                ## The user and their match should never be
                ## the same user - that's an error
                if user == pair:
                    print "FAIL"

                ## Since both the user and their pair are
                ## matched, they are removed from unmatched
                ## and added to the list of matches
                unmatched.remove(user)
                unmatched.remove(pair)
                all_matches[user] = pair
                all_matches[pair] = user
            return all_matches

        def get_match_results(all_matches):
            """Return set of users in place of set of user ids"""
            match_results = set([])
            for match in all_matches:
                u1= self.get_user_by_id(match)
                u2= self.get_user_by_id(all_matches[match])
                ## Matches should only be in once.
                ## This puts the user with the largest
                ## user id in the first position
                if u1.user_id > u2.user_id:
                    match_results.add((u1,u2))
                else:
                    match_results.add((u2,u1))
            return match_results

        ## calculates the potential matches
        analyze_easy_potentials()

        ## Since the algorithm doesn't promise an optimal
        ## solution on it's first (or any) iteration,
        ## this finds 1000 possible solutions and simply
        ## picks the highest performing iteration to return
        match_counts = {}
        for x in range(1000):
            all_matches = calculate()
            match_counts[x] = len(all_matches)
#            print len(all_matches),all_matches
        print "Count of Matches:", set(match_counts.values())
        max_matches = max(set(match_counts.values()))
        current_matches = 0
        while current_matches < max_matches:
            all_matches = calculate()
            current_matches = len(all_matches)

        ## Gets the match results in terms of users
        ## instead of just the user ids
        self.match_results = get_match_results(all_matches)

        ## For ease of spot checking,
        ## This prints all of the winning pairs
        ## along with the geogs where they can easily meet
        print "# Matches", len(all_matches),"matches", all_matches
        for u1, u2 in self.match_results:
            print u1.name, "---", u2.name, " ||| ", u1.user_id, "---", u2.user_id, "|||", set(u2.geogs.get_at_level("Easy")).intersection(set(u1.geogs.get_at_level("Easy")))
        
        return self.match_results
        

