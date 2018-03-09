import os

from ex1print import print_board

class onboard():
    
    def __init__(self, wk, wt, bk, col):
        self.wk = wk
        self.wt = wt
        self.bk = bk
        self.col = col
        self.board = set([chr(col + ord('a')) + chr(row + ord('1')) 
                            for col in range(0, 8) for row in range(0,8)])
    
    # Prints the board
    def printb(self):
        print("Next move: " + col)
        print_board(self.wk, self.wt, self.bk, True)
    

    # Based on a current state, returns all possible moves
    def nextMove(self):
        return True

    
    # 2d int position of a figure `s`
    def posInt(self, s):
        column = ord(s[0]) - ord('a')
        row = ord(s[1]) - ord('1')
        return column, row


    def posStr(self, col, row):
        """
        Given col & row, retrun a string in a chess notation
        eg. (1, 2) => 'b3'    (cols and rows are indexed from 0!)
        >>> ob = onboard('a1', 'b2', 'c3', 'black')
        >>> ob.posStr(1, 2)
        'b3'
        >>> col, row = ob.posInt('c2')
        >>> ob.posStr(col, row)
        'c2'
        """
        return str(chr(col + ord('a'))) + str(chr(row + ord('1'))) 

    
    # is a given position free?
    def isFree(self, col, row):
        return (col, row) != self.posInt(self.wk) and (col, row) != self.posInt(self.bk)
    
    # Fields attacked by white tower
    def whiteTowerAttacks(self):

        attacks = [self.wt]
        col, row = self.posInt(self.wt)

        # Check if sth is above the tower
        r = row - 1
        while r >= 0:
            attacks.append(self.posStr(col, r))
            if self.isFree(col, r) == False: break
            r -= 1  
            
        # Check BOT
        r = row + 1
        while r < 8:
            attacks.append(self.posStr(col, r))
            if self.isFree(col, r) == False: break
            r += 1  

        # Check LEFT
        c = col - 1
        while c >= 0:
            attacks.append(self.posStr(c, row))
            if self.isFree(c, row) == False: break
            c -= 1 

        # Check RIGHT
        c = col + 1
        while c < 8:
            attacks.append(self.posStr(c, row))
            if self.isFree(c, row) == False: break
            c += 1 

        return set(attacks)


    # Positions attacked by a king
    def kingAttacks(self, king):
        attacks = []
        col, row = self.posInt(king)
    
        attacks.append(self.posStr(col - 1, row - 1))   # top left
        attacks.append(self.posStr(col, row - 1))       # top top
        attacks.append(self.posStr(col + 1, row - 1))   # top right
        attacks.append(self.posStr(col - 1, row))       # left
        attacks.append(self.posStr(col + 1, row))       # right
        attacks.append(self.posStr(col - 1, row + 1))   # bot left
        attacks.append(self.posStr(col, row + 1))       # bot
        attacks.append(self.posStr(col + 1, row + 1))   # bot right

        return set(attacks) & self.board


    # Generate next white king move
    def movesWhiteKing(self):
        return self.kingAttacks(self.wk) - self.kingAttacks(self.bk) - set(self.wt)

    def movesBlackKing(self):
        return self.kingAttacks(self.bk) - self.kingAttacks(self.wk) - self.whiteTowerAttacks()
    
    def movesWhiteTower(self):
        return self.whiteTowerAttacks()

    def isCheckmate(self):
        return self.movesBlackKing() == set()

        
        



if __name__ == '__main__':
    
    finput  = 'input_1.1.txt'
    finput = 'data/ex1.test'
    # foutput = 'zad4_output.txt'

    # f2 = open(foutput,"w") 

    with open(finput) as f:
        for line in f:
            # Color, White King, White Tower, Black King
            col, wk, wt, bk = line.strip().split(" ")
            # OnBoard = onboard(wk, wt, bk, col)
            OnBoard = onboard( 'a3', 'b8', 'a1', 'white')            
            OnBoard.printb()
            print(OnBoard.movesWhiteKing())
            