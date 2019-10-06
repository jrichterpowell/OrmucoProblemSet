import random,time

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
        
        return "{} is equal to {}".format(string1, string1)

s = StringComparator()

print(s.compare('cat', 'dog'))
print(s.compare('aaab', 'aaaa'))
print(s.compare('baby', 'bark'))
print(s.compare('paradigm', 'parallel'))

#maps a decimal number to the first 10 letters of the alphabet
def mapString(integer, offset):

    endstr = ''
    letter = integer % 10 
    integer //= 10
    while integer:
        endstr += chr(letter + 97+ offset)
        letter = integer % 10 
        integer //= 10
    
    endstr += chr(letter + 97 + offset)
    return endstr[::-1]

print('Generating 100 random test cases')
time.sleep(3)
#generates 100 random test cases, which we know the order of since they are encoded numbers
for i in range(100):
    offset = random.randint(0,16)
    num1 = random.randint(10**8, 10**9)
    num2 = random.randint(10**8, 10**9)
    str1 = mapString(num1, offset)
    str2 = mapString(num2, offset)

    print(s.compare(str1, str2))
    print('And the correct order was', ((str1, str2) if num1 > num2 else (str2,str1)))

