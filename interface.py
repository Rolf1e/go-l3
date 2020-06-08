
from PIL import Image as Img
from PIL import ImageTk
import tkinter

import movelib
#import global_parameters
#import goban
import some_functions
import time
import playerlib

#Functions
def RBGAImage(path):
	return Img.open(path).convert("RGBA")

def IsACell(position):
	#position is a number
	if position < 0 or position > 360:
		return False
	else:
		return True
	
	
def quit_gui(event,root):
	textbox = tkinter.Tk(className="Are you sure?")
	haut = tkinter.Frame(textbox, borderwidth=0, relief=tkinter.GROOVE)
	haut.pack(side=tkinter.TOP, padx=10, pady=10)
	bas = tkinter.Frame(textbox, borderwidth=0, relief=tkinter.GROOVE)
	bas.pack(side=tkinter.TOP, padx=10, pady=10)
	tkinter.Message(haut,text="Etes vous sur de vouloir quitter?").pack(side=tkinter.LEFT, padx=5, pady=5)
	yes_button = tkinter.Button(bas, text ='Oui')
	yes_button.pack(side=tkinter.LEFT, padx=5, pady=5)
	yes_button.bind('<Button-1>', lambda event: close_two(event,textbox,root))
	no_button = tkinter.Button(bas, text ='Non')
	no_button.pack(side=tkinter.LEFT, padx=5, pady=5)
	no_button.bind('<Button-1>', lambda event: close_window(event,textbox))
	textbox.mainloop()
	
def close_window(event,window):
	window.destroy()

def close_two(event,textbox,root):	
	textbox.destroy()
	root.destroy()

