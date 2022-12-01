class KMP:
    # KMP class that has
    # myInput for taking user input
    # myLCSTable for storing the prefix values
    # Kmp Search method use the table and search for pattern

    def myInput(self):
        count1 = 0
        count2 = 0
        # Takes user inputs and checks for two strings
        print("*********************WELCOME TO KNUTH MORRIS PATTERN SEARCH ALGORITHM*******************")
        # The input string and the pattern to be matched with
        string = input("Please enter the first input string ")
        pattern = input("Please enter the pattern to be matched ")
        if len(string) == 0 or len(pattern) == 0:
            print("Empty String or Empty Pattern")
            return
        # calls the default constructor
        positionOfPattern = KMP()
        # listOfindex stores the positions/locations
        listOfindex1 = positionOfPattern.kmpSearch(pattern, string)
        if not listOfindex1:
            print("Pattern not found")
        else:
            for x in listOfindex1:
                print("The strings are the same and found at location", x)
                count1 += 1
            print("The number of times the pattern is found = ", count1)

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

    def myLCSTable(self, pattern, sizeOfPattern):
        # LCS table to store the pattern that's already been discovered

        # initialize table to 0 values
        lcsTable = [0] * sizeOfPattern
        i = 1
        j = 0
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
        # to check for length of the text and pattern
        sizeOfPattern = len(pattern)
        sizeOfString = len(string)

        # LCS Table
        lcsTable = self.myLCSTable(pattern, sizeOfPattern)

        # Pointers for string text and pattern
        patternPos = []
        i = 0;
        j = 0;

        while i != sizeOfString:
            # Makes sure the strings are case-insensitive
            if string[i].casefold() == pattern[j].casefold():
                i = i + 1;
                j = j + 1;
            else:
                # Pattern not found, decrement j in the table
                j = lcsTable[j - 1]
                # if reached the end of the pattern j=sizeofPattern
                # print index i-j
            if j == sizeOfPattern:
                patternPos.append(i - j)
                j = lcsTable[j - 1]
                # Reached the end of string but j is zero
            elif j == 0:
                i += 1;

        return patternPos
