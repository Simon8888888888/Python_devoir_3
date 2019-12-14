"""Ce module permet de jouer au jeu Quoridor"""
import argparse
import api


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


def afficher_damier_ascii(data):
    """Cette fonction trace le damier de quoridor
       en fonction de l'état qu'il reçoit"""
    players = []
    y_labels = ['  ', '9 ', '  ', '8 ', '  ', '7 ', '  ', '6 ', '  ', '5 ',
                '  ', '4 ', '  ', '3 ', '  ', '2 ', '  ', '1 ', '--', '  ']
    left_wall = [' ', '|', '|', '|', '|', '|', '|', '|', '|',
                 '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|']
    right_wall = [' ', '|', '|', '|', '|', '|', '|', '|', '|',
                  '|', '|', '|', '|', '|', '|', '|', '|', '|', ' ', ' ']

    matrice = []
    # Contour suppérieur
    matrice += [['  ', ' ', '---', '-', '---', '-',
                      '---', '-', '---', '-', '---', '-', '---',
                      '-', '---', '-', '---', '-', '---']]

    for i in range(1, 18):
        matrice += [['' for x in range(20)]]
        matrice[i][0] = y_labels[i]
        matrice[i][1] = left_wall[i]
        matrice[i][19] = right_wall[i]
        for j in range(2, 19):
            # Intérieur des contours (Pions et murs)
            if 0 < i < 18:
                if i % 2 == 1:
                    matrice[i][j] = ' . '
                else:
                    matrice[i][j] = '   '

                if j % 2 == 1:
                    matrice[i][j] = ' '

    # Contour inférieur
    matrice += [['--', '|', '---', '-', '---', '-',
                    '---', '-', '---', '-', '---', '-', '---',
                    '-', '---', '-', '---', '-', '---']]
    # Échelle en X
    matrice += [['  ', '|', ' 1 ', ' ', ' 2 ', ' ', ' 3 ',
                    ' ', ' 4 ', ' ', ' 5 ', ' ', ' 6 ', ' ',
                    ' 7 ', ' ', ' 8 ', ' ', ' 9']]

    # Joueurs
    for i, player in enumerate(data["joueurs"]):
        players += [(" " + str(i+1) + "=" + player["nom"])]
        matrice[19 - player["pos"][1]*2][player["pos"][0]*2] = f' {i+1} '
    players = ','.join(players)

    # Murs horizontaux
    for mur in data["murs"]["horizontaux"]:
        pos_x = mur[0] * 2
        pos_y = 20 - mur[1] * 2
        matrice[pos_y][pos_x] = '---'
        matrice[pos_y][pos_x + 1] = '-'
        matrice[pos_y][pos_x + 2] = '---'
    # Murs verticaux
    for mur in data["murs"]["verticaux"]:
        pos_x = mur[0] * 2 - 1
        pos_y = 17 - mur[1] * 2
        matrice[pos_y][pos_x] = '|'
        matrice[pos_y + 1][pos_x] = '|'
        matrice[pos_y + 2][pos_x] = '|'
    # Construction du damier
    for i in range(20):
        matrice[i] = ''.join(matrice[i])

    damier = 'Légende:' + players + '\n' + '\n'.join(matrice)
    print(damier)


if __name__ == "__main__":
    ARGS = analyser_commande()
    IDUL = ARGS.idul
    LIST = ARGS.lister_parties

    PLAYING = True

    if LIST:
        PLAYING = False
        try:
            print(api.lister_parties(IDUL))
        except RuntimeError as err:
            print(err)
    else:
        try:
            PARTIE = api.débuter_partie(IDUL)
            _ID = PARTIE[0]
            STATE = PARTIE[1]
            ERROR = False
        except RuntimeError as err:
            print(err)
        else:
            while PLAYING:
                if not ERROR:
                    afficher_damier_ascii(STATE)
                ERROR = False
                _TYPE = input("Entrer le mouvement (D, MH ou MV): ").upper()
                POS_X = input('Entrer la position en X de votre mouvement: ')
                POS_Y = input('Entrer la position en Y de votre mouvement: ')
                try:
                    NEW_STATE = api.jouer_coup(_ID, _TYPE, (POS_X, POS_Y))
                except StopIteration as err:
                    PLAYING = False
                    print('Gagnant:', err)
                except RuntimeError as err:
                    print(err)
                    ERROR = True
                else:
                    STATE = NEW_STATE