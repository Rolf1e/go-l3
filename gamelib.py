import playerlib
import gobanlib
import copy
import interface



class GameClass:
	def __init__(self, size, komi, opts={}):
		self.size = size # will initiate Goban class
		self.komi = komi
		self.move = 0
		self.moves = [] # list of all moves in the order
		
		self.gopositions = [] # list of all positions of the Goban (this is to avoid ko)
		self.color = 1 # 1 for black and -1 for white
		#TODO: change self.color to current_player_color or current_player
		self.score_black = 0
		self.score_white = 0
		self.goban = gobanlib.GobanClass(self)
		
			
		self.noir = None
		self.blanc = None
		if ("choix_joueurs" not in opts or opts["choix_joueurs"]):
			possibilites = [playerlib.Humain] + playerlib.IA.__subclasses__()
			if len(possibilites) == 1:
				print("Un seul type de joueur est actuellement implémenté : "+
					  str(possibilites[0])+".\nCe type sera choisi pour noir et blanc.")
				self.noir = possibilites[0](self, 1)
				self.blanc = possibilites[0](self, -1)
			else:
				print("Quel type de joueur souhaitez vous sélectionner pour noir ?",
					  "Les possibilités sont :")
				for i in range(len(possibilites)):
					print(i+1," : "+str(possibilites[i]))
				choix = input("Tapez le nombre correspondant.\n")
				self.noir = possibilites[int(choix)-1](self, 1)
				print("Quel type de joueur souhaitez vous sélectionner pour blanc ?\nLes possibilités sont :")
				for i in range(len(possibilites)):
					print(i+1," : "+str(possibilites[i]))
				choix = input("Tapez le nombre correspondant.\n")
				self.blanc = possibilites[int(choix)-1](self, -1)
		
		self.joueur_courant = self.noir
		
		self.partie_finie = False
		self.coord_last_loner_captured = None
		
	def lance_gui(self):
		gui = interface.GUIClass("Go", self.goban, self)
		gui.root.mainloop()

	def jouer(self,coord):
		'''jouer(coord). joue le coup coord, échange les joueurs et vérifie si la partie est finie.'''
		self.coord_last_loner_captured = None
		self.flag_superficialKO = False
		if coord != -1:
			self.goban.play(coord)
			self.move += 1
			self.moves.append(coord)
		else:
			if len(self.moves)>0 and self.moves[-1] == -1:
				self.partie_finie = True
			self.moves.append(-1)
		self.color *= -1
		if self.color == 1:
			self.joueur_courant = self.noir
		else:
			self.joueur_courant = self.blanc

		return True

	def copy(self):
		'''Rend une copie du jeu, dont le goban est lui même une copie. Les joueurs ne sont pas des copies.'''
		new_game = GameClass(self.size, self.komi, {"choix_joueurs":False})
		new_game.partie_finie = self.partie_finie
		new_game.noir = self.noir
		new_game.blanc = self.blanc
		new_game.joueur_courant = self.joueur_courant
		new_game.color = self.color
		new_game.move = self.move
		new_game.moves = copy.deepcopy(self.moves)
		new_game.goban = self.goban.copy(False)
		new_game.goban.game = new_game
		if len(self.gopositions) > 0:
			new_game.gopositions = copy.deepcopy([self.gopositions[-1]])
		new_game.score_black = self.score_black
		new_game.score_white = self.score_white
		#new_game.flag_superficialKO = self.flag_superficialKO
		return new_game
		
	def score(self):
		'''La méthode score() renvoie le nombre de points de noir moins ceux de blanc.'''
		s = 0
		for i in range(self.size):
			for j in range(self.size):
				s += self.goban.cells[i][j].color
		s -= self.komi
		s += self.score_black - self.score_white
		return s
		
