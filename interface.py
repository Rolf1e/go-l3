
from PIL import Image
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
	return Image.open(path).convert("RGBA")
	
	
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
	def __init__(self, name, goban, game):
		self.goban = goban
		self.game = game
		
		self.root = tkinter.Tk(className=name) # creates root window
		
		self.window_height = 500
		self.window_width = 700
		self.root.title("Go")
		self.root.geometry(str(self.window_width)+"x"+str(self.window_height))
		self.root.configure(background='grey')
		
		self.hspace = 1
		self.top = tkinter.Frame(self.root, borderwidth=0, relief=tkinter.GROOVE)
		self.top.grid(row=0, column=0, rowspan=self.hspace, columnspan=self.game.size)
		self.goban_frame = tkinter.Frame(self.root, borderwidth=0, relief=tkinter.GROOVE)
		self.goban_frame.grid(row=1, column=0, rowspan=self.game.size, columnspan=self.game.size)
		self.goban_label = tkinter.Label(self.goban_frame, borderwidth = 0, highlightthickness = 0)
		self.goban_label.grid()
		self.right = tkinter.Frame(self.root, borderwidth=0, relief=tkinter.GROOVE)
		self.right.grid(row=0, column=self.game.size, rowspan=self.game.size+self.hspace, columnspan=3)
		
		self.square_size = int(self.window_height / (self.game.size + self.hspace))
		
		self.top_label = tkinter.Label(self.top, text="Début de partie. A noir de jouer.")
		self.top_label.pack()
		self.right_label = tkinter.Label(self.right, text="Prisonniers capturés par noir : 0\nPrisonniers capturés par blanc : 0")
		self.right_label.grid(row=max(0,int(self.game.size//2)-2), rowspan=2, columnspan=3)
		
		self.min_wait_ai = 0.3 #temps minimum pour un coup de l'ia si deux ias
		
		self.load_images()
		self.draw_goban()
		self.add_quit_button()
		self.flag_two_ais = False
		self.flag_continue = True
		if not isinstance(self.game.noir, playerlib.Humain) and not isinstance(self.game.blanc, playerlib.Humain):
			self.flag_two_ais = True
		self.flag_human_active = False
		if isinstance(self.game.joueur_courant, playerlib.Humain):
			self.activate_human()
		else:
			self.add_start_button()
		#self.root.mainloop()
		#self.canvas = tkinter.Canvas(self.gauche, width=600, height=600)
		#gui_goban = RBGAImage("pictures/Goban_600px_19.gif")
		#self.gui_imagetk = ImageTk.PhotoImage(gui_goban)
		#self.gui_image = tkinter.Label(self.canvas, image=self.gui_imagetk)
	
	def add_start_button(self):
		self.start_button = tkinter.Button(self.right, text ='Start')
		self.start_button.grid(row=0, column=0)
		self.start_button.bind('<Button-1>', lambda event: self.start_game())
		
	def start_game(self):
		self.flag_continue = True
		self.start_button.destroy()
		self.add_stop_button()
		self.ai_plays()
		
	def add_stop_button(self):
		self.stop_button = tkinter.Button(self.right, text ='Stop')
		self.stop_button.grid(row=0, column=0)
		self.stop_button.bind('<Button-1>', lambda event: self.stop_game())
		
	def stop_game(self):
		self.flag_continue = False
		self.stop_button.destroy()
		self.add_start_button()
	
	def add_pass_button(self):
		self.pass_button = tkinter.Button(self.right, text ='Pass')
		self.pass_button.grid(row=int(self.game.size//2)+1, column=0)
		self.pass_button.bind('<Button-1>', lambda event: self.human_plays(None))
		
	def add_quit_button(self):
		self.quit_button = tkinter.Button(self.right, text ='Quit')
		self.quit_button.grid(row=int(self.game.size//2)+1, column=1)
		self.quit_button.bind('<Button-1>', lambda event: quit_gui(event, self.root))
		
	def load_images(self):
		f_hg = "images/plateau_hg.png"
		f_h = "images/plateau_h.png"
		f_hd = "images/plateau_hd.png"
		f_d = "images/plateau_d.png"
		f_bd = "images/plateau_bd.png"
		f_b = "images/plateau_b.png"
		f_bg = "images/plateau_bg.png"
		f_g = "images/plateau_g.png"
		f_c = "images/plateau_c.png"
		
		imgtk_hg = Image.open(f_hg).resize((self.square_size, self.square_size), Image.ANTIALIAS).convert("RGBA")
		imgtk_h = Image.open(f_h).resize((self.square_size, self.square_size), Image.ANTIALIAS).convert("RGBA")
		imgtk_hd = Image.open(f_hd).resize((self.square_size, self.square_size), Image.ANTIALIAS).convert("RGBA")
		imgtk_d = Image.open(f_d).resize((self.square_size, self.square_size), Image.ANTIALIAS).convert("RGBA")
		imgtk_bd = Image.open(f_bd).resize((self.square_size, self.square_size), Image.ANTIALIAS).convert("RGBA")
		imgtk_b = Image.open(f_b).resize((self.square_size, self.square_size), Image.ANTIALIAS).convert("RGBA")
		imgtk_bg = Image.open(f_bg).resize((self.square_size, self.square_size), Image.ANTIALIAS).convert("RGBA")
		imgtk_g = Image.open(f_g).resize((self.square_size, self.square_size), Image.ANTIALIAS).convert("RGBA")
		imgtk_c = Image.open(f_c).resize((self.square_size, self.square_size), Image.ANTIALIAS).convert("RGBA")
		
		self.img_goban = Image.new("RGBA", (self.game.size * self.square_size, self.game.size * self.square_size))
		self.img_goban.paste(imgtk_hg, (0,0))
		self.img_goban.paste(imgtk_hd, ((self.game.size-1)*self.square_size,0))
		self.img_goban.paste(imgtk_bd, ((self.game.size-1)*self.square_size,(self.game.size-1)*self.square_size))
		self.img_goban.paste(imgtk_bg, (0,(self.game.size-1)*self.square_size))
		for i in range(1, self.game.size-1):
			self.img_goban.paste(imgtk_h, (i*self.square_size,0))
			self.img_goban.paste(imgtk_d, ((self.game.size-1)*self.square_size,i*self.square_size))
			self.img_goban.paste(imgtk_b, (i*self.square_size,(self.game.size-1)*self.square_size))
			self.img_goban.paste(imgtk_g, (0,i*self.square_size))
			for j in range(1, self.game.size-1):
				self.img_goban.paste(imgtk_c, (i*self.square_size,j*self.square_size))
		
		f_black = "images/stone_black.png"
		f_black_last = "images/stone_black.png"
		f_white = "images/stone_white.png"
		f_white_last = "images/stone_white.png"
		
		self.img_black = Image.open(f_black).resize((self.square_size, self.square_size), Image.ANTIALIAS).convert("RGBA")
		self.img_white = Image.open(f_white).resize((self.square_size, self.square_size), Image.ANTIALIAS).convert("RGBA")
		self.img_black_last = Image.open(f_black_last).resize((self.square_size, self.square_size), Image.ANTIALIAS).convert("RGBA")
		self.img_white_last = Image.open(f_white_last).resize((self.square_size, self.square_size), Image.ANTIALIAS).convert("RGBA")
		
		
	def draw_goban(self):
		
		self.full_img_goban = Image.new("RGBA", (self.game.size * self.square_size, self.game.size * self.square_size))
		self.full_img_goban.paste(self.img_goban)
				
		for i in range(self.game.size):
			for j in range(self.game.size):
				if self.goban.cells[i][j].color == 1:
					self.full_img_goban.paste(self.img_black, (i*self.square_size, j*self.square_size), self.img_black)
				elif self.goban.cells[i][j].color == -1:
					self.full_img_goban.paste(self.img_white, (i*self.square_size, j*self.square_size), self.img_white)
					
		if len(self.game.moves) > 0:
			if self.game.moves[-1] != -1:
				coord = self.game.moves[-1]
				if self.goban.cells[coord[0]][coord[1]].color == 1:
					self.full_img_goban.paste(self.img_black_last, (coord[0]*self.square_size, coord[1]*self.square_size), self.img_black_last)
				elif self.goban.cells[coord[0]][coord[1]].color == -1:
					self.full_img_goban.paste(self.img_white_last, (coord[0]*self.square_size, coord[1]*self.square_size), self.img_white_last)
		self.full_img_goban = ImageTk.PhotoImage(self.full_img_goban)
		self.goban_label.configure(image=self.full_img_goban)
		
	def activate_goban(self):
		self.goban_label.bind("<Button-1>", lambda event: self.human_plays(event))
	
	def activate_human(self):
		self.flag_human_active = True
		self.activate_goban()
		self.add_pass_button()
		
	def deactivate_human(self):
		self.flag_human_active = False
		self.goban_label.unbind("<Button-1>")
		self.pass_button.destroy()
			
	def human_plays(self, event):##,Goban, Game):
		flag_played = False
		if event is None:
			self.game.jouer(-1)
			flag_played = True
		else:
			coord = self.event_to_coord(event)
			if coord is not None:
				if movelib.IsValidMove(coord, self.goban, self.game):
					self.game.jouer(coord)
					flag_played = True
		if flag_played:
			self.update_interface()
			if not isinstance(self.game.joueur_courant, playerlib.Humain) and not self.game.partie_finie:
				self.ai_plays()
		'''coord = some_functions.GuiToCoord(event.x,event.y)
		if coord == False:
			return False
		else:
			if movelib.IsValidMove(coord,Goban,Game):
				self.play(coord, Goban, Game)  
				return True
			else:
				return False  '''
		
	def ai_plays(self):
		start = time.time()
		ai_move = self.game.joueur_courant.donne_coup(self.game)
		end = time.time()
		if self.flag_two_ais and end-start < self.min_wait_ai:
			time.sleep(self.min_wait_ai - end + start)
		self.game.jouer(ai_move)
		self.update_interface()
		if not isinstance(self.game.joueur_courant, playerlib.Humain) and\
			self.flag_continue:
			if self.game.partie_finie:
				self.stop_button.destroy()
			else:
				self.ai_plays()
		
	def update_interface(self):
		self.draw_goban()
		if self.game.joueur_courant.color == 1:
			color = "noir"
			previous = "blanc"
		else:
			color = "blanc"
			previous = "noir"
		if self.game.partie_finie:
			msg_turn = "La partie est terminée !"
		else:
			msg_turn = "A "+color+" de jouer."
		if self.game.moves[-1] == -1:
			msg_move = previous+" a passé. "
		else:
			msg_move = previous+" a joué en "+str(self.game.moves[-1])+". "
		if self.game.partie_finie:
			score = self.game.score()
			if score > 0:
				msg_victoire = "Noir gagne la partie de "+str(score)+" points."
			elif score < 0:
				msg_victoire = "Blanc gagne la partie avec "+str(-score)+" points."
			else:
				msn_victoire = "La partie est un match nul."
			self.top_label.config(text=msg_move+msg_turn+'\n'+msg_victoire)
		else:
			self.top_label.config(text=msg_move+msg_turn)
		msg_score_black = "Prisonniers capturés par noir : "+str(self.game.score_black)+"."
		msg_score_white = "Prisonniers capturés par blanc : "+str(self.game.score_white)+"."
		self.right_label.config(text=msg_score_black+'\n'+msg_score_white)
		if self.flag_human_active and (self.game.partie_finie or not 
									   isinstance(self.game.joueur_courant, playerlib.Humain)):
			self.deactivate_human()
		elif not self.flag_human_active and not self.game.partie_finie\
			and isinstance(self.game.joueur_courant, playerlib.Humain):
			self.activate_human()
		self.root.update()
	
		
	def event_to_coord(self, event):
		"""Prend un event, et rend les coordonnées correspondantes sur le goban, 
		ou None si l'event ne correspond pas à un clic sur le goban."""
		coord = [int(event.x / self.square_size), int(event.y / self.square_size)]
		if coord[0] >= self.game.size or coord[1] < 0:
			return None
		else:
			return coord		
		
def couleur_to_couleurstr(c, maj=False):
	if c == 1:
		if maj:
			return "Noir"
		return "noir"
	else:
		if maj:
			return "Blanc"
		return "blanc"