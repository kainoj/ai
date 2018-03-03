
#    tamatematykapustkinieznosi
#   t
#   a   
  
wordsLenHistogram = [0] * 31

def readLines(filename):
    d = []
    maxLineLen = 0
    with open(filename) as f:
        for line in f:
            d.append(line.strip('\n'))
            wordsLenHistogram[len(line)] += 1
    return d

dictionary = set(readLines("data/words_for_ai1.txt"))

# for (i, val) in enumerate(wordsLenHistogram):
#     print("{}: \t {}".format(i, val))

txt = "tamatematykapustkinieznosi"

txt = "ala"
# dp[i][j] = cost of txt[i:j]
dp = [[0] * len(txt) for _ in range(len(txt))]


# Init diag
for i in range(0, len(txt)):
    if txt[i:i+1] in dictionary:
        dp[i][i] = 1

for i in range(len(txt)):
    for j in range(0, len(txt) - i):
        print("({}, {})".format(j, i+j+1))
    print()


# (0,0) (0, 1)
#      (1,1) (1,2)
#            (2,2) (2,3)
#                  (3,3)