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



dprint("txt: \t{}\ndict: \t{}".format(txt, sorted(list(dictionary))))

# dp[i][j] = cost of txt[i:j]
dp = [[0] * len(txt) for _ in range(len(txt))]


# # Init diag
# for i in range(0, len(txt)):
#     if txt[i:i+1] in dictionary:
#         dp[i][i] = 1

for i in range(len(txt)):
    for j in range(0, len(txt) - i):
        dprint(">>> ({}, {}) -----> {}".format(j, i+j+1, txt[j: i+j+1])) 
        if txt[j: i+j+1] in dictionary:
            dp[j][i+j] = len(txt[j: i+j+1]) * len(txt[j: i+j+1])
            dprint("{} in dict!!!".format(txt[j: i+j+1]))
        else:
            ans = [0]
            for k in range(j+1, i+j+1):
                if txt[j:k] in dictionary and txt[k:i+j+1] in dictionary:
                    ans.append(len(txt[j:k])*len(txt[j:k]) + len(txt[k:i+j+1])*len(txt[k:i+j+1]))
                    
                dprint("({}, {}, {}) \t{}\t{}".format(j, i+j+1, k, txt[j:k], txt[k:i+j+1]))
            dp[j][i+j] = max(ans)
        
        dprint()
    dprint("\t-----\t")


pprint(dp)
# (0,0) (0, 1)
#      (1,1) (1,2)
#            (2,2) (2,3)
#                  (3,3)