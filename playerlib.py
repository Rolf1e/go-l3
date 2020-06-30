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
        coups = game.goban.liste_coups_oks()
        best = []
        score = -np.infty
        if not coups:
            return -1

        else:
            for coup in coups:
                average = self.average(game.copy(), 10)
                if average > score:
                    score = average
                    best = coup

        return best

    def average(self, game, nb_sim):
        average = 0
        for i in range(nb_sim):
            print("simulation" + str(i))
            result = self.simulation(game) * self.color
            average += result

        return average / nb_sim

    def simulation(self, simulation):
        i = 0
        while not simulation.partie_finie:
            i += 1
            print(i)
            coups = simulation.goban.liste_coups_oks()
            simulation.jouer(coups[randint(0, len(coups) - 1)])

        return simulation.score()

