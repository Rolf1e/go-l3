#import goban

lettre = "ABCDEFGHJKLMNOPQRST"
sgf_lettre = "abcdefghijklmnopqrs"

def SgfToGoban(position,size):
	#sgf position format is with 2 small letters
	#Goban format is a number, from 0 (A1) to 360 (T19)
	x = sgf_lettre.find(position[0])
	y = sgf_lettre.find(position[1])
	return x+size*y
	
def GobanToSgf(position,size):
	#Goban format is a number, from 0 (A1) to 360 (T19)
	#sgf position format is with 2 small letters
	x = position % size
	y = position // size
	return sgf_lettre[x]+sgf_lettre[y]
	
def GobanToPosition(position,size):
	#Goban format is a number, from 0 (A1) to 360 (T19)
	#Position is from A1 to T19
	x = position % size
	y = position // size
	return lettre[x]+str(size-y)

def GuiToGoban(x,y,size):
	#Gui Coordinates are coordinates in the image of the goban (x and y)
	#Goban format is a number, from 0 (A1) to 360 (T19)
	#return 361 if not on a cell
	reste_x = (x-60)%28.333
	reste_y = (y-59)%28.333
	if (reste_x < 10 or reste_x > 18.333) and (reste_y < 10 or reste_y > 18.333) and (x>50) and (y>50) and (x<580) and (y<580):
		# We are on a cell!
		l = int(round((y-59)/28.333))
		c = int(round((x-60)/28.333))
		return l*size+c
	else:
		return 361
		
def GuiToCoord(x,y):
	#Gui Coordinates are coordinates in the image of the goban (x and y)
	#Coord are coordinates in Goban
	#return False if not a cell
	reste_x = (x-60)%28.333
	reste_y = (y-59)%28.333
	if (reste_x < 10 or reste_x > 18.333) and (reste_y < 10 or reste_y > 18.333) and (x>50) and (y>50) and (x<580) and (y<580):
		# We are on a cell!
		c = int(round((x-60)/28.333))
		l = int(round((y-59)/28.333))
		coord = [l,c]
		return coord
	else:
		return False
		
def CoordToGui(i,j):
	#Coord are coordinates i,j from 0 to goban.size
	#Gui Coordinates are coordinates in the image of the goban (x and y)
	x = int(round(44+j*28.333))
	y = int(round(43+i*28.333))
	return [x,y]

def CoordToPosition(coord,size):
	#Coord are coordinates i,j from 0 to goban.size
	#Position is from A1 to T19
	return lettre[coord[1]]+str(size-coord[0])
	
def Player(color):
	#return Black or White
	return "Black" if color == -1 else "White"




def PrintControl(Goban):
	#Print the Goban in the console for control (only in development)
	#Print Goban
	car_sequence = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
	top_print = '  '
	big_top_print = '	'
	for a in car_sequence[:Goban.size]:
		top_print += a
		big_top_print += a
		top_print += ' '
		big_top_print += '   '
	print("")
	print("Goban:")
	print("")
	print(top_print+'\n')
	for i in range(Goban.size):
		print(" ", end=" ")
		for j in range(Goban.size):
			if Goban.cells[i][j].color==1:
				print("@", end=" ")
			elif  Goban.cells[i][j].color==-1:
				print("O", end=" ")
			else:
				print(".", end=" ")
		print(" " + str(Goban.size-i))
	#Print Group
	print("")
	print("Groups:")
	print("")
	print(big_top_print)
	print("")
	for i in range(Goban.size):
		print(" ", end=" ")
		for j in range(Goban.size):
			if Goban.cells[i][j].id_group == None:
				print (end="  . ")
			else:
				size = len(str(Goban.cells[i][j].id_group))
				for k in range(3-size):
					print (end=" ")
				print(Goban.cells[i][j].id_group, end=" ")
		print(" " + str(Goban.size-i))
		print("")
	#Print Liberties
	print("")
	print("Liberties:")
	print("")
	print(top_print)
	print("")
	for i in range(Goban.size):
		print(" ", end=" ")
		for j in range(Goban.size):
			print(Goban.cells[i][j].liberties, end=" ")
		print(" " + str(Goban.size-i))
	print("")
	return 0
	
	
	
def print_board(board, message=''):
	print(message)
	size = len(board)
	car_sequence = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
	boardtype = int
	for a in board:
		for b in a:
			if type(b) == float:
				boardtype = float
	if boardtype == float:
		top_print = '   '
		for a in car_sequence[:size]:
			top_print += a
			top_print += '	 '
	else:
		lenmax = len(str(max([max(a) for a in board])))
		top_print = ' '*(lenmax - 1)
		for a in car_sequence[:size]:
			top_print += a
			top_print += ' '*lenmax
	print(top_print+'		\n')
	for i in range(size):
		for j in range(size):
			if boardtype == float:
				if board[i][j] >= 0:
					print(" %.3f" % board[i][j], end=' ')
				else:
					print("%.3f" % board[i][j], end=' ')
			else:
				s = str(board[i][j])
				print(' '*(lenmax - len(s)) + s, end=' ')
		print('  ' + str(i+1))
	print('\n')
