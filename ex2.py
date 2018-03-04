from pprint import pprint

debug = False

# Printing for debugging purposes
def dprint(str = ""):
    if debug == True:
        print(str)

def dpprint(str):
    if debug == True:
        pprint(str)

# Read lines from file and return them as an array
def readLines(filename):
    d = []
    with open(filename) as f:
        for line in f:
            d.append(line.strip('\n'))
    return d


# Given 'matrix of slice points', restore spaces
def traceback(i, j, K):
    if i >= j:
        return ""
    dprint("i = {}\tj = {}\t --> {}".format(i, j, txt[i:j]))
    if txt[i:j] in dictionary:
        return txt[i:j]
    k = K[i][j-1]
    return traceback(i, k, K) + " " + traceback(k, j, K)


def spacify(txt):
    # dp[i][j] = cost of txt_i, ..., txt_j
    dp = [[0] * len(txt) for _ in range(len(txt))]

    # For each slice txt_i, ..., txt_j remember k - slicing point
    # ks[i][j] - a point, where txt_i, ..., txt_j was sliced 
    ks = [[0] * len(txt) for _ in range(len(txt))]

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
                dpk = 0
                kpos = 0
                for k in range(X + 1, Y):
                    dprint("({}, {}, {}) \t{} \t({}) \t{} \t({})".format(X, Y, k, txt[X:k], dp[X][k-1], txt[k:Y], dp[k][Y-1]))
                    if dp[X][k-1] == 0 or dp[k][Y-1] == 0:
                        dprint("mam cie smieciu")

                    elif dp[X][k-1] + dp[k][Y-1] > dpk:
                        dpk = dp[X][k-1] + dp[k][Y-1]
                        kpos = k
                dp[j][i+j] = dpk
                ks[j][i+j] = kpos

            dprint()
        dprint("\t-----\t")
    dpprint(dp)
    dpprint(ks)
    return traceback(0, len(txt), ks)


dictionary = {}

if __name__ == '__main__':

    dictfile = "data/words_for_ai1.txt"
    inpfile = "data/pan_tadeusz_bez_spacji.txt"

    inpfile = "zad2_input.txt"
    outfile = "zad2_output.txt"

    # inpfile = "data/ex4-2.in"    
    # debug = True

    dictionary = set(readLines(dictfile))
    txts = readLines(inpfile)

    with open(outfile, 'w') as f:
        for txt in txts:
            res = spacify(txt)
            f.write(res + "\n")
        
    