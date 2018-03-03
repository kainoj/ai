def opt_dist(row, D, debug = False):
    """
    >>> row = [0, 0, 1, 0, 0, 0, 1, 0 , 0 , 0]
    >>> opt_dist(row, 5)
    3
    >>> opt_dist(row, 4)
    4
    >>> opt_dist(row, 3)
    3
    >>> opt_dist(row, 2)
    2
    >>> opt_dist(row, 1)
    1
    >>> opt_dist(row, 0)
    2
    >>> opt_dist([0, 0, 0, 0, 1], 1)
    0
    """

    # Index of a beginnign of a frame
    fst = 0
    # Index after end of a frame
    lst = D

    # Total number of ones in the array
    ones = row.count(1)

    # Number of rows before, in and after frame
    inframe = row[0: D].count(1)
    b4frame = 0
    afframe = ones - inframe

    ans = []

    if D == 0:
        return ones
    
    for i in range(len(row) - D +1 ):
        if debug:
            print("---")
            print(row)
            print("{}{}".format("   " *i, row[fst:lst]))
            print("\tmusze ustawic {} jedynek, {} zgasic przed, {} jedynek zgasic po".format(D - inframe, b4frame, afframe))
            print("\t\t b4 = {}, in = {}, af = {}".format(b4frame, inframe, afframe))
            print("\t\t fst = {} \t lst = {}".format(fst, lst))

        ans.append(D - inframe + b4frame + afframe)      

        # One 1 was dropped form rame
        if row[fst] == 1:
            if debug:
                print("\t\tdrop: {}".format(fst))
            inframe = max(inframe - 1, 0)
            b4frame += 1
        
        # One 1 was put in frame
        if lst < len(row) and row[lst] == 1:
            if debug:
                print("\t\tgain: {}".format(lst))            
            inframe += 1
            afframe = max(afframe - 1, 0)

        # Move indiceies
        fst += 1
        lst += 1

    
    return min(ans)


if __name__ == '__main__':
    
    finput  = 'zad4_input.txt'
    foutput = 'zad4_output.txt'

    f2 = open(foutput,"w") 

    with open(finput) as f:
        for line in f:
            row, D = line.strip().split(" ")
            row = [int(s) for s in row]
            D = int(D)
            print(opt_dist(row, D), file = f2)
