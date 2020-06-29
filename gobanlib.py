
import some_functions
import movelib

class GobanClass():
	
	def __init__(self, game):
		self.game = game
		self.size = game.size
		self.cells = [[CellClass([i, j], self) for j in range(self.size)] for i in range(self.size)]
		self.link_cells() #a faire apres l'initialisation des cells
		self.groups = {} # elements of this dictionary are objects of class Group.
		self.last_group_id = 0 # will be incremented at every new group
		self.free_coords = [[i//self.size, i%self.size] for i in range(self.size**2)]

	def play(self, coord, fake=False):
		cell = self.cells[coord[0]][coord[1]]
		cell.color = self.game.color
		self.free_coords.remove(coord)
		
		players_groups = []
		opponents_groups = []
		for c in cell.adjacent_cells.values():
			c.liberties -= 1
			if c.color == self.game.color and c.id_group not in players_groups:
				players_groups.append(c.id_group)
			if c.color == -self.game.color and c.id_group not in opponents_groups:
				opponents_groups.append(c.id_group)
		
		for g_id in opponents_groups:
			self.groups[g_id].remove_liberty(cell, fake)
		
		#npas de merge
		if len(players_groups) == 0:
			g = GroupClass(cell, self, self.last_group_id)
			self.last_group_id += 1
			self.groups[g.id] = g
		else:#merge
			g = self.groups[players_groups[0]]
			g.cells.append(cell)
			liberties = cell.list_free_cells()
			for l in liberties:
				if l not in g.liberties:
					g.liberties.append(l)
					g.nb_liberties += 1
			cell.id_group = g.id
			cell.in_group = g
					
			for other_g_id in players_groups[1:]:
				self.groups[other_g_id].merge_into(g)
				
			g.liberties.remove(cell)
			g.nb_liberties -= 1
			
			
	def link_cells(self):
		for i in range(self.size):
			for j in range(self.size):
				self.cells[i][j].link()

	def to_matrix(self):
		"""Returns the size per size matrix of stones representing the goban."""
		return [[c.color for c in column] for column in self.cells]

	def copy(self, copie_jeu=True):
		'''rend une copie du goban, utilisable pour des simulations ou tester pour un ko sans modifier le goban initial.'''
		if copie_jeu:
			new_goban = GobanClass(self.game.copy())
			new_goban.game.goban = new_goban#the new game created its own goban, which needs to be replaced
		else:
			new_goban = GobanClass(self.game)
		new_goban.last_group_id = self.last_group_id
		for i in range(self.size):
			for j in range(self.size):
				new_goban.cells[i][j] = self.cells[i][j].copy(new_goban) #copie les cases mais ne les lie pas entre elles ni avec les groupes
		for i in range(self.size):
			for j in range(self.size):
				new_goban.cells[i][j].link() #doit etre fait apres la creation des cells. Lie avec les cellules adjacentes et initialise le nombre de libertes
		#new_goban.groups = {}
		
		for g in self.groups.values():
			if g.active: #sinon le groupe est mort et flotte dans le néant. Et devrait se faire garbage collecter.
				new_goban.groups[g.id] = g.copy(new_goban) #this also links the new cells to their group
		new_goban.last_group_id = self.last_group_id
		return new_goban
	
	def liste_coups_oks(self):
		'''liste_coups_oks() rend la liste des coups valides qui ne sont pas des yeux
		en testant si chaque case libre est un coup valide et pas un oeil, y compris passer. A ne pas trop utiliser.'''
		candidats = [c for c in self.free_coords]
		coups = []
		for c in candidats:
			if movelib.IsValidMove(c, self, self.game) and not movelib.IsEye(c, self, self.game):
				coups.append(c)
		return coups + [-1]
	
	def liste_cases_libres(self):
		return self.free_coords

		
class GroupClass():

	def __init__(self, cell, goban, id_group):
		self.active = True #after killed, change to False
		self.goban = goban
		self.color = cell.color # -1 for black, 1 for white
		self.cells = [cell]
		self.id = id_group
		self.liberties = cell.list_free_cells()
		self.nb_liberties = len(self.liberties) #PJ: normally it should be also cell.liberties which is a number
		
		cell.in_group = self
		cell.id_group = id_group
		
	def remove_liberty(self, cell, fake=False):
		self.nb_liberties -= 1
		self.liberties.remove(cell)
		if self.nb_liberties == 0: #capture time
			self.autodestruction(fake)
			
	def autodestruction(self, fake=False):
		if len(self.cells) == 1: #if only one cell was captured, it could be a possibility for a KO next move.
			self.goban.game.coord_last_loner_captured = self.cells[0].coord
		#tracking prisonners points
		if self.color == 1 and not fake:
			self.goban.game.score_white += len(self.cells)
		elif self.color == -1 and not fake:
			self.goban.game.score_black += len(self.cells)
		
		#PJ: to correct bug for suicide
		for c in self.cells:
			for d in c.adjacent_cells.values():
				d.liberties+=1
		#resetting group's cells and recounting liberties
		for c in self.cells:
			c.make_cell_liberty()
	
		#removing group
		del self.goban.groups[self.id]
		self.active = False #mieux vaut carrement supprimer le groupe non ?
		
	def	merge_into(self, other):
		for c in self.cells:
			other.cells.append(c)
			c.id_group = other.id
			c.in_group = other
		for l in self.liberties:
			if l not in other.liberties:
				other.liberties.append(l)
				other.nb_liberties += 1
		del self.goban.groups[self.id]
		self.active = False
			
	#def __eq__(self, other):
	#	return self.id == other.id
	
	def copy (self,goban):
		oldcell = self.cells[0] #be careful not to create links
		new_group = GroupClass(goban.cells[oldcell.coord[0]][oldcell.coord[1]], goban, self.id)
		#new_group.active = self.active
		#new_group.goban = goban
		#new_group.color = self.color # ca devrait avoir été fait dans l'initialisation aussi
		new_group.cells = []
		new_group.liberties = []
		for c in self.cells:
			new_c = goban.cells[c.coord[0]][c.coord[1]]
			new_group.cells.append(new_c)
			new_c.in_group = self
			new_c.id_group = self.id
		for l in self.liberties:
			new_group.liberties.append(goban.cells[l.coord[0]][l.coord[1]])
		#for i in range(goban.size):
		#	for j in range(goban.size):
		#		if goban.cells[i][j].id_group == self.id:
		#			new_group.cells.append(goban.cells[i][j])
		#		if self.goban.cells[i][j] in self.liberties:
		#			new_group.liberties.append(goban.cells[i][j])
		#new_group.id = self.id
		new_group.nb_liberties = self.nb_liberties
		return new_group
	

	
class CellClass():

	def __init__(self, coord, goban):
		self.goban = goban
		self.coord = coord
		self.color = 0 # 0 pour vide, -1 pour noir 1 pour blanc
		self.in_group = None #groupe auquel la cell appartient
		self.id_group = None #self.in_group = goban.groups[self.id_group]
		#self.is_liberty_of = [] #liste des groupes dont la cell est une liberté
		#self.est_oeil
		
	#only to be used at initialisation
	def link(self):
		self.adjacent_cells = {}
		if self.coord[1] < self.goban.size - 1:
			self.adjacent_cells['right'] = self.goban.cells[self.coord[0]][self.coord[1] + 1]
		if self.coord[1] > 0:
			self.adjacent_cells['left'] = self.goban.cells[self.coord[0]][self.coord[1] - 1]
		if self.coord[0] < self.goban.size - 1:
			self.adjacent_cells['down'] = self.goban.cells[self.coord[0] + 1][self.coord[1]]
		if self.coord[0] > 0:
			self.adjacent_cells['up'] = self.goban.cells[self.coord[0] - 1][self.coord[1]]
		
		self.liberties = 0
		for c in self.adjacent_cells.values():
			if c.color == 0:
				self.liberties += 1

	def list_free_cells(self):
		l = []
		for c in self.adjacent_cells.values():
			if c.color == 0:
				l.append(c)
		return l
		
	def make_cell_liberty(self):
		if self.color == 0:
			return False #error: the cell is already free
		self.color = 0
		self.goban.free_coords.append(self.coord)
		self.in_group = None
		self.id_group = None
		
		groups_id = []
		for c in self.adjacent_cells.values():
			#c.liberties += 1
			if c.id_group != None and c.id_group not in groups_id:
				groups_id.append(c.id_group)
		
		for g_id in groups_id:
			if self not in self.goban.groups[g_id].liberties:
				self.goban.groups[g_id].liberties.append(self)
				self.goban.groups[g_id].nb_liberties += 1
		
		
	def __eq__(self, other):
		return self.coord == other.coord
	
	def copy(self, goban):
		new_cell = CellClass(self.coord, goban)
		new_cell.color = self.color
		new_cell.id_group = self.id_group
		new_cell.liberties = self.liberties
		return new_cell







