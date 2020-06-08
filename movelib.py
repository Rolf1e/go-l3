#import global_parameters
#import goban
#import some_functions
#import interface
import copy
#from random import randint

def IsValidMove(coord,Goban,Game):
	#Game = Goban.Game
	#Is it a valid move (no stone here, no suicide)
	if Goban.cells[coord[0]][coord[1]].color !=0:
		#There is a stone here!
		return False
	else:
		#Should not be a suicide
		if IsSuicide(coord, Goban, Game):
			return False
		else:
			#Should not be a ko		
			return not IsKo(coord,Goban,Game)

def IsEye(coord,Goban,Game):
	"""IsEye(coord, Goban, Game)
	Returns True if the intersection at coordinates coord is an eye of the current player, that if it is empty, and surrounded by stones of the current player. Returns False otherwise."""
	current_cell = Goban.cells[coord[0]][coord[1]]
	if current_cell.color != 0:
		return False
	voisins = current_cell.adjacent_cells.values()
	for c in voisins:
		if Game.color != c.color:
			return False
	return True



def IsKo(coord,Goban,Game):#superficial KO activated
	if Game.flag_superficialKO:
		return Game.coordoflastlonercaptured == coord
	return False

def IsSuicide(coord,Goban,Game):
	# It is suicide if there is an adjacent group of same color with only 1 liberty
	# and no adjacent group of the other color with only 1 liberty
	# and the case has 0 liberty
	current_cell = Goban.cells[coord[0]][coord[1]]
	if current_cell.liberties > 0:
		return False
	else:	
		#0 liberty
		players_groups = []
		opponents_groups = []
		for c in current_cell.adjacent_cells.values():
			#c.liberties -= 1 #PJ: ajoute ça pour corriger bug suicide
			if c.color == Game.color and c.id_group not in players_groups:
				players_groups.append(c.id_group)
			if c.color == -Game.color and c.id_group not in opponents_groups:
				opponents_groups.append(c.id_group)
		kill = False
		# first case: are we killing a group?
		if len(opponents_groups)>0:
			for o_g in opponents_groups:
				if Goban.groups[o_g].nb_liberties == 1:
					kill = True
		if kill:
			return False
		else:			
			#second case: has any of the player's group more than one liberty
			for p_g in players_groups:
				if Goban.groups[p_g].nb_liberties > 1:
					return False
			#print ("Suicide is forbidden by the god of Go Game!")
			return True