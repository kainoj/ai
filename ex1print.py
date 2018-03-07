from pprint import pprint

figures = ('♔', '♖', '♚')

def pos2d(s):
    """
        s - position on the board, for example 'a3' or 'h8'
    """
    column = ord(s[0]) - ord('a')
    row = ord(s[1]) - ord('1')
    return column, row

def print_board( wk, wt, bk ):
	"""
	  wk - position of the white king
	  wt - position of the white tower
	  bk - position of the black king
	"""
	board = [ [' ' for i in range(8)] for j in range(8) ] 
	c,r = pos2d(wk)
	board[r][c] = figures[0]
	c,r = pos2d(wt)
	board[r][c] = figures[1]
	c,r = pos2d(bk)
	board[r][c] = figures[2]
	board =  [ [' '] +  [chr(j+97) for j in range(8)] ] + [ ([chr(j+49)] + board[j]) for j in range(8) ]
	pprint(board)
	#display(HTML(tabulate.tabulate(board, tablefmt='html').replace(
	#     '<table>', '<table style="border: 2px solid black;">').replace(
	#     '<td>'   , '<td    style="border: 1px solid black;">')
	#))

