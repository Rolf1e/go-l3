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
    def __init__(self, game, color, nb_sim):
        super(MonteCarlo, self).__init__(game, color)
        self.nb_sim = nb_sim
        self.nb_coup_player = 0

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
                average = self.average(game_copy, self.nb_sim)
                if average > score:
                    score = average 
                    best = coup
        self.nb_coup_player += 1
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
        return sim.score()

class MonteCarloArthur(IA):

    def __init__(self, jeu, color, nombreSimulation = 5, showCompteur = False):
        super(MonteCarloArthur, self).__init__(jeu, color)
        self.nombreSimulation = nombreSimulation
        self.nombreDeCoup = 0
        self.showCompteur = showCompteur

    def donne_coup(self, game):

        listeCoups = game.goban.liste_coups_oks()
        tailleListeCoups = len(listeCoups) - 1
        coor = []
        score = - np.infty

        if tailleListeCoups != 0:

            for i in range(tailleListeCoups):
                averageScore = 0

                for j in range(self.nombreSimulation):
                    copyGame = game.copy()
                    copyGame.jouer(listeCoups[i])
                    averageScore = averageScore + (self.simulation(copyGame) * self.color)

                averageScore = averageScore / self.nombreSimulation

                if averageScore > score:
                    score = averageScore
                    coor = listeCoups[i]

            if self.showCompteur:
                print("nombre de coups : " + str(self.nombreDeCoup))

            return coor

        else:
            if self.showCompteur:
                print("nombre de coups : " + str(self.nombreDeCoup))

            return -1

    def simulation(self, game):

        while not game.partie_finie:
            listeCoups = game.goban.liste_coups_oks()
            arrayLength = len(listeCoups) - 1
            randomNumber = randint(0, arrayLength)
            game.jouer(listeCoups[randomNumber])
            self.nombreDeCoup = self.nombreDeCoup + 1

        return game.score()


