import playerlib
import gamelib
import matplotlib.pyplot as plt
import time


def graph(x, y, xlabel, ylabel):
    plt.figure(figsize=(5, 5))
    plt.plot(x, y, label="performance")
    plt.title("Monte carlos Go")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()
#    plt.grid()

def game(difficulty, nb_party, scores, nombre_sim, times):    
    black_wins = 0
    white_wins = 0
    timeStart = 0

    for i in range(nb_party):
        jeu = gamelib.GameClass(5, 0.5, {"choix_joueurs": False})
        timeStart = time.time()
        #jeu.blanc = playerlib.Random(jeu, -1)
        jeu.noir = playerlib.MonteCarlo(jeu, 1, difficulty)
        jeu.blanc = playerlib.MonteCarloArthur(jeu, -1, difficulty, False)
        jeu.joueur_courant = jeu.noir
        while(not jeu.partie_finie):
            jeu.jouer(jeu.joueur_courant.donne_coup(jeu))

        score =  jeu.score()
        difficulty += 1
        print("partie :", i , "score: ", score)
        if score < 0:
            white_wins += 1
            print("white wins")
        else:
            black_wins += 1
            print("Black wins")

        scores.append(score)
        nombre_sim.append(difficulty)
        times.append(time.time() - timeStart)


    print("Black : ", black_wins, "White :", white_wins)


    print("coups:", nombre_sim)
    print("score:", scores)
    print("temps:", times)

    return difficulty


# main code
scores = [] #x
nombre_sim = [] #y
times = []
difficulty = 1
for i in range(5):
    print("####### simulation :", i , "#########")
    difficulty = game(difficulty, 5, scores, nombre_sim, times)

graph(nombre_sim, scores, "nombre de simulation", "scores")
graph(nombre_sim, times, "nombre de simulation", "time")
"""jeu = gamelib.GameClass(5, 0.5)
   jeu.lance_gui() """
