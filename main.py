"""Ce module permet de jouer au jeu Quoridor"""
import argparse
import api
import tkinter
import turtle
from quoridor import Quoridor

def analyser_commande():
    """Cette fonction retire l'IDUL de l'argument d'entrée"""
    parser = argparse.ArgumentParser(
        description="Jeu Quoridor - phase 3"
    )
    parser.add_argument(
        'idul', metavar='idul', help="IDUL du joueur."
    )
    parser.add_argument(
        '-a', '--automatique', 
        dest='automatique', action="store_true",
        help="Activer le mode automatique."
    )
    parser.add_argument(
        '-x', '--graphique', 
        dest='graphique', action="store_true",
        help="Activer le mode graphique."
    )

    args = parser.parse_args()
    
    return args


if __name__ == "__main__":
    ARGS = analyser_commande()
    IDUL = ARGS.idul
    AUTOMATIQUE = ARGS.automatique
    GRAPHIQUE = ARGS.graphique
    
    PLAYING = False
    WINS = []
    # Débuter partie
    try:
        PARTIE = api.débuter_partie(IDUL)
        _ID = PARTIE[0]
        STATE = PARTIE[1]
        JOUEURS = STATE['joueurs']
        MURS = STATE['murs']
        QUORIDOR = Quoridor(JOUEURS, MURS)
        ERROR = False
    except RuntimeError as err:
        print(err)
    else:
        PLAYING = True
        # Jouer
        while PLAYING:
            if not ERROR:
                print(QUORIDOR)
            ERROR = False
            if AUTOMATIQUE:
                COUP = QUORIDOR.jouer_coup(1)
            else:
                _TYPE = input("Entrer le mouvement (D, MH ou MV): ").upper()
                POS_X = input('Entrer la position en X de votre mouvement: ')
                POS_Y = input('Entrer la position en Y de votre mouvement: ')
                COUP = (_TYPE, (POS_X, POS_Y))
            try:
                STATE = api.jouer_coup(_ID, *COUP)
                QUORIDOR.partie = STATE
            except StopIteration as err:
                PLAYING = False
                print('Gagnant:', err)
            except RuntimeError as err:
                print(err)
                ERROR = True