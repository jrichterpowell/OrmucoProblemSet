import sys 

if len(sys.argv) != 5:
    print("Error: Not enough arguments provided")

#logic is fairly straightforward, intersection is only non-empty if (x_1 > x_3 && x_1 < x_4) ||  (x_2 > x_3 && x_2 < x_4)
# since the intervals are closed and contain their endpoints

def testIntersection(A,B):
    print(A,B)
    if (A[0] >= B[0] and A[1] <= B[1]) or  (A[1] >= B[0] and A[1] <= B[1]):
        return "Lines Intersect!"
    
    return "Lines do not intersect"

line1 = (float(sys.argv[1]), float(sys.argv[2]))
line2 = (float(sys.argv[3]), float(sys.argv[4]))

print(testIntersection(line1, line2))