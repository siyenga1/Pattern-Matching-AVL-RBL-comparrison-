"""
References:
https://www.cs.princeton.edu/~wayne/cs423/lectures/stringsearch-4up.pdf
"""


class KMP:
    """
     KMP class that has
     myInput for taking user input
     myLCSTable for storing the prefix values
     Kmp Search method use the table and search for pattern
    """

    @staticmethod
    def myInput():
        count1 = 0
        count2 = 0
        """
        Takes user inputs and checks for two strings
        """
        print("*********************WELCOME TO KNUTH MORRIS PATTERN SEARCH ALGORITHM*******************")
        # The input string and the pattern to be matched with
        string = input("Please enter the first input string ")
        pattern = input("Please enter the pattern to be matched ")
        if len(string) == 0 or len(pattern) == 0:
            print("Empty String or Empty Pattern")
            return
        """
        calls the default constructor
        """
        positionOfPattern = KMP()
        """
        # listOfindex stores the positions/locations
        """
        listOfindex1 = positionOfPattern.kmpSearch(pattern, string)
        if not listOfindex1:
            print("Pattern not found")
        else:
            for x in listOfindex1:
                print("The strings are the same and found at location", x)
                count1 += 1
            print("The number of times the pattern is found = ", count1)
        """
        Two strings to check different kinds of inputs...
        For ex: to check case sensitive and insensitive.
        """
        string2 = input("Please enter the second input string ")
        pattern2 = input("Please enter the pattern to be matched ")
        if len(string2) == 0 or len(pattern2) == 0:
            print("Empty String or Empty Pattern")
            return
        positionOfPattern2 = KMP()
        listOfindex2 = positionOfPattern2.kmpSearch(pattern2, string2)
        if not listOfindex2:
            print("Pattern not found")
        else:
            for y in listOfindex2:
                print("The strings are the same and found at location", y)
                count2 += 1
            print("The number of times the pattern is found = ", count2)

    @staticmethod
    def myLCSTable(pattern, sizeOfPattern):
        """
        LCS table to store the pattern that's already been discovered
        initialize this table to 0 values.
        For example:
        If t[0..4] matches p[0..4] then t[1..4] matches p[0..3].
        – no need to check i=1,j=0,1,2,3
        – saves 4 comparisons
        """
        lcsTable = [0] * sizeOfPattern
        i = 1
        j = 0
        """
        Iterates over the pattern
        """
        while i != sizeOfPattern:
            if pattern[i] == pattern[j]:
                j = j + 1
                lcsTable[i] = j
                i = i + 1
            elif j != 0:
                j = lcsTable[j - 1]
            else:
                lcsTable[i] = 0
                i = i + 1
        return lcsTable

    def kmpSearch(self, pattern, string):
        """
        To check for length of the text and pattern
        respective variables: sizeOfPattern and string
        """
        sizeOfPattern = len(pattern)
        sizeOfString = len(string)

        """
        Invokes the LCS table to store pattern along
        with length of the pattern computed
        """
        lcsTable = self.myLCSTable(pattern, sizeOfPattern)
        """
        Pointer for string text as i
        and pointer for pattern as j
        """
        patternPos = []
        i = 0
        j = 0

        while i != sizeOfString:
            """
            casefold() makes sure the strings are case-insensitive
            For ex: DATA structure = data structure 
            """
            if string[i].casefold() == pattern[j].casefold():
                i = i + 1
                j = j + 1
            else:
                """
                Pattern not found, 
                decrement j in the table
                """
                j = lcsTable[j - 1]
                """
                if reached the end of the pattern j=sizeofPattern
                print index i-j
                """
            if j == sizeOfPattern:
                patternPos.append(i - j)
                j = lcsTable[j - 1]
                """
                Reached the end of string 
                """
            elif j == 0:
                i += 1

        return patternPos
