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
    def __init__(self, jeu, color):
        super(Random, self).__init__(jeu, color)

    def donne_coup(self, jeu):
        coups = jeu.goban.liste_coups_oks()
        length = len(coups)
        if not coups:
            return -1
        else:
            return coups[randint(0, length) - 1]

class MonteCarlo(IA):
    def __init__(self, game, color):
        super(MonteCarlo, self).__init__(game, color)

    def donne_coup(self, game):
        best = -1
        score = -np.infty 
        coups = game.goban.liste_coups_oks()
        if not coups:
            return -1

        else:

            for coup in coups:
                game_copy = game.copy()
                game_copy.jouer(coup)
                average = self.average(game_copy, 10)
                if average > score:
                    score = average 
                    best = coup

#        print("best:", best)
        return best

    def average(self, game, nb_sim):
        average = 0
        for i in range(nb_sim):
            result = self.simulation(game.copy()) * self.color
            average += result

        return average / nb_sim

    def simulation(self, sim):
        while not sim.partie_finie:
            coups = sim.goban.liste_coups_oks()
            sim.jouer(coups[randint(0, len(coups) - 1)])
        if sim.score() > 0:
            return 1
        else:
            return 0

