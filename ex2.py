from pprint import pprint

debug = True

# Printing for debugging purposes
def dprint(str = ""):
    if debug == True:
        print(str)

wordsLenHistogram = [0] * 31

def readLines(filename):
    d = []
    maxLineLen = 0
    with open(filename) as f:
        for line in f:
            d.append(line.strip('\n'))
            wordsLenHistogram[len(line)] += 1
    return d

if debug == True:
    filename = "data/ex4.test"
else:
    filename = "data/words_for_ai1.txt"

dictionary = set(readLines(filename))


txt = "tamatematyka"
# txt = "mamama"



dprint("txt: \t{}\ndict: \t{}".format(txt, sorted(list(dictionary))))

# dp[i][j] = cost of txt_i, ..., txt_j
dp = [[0] * len(txt) for _ in range(len(txt))]


for i in range(len(txt)):
    for j in range(0, len(txt) - i):
        # Translate coords to human-readable format
        X = j
        Y = i + j + 1
        dprint(">>> ({}, {}) -----> {}".format(X, Y, txt[X: Y])) 
        
        if txt[X: Y] in dictionary:
            dp[j][i + j] = (i + 1) * (i + 1)
            dprint("{} in dict!!!".format(txt[X: Y]))
        else:
            dprint("{} not in dict...".format(txt[X: Y]))
            ans = [0]
            for k in range(X + 1, Y):
                # if txt[j:k] in dictionary and txt[k:Y] in dictionary:
                # ans.append(k * k + (Y - k) * (Y - k))
                dprint("({}, {}, {}) \t{} \t({}) \t{} \t({})".format(X, Y, k, txt[X:k], dp[X][k-1], txt[k:Y], dp[k][Y-1]))
                ans.append(dp[X][k-1] + dp[k][Y-1])     
            dp[j][i+j] = max(ans)  

        dprint()
    # pprint(dp)    
    dprint("\t-----\t")


pprint(dp)
# (0,0) (0, 1)
#      (1,1) (1,2)
#            (2,2) (2,3)
#                  (3,3)

#   m a m a m a
# m   .   x
# a     
# m       .
# a
# m
# a