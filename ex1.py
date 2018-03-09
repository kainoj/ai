from ex1print import print_board

class onboard():
    
    def __init__(self, wk, wt, bk, col):
        self.wk = wk
        self.wt = wt
        self.bk = bk
        self.col = col
    
    # Prints the board
    def printb(self):
        print("Next move: " + col)
        print_board(self.wk, self.wt, self.bk)
    
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


    # True if a figure `f` is on board
    def isOnBoard(self, col, row):
        return 1 <= col and col <= 8 and 1 <= row and row <= 8

    # Generate next king's move
    def moveWhiteKing(self, king):
        moves = []
        col, row = self.posInt(king)
        # top left
        if self.isOnBoard(col - 1, row - 1):
            moves.append(self.posStr(col - 1, row - 1))
        
        # top top
        if self.isOnBoard(col, row - 1):
            moves.append(self.posStr(col, row - 1))

        # top right
        if self.isOnBoard(col + 1, row - 1):
            moves.append(self.posStr(col + 1, row - 1))

        # left
        if self.isOnBoard(col - 1, row):
            moves.append(self.posStr(col - 1, row))
        
        # right
        if self.isOnBoard(col + 1, row):
            moves.append(self.posStr(col + 1, row))
        
        # bot left
        if self.isOnBoard(col - 1, row + 1):
            moves.append(self.posStr(col - 1, row + 1))

        # bot
        if self.isOnBoard(col, row + 1):
            moves.append(self.posStr(col, row + 1))

        # bot right
        if self.isOnBoard(col + 1, row + 1):
            moves.append(self.posStr(col + 1, row + 1))       

        
    
        

        
        



if __name__ == '__main__':
    
    finput  = 'input_1.1.txt'
    finput = 'data/ex1.test'
    # foutput = 'zad4_output.txt'

    # f2 = open(foutput,"w") 

    with open(finput) as f:
        for line in f:
            # Color, White King, White Tower, Black King
            col, wk, wt, bk = line.strip().split(" ")
            OnBoard = onboard(wk, wt, bk, col)
            OnBoard.printb()
            OnBoard.moveWhiteKing(wk)
