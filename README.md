Tigran SLAMA

Require :

 - Pip : `apt install python3-pip`

 - numpy : `pip3 install numpy`

 - tkinter : `apt-get install python3-tk`

 - Pillow : `pip3 install Pillow`

 - matplotlib : `pip3 install matplotlib`

 Run following to start the AI : `python3 main.py`

 - [x] Random 

 - [x] Monte Carlo  

14. 
Nous pourrions imaginer de donner un poids en fonction des coordonnées d'une case disponible. Une case sur le bord, pourrait être préférée en fonction de l'état de la partie, du type temps de jeu, position par rapport à l'adversaire, résultats à l'instant t. On pourrait regarder là où se place notre point par rapport à nos précédents. Un pion collé à un pion de notre couleur peut être préféré car il peut permettre de capturer. Le fait d'effectuer des ilots de pions est souvent préférable en terme de stratégie. Ou la possibilité de pouvoir créer un oeil.C'est difficile d'envisager car il faut effectuer énormément de calculs et de simulation à chaque tour pour faire le meilleur choix.

15. 
Je pense que le joueur jouant en premier aura de meilleure chance de gagner peu importe l'ia. Les deux algoritmes donnant les mêmes sorties pour des entrées identiques, cela dépend de la fonction d'évaluation. 