class GUIClass:
	def __init__(self, name, Goban, Game):
		self.root = tkinter.Tk(className=name) # creates root window
		self.haut = tkinter.Frame(self.root, borderwidth=0, relief=tkinter.GROOVE)
		self.bas = tkinter.Frame(self.root, borderwidth=0, relief=tkinter.GROOVE)
		self.gauche = tkinter.Frame(self.bas, borderwidth=0, relief=tkinter.GROOVE)
		#self.canvas_goban = GUI_Goban(self)
		self.droite = tkinter.Frame(self.bas, borderwidth=0, relief=tkinter.GROOVE)
		self.move = tkinter.StringVar() #TODO: pas une tres bonne idee de nom
		self.goban = Goban
		self.game = Game
		
		self.canvas = tkinter.Canvas(self.gauche,width=600, height=600)
		gui_goban = RBGAImage("pictures/Goban_600px_19.gif")
		self.gui_imagetk = ImageTk.PhotoImage(gui_goban)
		self.gui_image = tkinter.Label(self.canvas, image=self.gui_imagetk)
		
	def initialize_goban(self):
		self.canvas.pack()
		self.gui_image.pack()
		if self.game.joueur_courant.couleur == 1:
			self.top_label.config(text = "A noir de jouer")
		else:
			self.top_label.config(text = "A blanc de jouer")
		
	def Launch(self):
		self.haut.pack(side=tkinter.TOP, padx=10, pady=10)
		self.top_label = tkinter.Label(self.haut, text="")
		self.top_label.pack(padx=10, pady=10)
		self.bas.pack(side=tkinter.BOTTOM, padx=10, pady=10)
		self.gauche.pack(side=tkinter.LEFT, padx=10, pady=10)
		self.droite.pack(side=tkinter.LEFT, padx=10, pady=10)
		self.right_label = tkinter.Label(self.droite, text="No prisoner yet")
		self.right_label.pack(side=tkinter.TOP, padx=10, pady=10)
		self.pass_button = tkinter.Button(self.droite, text ='Pass')
		self.pass_button.pack(side=tkinter.LEFT, padx=5, pady=5)
		quit_button = tkinter.Button(self.droite, text ='Quit')
		quit_button.pack(side=tkinter.LEFT, padx=5, pady=5)
		quit_button.bind('<Button-1>', lambda event: quit_gui(event, self.root))
	
	def GameOn(self):
		self.initialize_goban()
		self.move.trace("w", self.PlayMove)
		self.pass_button.bind('<Button-1>', lambda event: self.play(-1, self.goban, self.game))
		#First move :
		self.move.set(0)
		
	def PlayMove(self, *args):
		#add a stone in the goban:
		
		if not isinstance(self.game.joueur_courant, playerlib.IA):
			self.gui_image.bind("<Button-1>", lambda event: self.human_plays(event, self.goban, self.game))
		else:
			coord = self.game.joueur_courant.donne_coup(self.game)
			self.play(coord, self.goban, self.game)

		return True
		
	def End(self):
		self.root.mainloop() 
		
	def play(self, coord, Goban, Game):
		#PlayMove(coord,Goban,Game)			 
		couleurstr = couleur_to_couleurstr(Game.joueur_courant.couleur)
		if coord == -1: #code for passing
			message = "Coup numéro "+str(Game.move)+": "+couleurstr+" passe. "
			Game.jouer(-1)
			message = message+"A "+couleurstr+" de jouer."
			self.top_label.config(text = message)
		
			self.update(Goban, Game)
			if Game.move > 1 and Game.moves[-2] == -1: #2 pass de suite, fin du jeu
				s = Game.score()
				print('Fin de la partie! ')
				if s > 0:
					print('Blanc gagne avec '+str(s)+' points.')
				elif s < 0:
					print('Noir gagne avec '+str(-s)+' points.')
				elif s == 0:
					print('La partie est à égalité!')
				else:
					print('Un résultat surnaturel : '+str(s))
					
			else:
				self.PlayMove()
		else:
			
			if not isinstance(self.game.joueur_courant, playerlib.IA) or 1==1:
				message = "Move number "+str(Game.move+1)+": "+couleurstr+" plays at "+some_functions.CoordToPosition(coord, Game.size)+'. '
				message += couleurstr+" to play."
				self.top_label.config(text = message)
			
			Game.jouer(coord)
			self.update(Goban, Game)
			if isinstance(self.game.noir, playerlib.IA) and isinstance(self.game.blanc, playerlib.IA):
				pass#here later put to sleep
			self.PlayMove()
			
			message = "Black prisoners: "+str(Game.score_black)+".\n White prisoners: "+str(Game.score_white)+"."
			self.right_label.config(text = message)
			
	def human_plays(self,event,Goban, Game):
		coord = some_functions.GuiToCoord(event.x,event.y)
		if coord == False:
			return False
		else:
			if movelib.IsValidMove(coord,Goban,Game):
				self.play(coord, Goban, Game)  
				return True
			else:
				return False  
			
	def update(self,Goban,Game):
		gui_goban = RBGAImage("pictures/Goban_600px_19.gif")
		gui_stone_white = RBGAImage("pictures/stone_white.gif")
		gui_stone_black = RBGAImage("pictures/stone_black.gif")
		gui_stone_white_current = RBGAImage("pictures/stone_white_current.gif")
		gui_stone_black_current = RBGAImage("pictures/stone_black_current.gif")
		if Game.move > 0:
			last_move = Game.moves[-1]
		else:
			last_move = [Game.size,Game.size]
		
		for i in range(Goban.size):
			for j in range(Goban.size):
				if Goban.cells[i][j].color==1:
					gui_goban.paste(gui_stone_black, (some_functions.CoordToGui(i,j)[0], some_functions.CoordToGui(i,j)[1]), gui_stone_black)		
					if last_move != -1:
						if i==last_move[0] and j==last_move[1]:
							gui_goban.paste(gui_stone_black_current, (some_functions.CoordToGui(i,j)[0], some_functions.CoordToGui(i,j)[1]), gui_stone_black_current)
					
				elif Goban.cells[i][j].color==-1:
					gui_goban.paste(gui_stone_white, (some_functions.CoordToGui(i,j)[0], some_functions.CoordToGui(i,j)[1]), gui_stone_white)		
					if last_move != -1:
						if i==last_move[0] and j==last_move[1]:
							gui_goban.paste(gui_stone_white_current, (some_functions.CoordToGui(i,j)[0], some_functions.CoordToGui(i,j)[1]), gui_stone_white_current)

		
		self.gui_imagetk = ImageTk.PhotoImage(gui_goban)
		self.gui_image.config(image = self.gui_imagetk)
		
		
def couleur_to_couleurstr(c):
	if c == 1:
		return "noir"
	else:
		return "blanc"