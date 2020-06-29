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
    def __init__(self, jeu, color):
        super(MonteCarlo, self).__init__(jeu, color)

    def donne_coup(self, jeu):
        return self.simulation(jeu, 2)

    def simulation(self, jeu, max_sim):
        simulation = jeu.copy()
        current_sim = 0;
        while (simulation.partie_finie == False or current_sim == max_sim):
            available = simulation.goban.liste_coups_oks()
            if not available:
                return -1
            else:
                for coup in available:
                    if self.test_coup(simulation, available[current_sim], simulation.color) < jeu.color:
                        return available[current_sim]
            current_sim += 1 
        return -1

    def test_coup(self, simulation, coup, player):
        simulation.copy().jouer(coup)
        return simulation.score_black if player == -1 else simulation.score_white

            








