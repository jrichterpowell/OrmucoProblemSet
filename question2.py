class StringComparator:
    def compare(self, string1, string2):
        loopLen = max(len(string1), len(string2))

        for i in range(loopLen):

            if i < len(string1):
                a = ord(string1[i])
            else:
                a = ord(' ')
            
            if i < len(string2):
                b = ord(string2[i])
            else:
                b = ord(' ')
            
            if a < b:
                return "{} is greater than {}".format(string2,string1)
            elif a>b:
                return "{} is greater than {}".format(string1,string2)
            else:
                continue

s = StringComparator()

print(s.compare('cat', 'dog'))