from random import randint
import movelib
import copy
import numpy as np


class Joueur():

    def __init__(self, jeu, color):
        self.jeu = jeu
        self.color = color

    def donne_coup(self, jeu):
        pass


class Humain(Joueur):
    pass


class IA(Joueur):
    pass


class Random(IA):
    def __init__(self, jeu, couleur):
        super(Random, self).__init__(jeu, couleur)

    def donne_coup(self, jeu):
        coups = jeu.goban.liste_coups_oks()
        length = len(coups)
        if not coups:
             return -1
        else:
            return coups[randint(0, length) - 1]


