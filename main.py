"""Ce module permet de jouer au jeu Quoridor"""
import turtle
import argparse
import api
from quoridor import Quoridor
from quoridorx import QuoridorX


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
        if GRAPHIQUE:
            if AUTOMATIQUE:
                QUORIDOR = QuoridorX(JOUEURS,
                                     MURS,
                                     auto=True)
            else:
                QUORIDOR = QuoridorX(JOUEURS, MURS)
        else:
            QUORIDOR = Quoridor(JOUEURS, MURS)
        ERROR = False
    except RuntimeError as err:
        print(err)
    else:
        PLAYING = True
        # Jouer
        while PLAYING:
            if not ERROR and not GRAPHIQUE:
                print(QUORIDOR)
            ERROR = False
            if AUTOMATIQUE:
                COUP = QUORIDOR.jouer_coup(1)
            else:
                _TYPE = input("Entrer le mouvement (D, MH ou MV): ").upper()
                POS_X = input('Entrer la position en X de votre mouvement: ')
                POS_Y = input('Entrer la position en Y de votre mouvement: ')
                COUP = (_TYPE, (POS_X, POS_Y))
            if GRAPHIQUE:
                QUORIDOR.afficher()
            try:
                STATE = api.jouer_coup(_ID, *COUP)
                QUORIDOR.partie = STATE
                if GRAPHIQUE:
                    QUORIDOR.afficher()
            except StopIteration as err:
                PLAYING = False
                if GRAPHIQUE:
                    QUORIDOR.afficher_tortue_gagnante(str(err))
                    turtle.done()
                print('Gagnant:', err)
            except RuntimeError as err:
                print(err)
                ERROR = True
