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


# class Random(IA):
#     def __init__(self, jeu, couleur):
#         super(Random, self).__init__(jeu, couleur)
#
#     def donne_coup(self, jeu):
#         return randon_play()
#
# def randon_play():

