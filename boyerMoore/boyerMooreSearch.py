# Boyer Moore Implementation
# References:
# https://dl.acm.org/doi/pdf/10.1145/359842.359859
# https://www.cs.jhu.edu/~langmea/resources/lecture_notes/strings_matching_boyer_moore.pdf
class BoyerMooreSearch:
    def __init__(self, pattern=None):
        """
        Constructor for the Boyer Moore Search
        Sets the pattern and creates delta tables
        in case search is required in more than one
        text.
        """
        self.pattern = pattern
        if self.pattern:
            self.delta1 = self.generate_delta_1(self.pattern)
            self.prefix_suffix_table = self.preprocess_prefix_suffix(self.pattern)
            self.delta2_case1 = self.good_suffix_rule_case_1(self.pattern)
            self.delta2_case2 = self.good_suffix_rule_case_2(self.pattern)

    def set_pattern(self, pattern):
        """
        Sets the pattern in the object if
        not done during initialization.
        """
        self.pattern = pattern
        self.delta1 = self.generate_delta_1(self.pattern)
        self.prefix_suffix_table = self.preprocess_prefix_suffix(self.pattern)
        self.delta2_case1 = self.good_suffix_rule_case_1(self.pattern)
        self.delta2_case2 = self.good_suffix_rule_case_2(self.pattern)

    def generate_delta_1(self, pattern):
        """
        generates the delta1 (bad character table)
        for shift.
        It is generated for all characters in char set.
        for characters in pattern, the value is set to
        patlen - (i-1).
        for others, value is set to patlen.

        bad character table, looks for the character
        mismatched in text. If the character does not
        exist in the pattern anywhere, It is better to
        shift entire pattern rather than by 1. Hence,
        we set the value to such characters as patlen.

        For similar case with characters present in our
        pattern, we want to align the mismatched character
        in text to the character in pattern, thus the distance
        from the end to the index is the shift required.
        """
        patlen = len(pattern)
        delta1 = [patlen] * 256

        for i in range(patlen - 1):
            if ord(pattern[i])>256:
                print(pattern[i], ord(pattern[i]))
            delta1[ord(pattern[i])] = patlen - i - 1

        return delta1

    def preprocess_prefix_suffix(self, pattern):
        """
        Table at ith index stores the index of
        the start of the suffix which is equal
        to some prefix of pattern[i:patlen].
        """
        patlen = len(pattern)
        j = patlen + 1
        suffix_start_index = [0] * (patlen + 1)
        suffix_start_index[patlen] = patlen + 1
        suffix_start_index[patlen - 1] = patlen
        i = patlen - 1
        j = j - 1

        while i > 0:
            while j <= patlen and pattern[i - 1] != pattern[j - 1]:
                # Incase there is a mismatch between
                # the characters, the suffix_start_index
                # lies towards the previous suffix_start_index
                # until we find equal character to i-1
                # then we assign that border to our char
                # else if no suffix exists that equals
                # prefix, we assign length
                j = suffix_start_index[j]

            # Incase the char prev to last suffix_start
            # matches with our char our new suffix_starts
            # from prev char in the pattern
            # example:
            # bddcdd
            #  ^  ^
            #  1  4
            # here d at index 1 will match with d at index 4
            # hence suffix_start_index[1] = 4
            j -= 1
            i -= 1
            suffix_start_index[i] = j
        return suffix_start_index

    def good_suffix_rule_case_1(self, pattern):
        """
        Uses the prefix_suffix_table generated
        to store the delta2 for case 1.

        Case 1 is when you match a suffix of
        pattern with text and match failed preceding
        the suffix and another substring equal to
        the suffix exists in the pattern with different
        character preceding to it.

        We reverse look up on our prefix_suffix_table.
        Since we know that for ith index suffix start
        at some prefix_suffix_table[i], therefore, we
        can see that suffix from prefix_suffix_table[i]
        to end exists from i to patlen - prefix_suffix_table[i].


        We check the preceding characters using the below
        condition and if they are not same, we calculate shift.

        pattern[self.prefix_suffix_table[i]-1] != pattern[i-1]

        We try to shift to the right most occurrence of the
        suffix incase we have multiple occurrences. Therefore,
        incase we have a non-zero delta present for the index,
        we don't change it. Below condition ensures it.

        good_suffix_table[self.prefix_suffix_table[i]] == 0
        """
        m = len(pattern)
        good_suffix_table = [0] * (m + 1)
        for i in range(len(good_suffix_table) - 2, -1, -1):
            if pattern[self.prefix_suffix_table[i] - 1] != pattern[i - 1] and good_suffix_table[self.prefix_suffix_table[i]] == 0:
                good_suffix_table[self.prefix_suffix_table[i]] = self.prefix_suffix_table[i] - i
        return good_suffix_table

    def good_suffix_rule_case_2(self, pattern):
        """
        This is to generate delta2 for case 2.
        Case 2 is used only when we don't have a substring
        equal to the suffix but a part of the suffix is equal to
        the prefix of the pattern itself. In that case,
        we use the delta2 case 2.
        max_suffix is index at which suffix of the pattern
        equals prefix of the pattern
        ex: dddsydssddd
            ---     ---
            ^       ^
            0       8
            max_shift=prefix_suffix_table[0] = 8
            Hence, from index 0 to 8, we know we can shift
            to the maximum.

            Then we change the value to the new max_shift
            in case we have some prefix equal to suffix.

        """
        patlen = len(pattern)
        max_suffix = self.prefix_suffix_table[0]
        good_suffix_table_c2 = [max_suffix if j < max_suffix else 0 for j in range(patlen + 1)]

        i = max_suffix
        while i <= patlen:
            good_suffix_table_c2[i] = max_suffix
            if max_suffix == i:
                max_suffix = self.prefix_suffix_table[max_suffix]
            i += 1
        return good_suffix_table_c2

    def search(self, text, pattern=None):
        """
        Searches the pattern in text in
        case-sensitive manner.
        Incase, pattern has been set already,
        We can search using the text only.
        """
        if not pattern and not self.pattern:
            print("Set Pattern or Pass pattern")
        elif pattern:
            self.set_pattern(pattern)
        self.search_util(text, self.pattern)

    def search_util(self, text, pat):
        """
        Runs the search using delta1 and delta2
        delta1 is the bad character while delta2
        have 2 cases. Shift utilizes the maximum
        of delta1 and delta2 cases in different
        scenarios.

        It finds all the occurances of the pattern
        in the text.
        """
        s = 0
        patlen = len(pat)
        n = len(text)
        flag = False
        # Generate tables for delta1, delta2 case 1 & 2
        delta1 = self.delta1
        delta2_1 = self.delta2_case1
        delta2_2 = self.delta2_case2

        while s <= n - patlen:
            j = patlen - 1
            while j >= 0 and pat[j] == text[s + j]:
                j -= 1

            # if j<0, means pattern matched
            if j < 0:
                print("pattern occurs at location = %d" % s)
                flag = True
                if s + patlen < n:
                    next_char = text[s + patlen]
                    s = s + delta1[ord(next_char)]
                else:
                    s += delta2_2[0]
            else:
                # In case of mismatch at first character
                # use bad character table
                if j + 1 == patlen:
                    bad_char = text[s + j]
                    #print(bad_char,ord(bad_char))
                    bad_char_occ = delta1[ord(bad_char)] - (patlen - j)
                    s += max(1, bad_char_occ)
                elif delta2_1[j + 1] != 0:
                    # Incase we have reoccurrence with preceding
                    # character different, we take max from bad char
                    # and delta2 case 1
                    bad_char = text[s + j]
                    bad_char_occ = delta1[ord(bad_char)] - (patlen - j)
                    s += max(delta2_1[j + 1], bad_char_occ)
                else:
                    # Incase delta2 case 1 was not applicable
                    # we use detla2 case 2.
                    s += delta2_2[j + 1]

        if not flag:
            print("Pattern not found anywhere in string.")