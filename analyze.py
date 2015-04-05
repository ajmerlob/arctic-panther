import random

class Analyze:
    def __init__(self,users):
        self.potential_pairs = {}
        self.users = users
        self.match_results = set([])

    def get_user_by_id(self,user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    def get_potential_pairs(self):
        return self.potential_pairs

    def analyze_easy_potentials(self):
        loc = {}
        for user in self.users:
            user_id = user.user_id
            easy_geogs = user.geogs.get_at_level("Easy")
            if easy_geogs is None:
                print "No Easy Matches for :", user.name, user_id, ":-(", user.geogs.print_string()
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

    def get_best_matches(self):
        def find_pair(user, potentials,matches):
            if user not in potentials:
                return None
            if (len(potentials[user])) == 0:
                return None
            if len(potentials[user].difference(matches.keys())) == 0:
                return None
            pairs = list(potentials[user].difference(matches.keys()))
            return random.choice(pairs)

        def calculate():
            unmatched = []
            for user in self.users:
                unmatched.append(user.user_id)

            all_matches = {}
            never_matched = []
            count = 0
            while (len(unmatched)>1 or count > 1000):
                count +=1
                user = random.choice(unmatched)
                pair = find_pair(user,self.potential_pairs,all_matches)
                if pair is None:
#                    print user, "had no easy matches left"
                    never_matched.append(user)
                    unmatched.remove(user)
                    continue
                if user == pair:
                    print "FAIL"
                unmatched.remove(user)
                unmatched.remove(pair)
                all_matches[user] = pair
                all_matches[pair] = user
            return all_matches

        def get_match_results(all_matches):
            match_results = set([])
            for match in all_matches:
                u1= self.get_user_by_id(match)
                u2= self.get_user_by_id(all_matches[match])
                if u1.user_id > u2.user_id:
                    match_results.add((u1,u2))
                else:
                    match_results.add((u2,u1))
            return match_results

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


        print len(all_matches),all_matches
        for match in all_matches:
            u1= self.get_user_by_id(match)
            u2= self.get_user_by_id(all_matches[match])
            print u1.name, "---", u2.name, " ||| ", u1.user_id, "---", u2.user_id

        self.match_results = get_match_results(all_matches)
        return self.match_results
        

