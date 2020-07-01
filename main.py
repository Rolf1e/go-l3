import playerlib
import gamelib

black_wins = 0
white_wins = 0
for i in range(10):
    jeu = gamelib.GameClass(5, 0.5, {"choix_joueurs": False})
    jeu.blanc = playerlib.Random(jeu, -1)
    jeu.noir = playerlib.MonteCarlo(jeu, 1)
    jeu.joueur_courant = jeu.noir
    while(not jeu.partie_finie):
        jeu.jouer(jeu.joueur_courant.donne_coup(jeu))

    score =  jeu.score()
    print("partie :", i , "score: ", score)
    if score < 0:
        white_wins += 1
        print("white wins")
    else:
        black_wins += 1
        print("Black wins")

print("Black : ", black_wins, "White :", white_wins)
    



"""jeu = gamelib.GameClass(5, 0.5)
   jeu.lance_gui() """
