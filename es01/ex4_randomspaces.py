import random as rand

def randspac(txt):
    if txt == "" or len(txt) == 1:
        return txt
    k = rand.randint(1, len(txt))
    return txt[0:k] + " " + randspac(txt[k:])

def randspace2(txt):
    rs = [0]
    while rs[-1] < len(txt):
        rs.append(rand.randint(rs[-1]+1, len(txt)))
    res = ""
    for i in range(1, len(rs)):
        res += txt[rs[i-1]:rs[i]] + " "
    return res

def randspace3(txt):
    rs = [0]
    res = ""
    while rs[-1] < len(txt):
        rs.append(rand.randint(rs[-1]+1, len(txt)))
        res += txt[rs[-2]:rs[-1]] + " "
    return res

def randspace4(txt):
    prev = 0
    curr = 0
    res = ""
    while prev < len(txt):
        curr = rand.randint(prev+1, len(txt))
        res += txt[prev:curr] + " "
        prev = curr
    return res





txt = "alamakota"

res = randspac(txt)
print(res)

print(randspace2(txt))
print(randspace3(txt))
print(randspace4(txt))