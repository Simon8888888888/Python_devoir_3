"""Ce module permet la gestion d'une partie de quoridor"""
import random
import copy
import networkx as nx


class QuoridorError(Exception):
    """Classe d'erreur du jeu Quoridor"""


class Quoridor:
    """Représentation et gestion d'une partie du jeu Quoridor"""

    def __init__(self, joueurs, murs=None):
        """Constructeur de la classe"""
        # Initialisation vide
        self.partie = {"joueurs": [],
                       "murs": {"horizontaux": [], "verticaux": []}}
        init_pos = [[5, 1], [5, 9]]
        nb_murs_joueurs = 0
        # Vérification du format des joueurs
        if not isinstance(joueurs, (list, tuple)):
            raise QuoridorError('Les joueurs doivent être une liste')
        # Nombre de joueur non-égal à 2
        if not len(joueurs) == 2:
            raise QuoridorError('La partie doit comprendre 2 joueurs')

        for i, joueur in enumerate(joueurs):
            # Joueur string
            if isinstance(joueur, str):
                self.partie["joueurs"] += [{"nom": joueur,
                                            "murs": 10,
                                            "pos": init_pos[i]}]
                nb_murs_joueurs += 10
            # Joueur dictionnaire
            elif isinstance(joueur, dict):
                # Dictionnaire incomplet
                if (not ("nom" in joueur and "murs"
                         in joueur and "pos" in joueur)):
                    raise QuoridorError('Joueur fourni incomplet')
                # Position des joueurs identique
                if joueurs[0]["pos"] == joueurs[1]["pos"]:
                    raise QuoridorError('Position d\'un joueur invalide')
                # Nombre de mur invalide
                if joueur["murs"] > 10 or joueur["murs"] < 0:
                    raise QuoridorError('Nb mur invalide pour un joueur')
                # Position du joueur hors limites
                if ((not 1 <= joueur["pos"][0] <= 9)
                        or (not 1 <= joueur["pos"][1] <= 9)):
                    raise QuoridorError('Position d\'un joueur invalide')
                # Joueur valide
                nb_murs_joueurs += joueur["murs"]
                self.partie["joueurs"] += [joueur]
            else:
                # Joueur non-str ou non-dict
                raise QuoridorError('Format de joeur invalide')
        # Vérification des murs
        if murs:
            # Les murs sont un dictionnaire valide
            if (isinstance(murs, dict) and "horizontaux" in murs and
                    "verticaux" in murs):
                # Nombre de mur trop grand
                if (not(len(murs["horizontaux"]) + len(murs["verticaux"])
                        + nb_murs_joueurs) == 20):
                    raise QuoridorError('Il n\'y a pas 20 murs au total')
                # Position murs horizontaux et verticaux
                bounds = [(1, 8), (2, 9)]
                orientations = ["horizontaux", "verticaux"]
                # Initialiser une partie temporaire
                temp_partie = copy.deepcopy(self.partie)
                for j, orientation in enumerate(orientations):
                    for i, mur in enumerate(murs[orientation]):
                        # Vérification des limites des murs
                        if (not bounds[j][0] <= mur[0] <= bounds[j][1]
                                or not bounds[1-j][0]
                                <= mur[1]
                                <= bounds[1-j][1]):
                            raise QuoridorError('Position de mur invalide')

                        # Vérifier si murs occupé
                        if ((any(check in temp_partie["murs"]["horizontaux"]
                                 for check in [(mur[0]-1, mur[1]),
                                               mur, (mur[0]+1, mur[1])])
                             or (mur[0]+1, mur[1]-1)
                             in temp_partie["murs"]["verticaux"])
                                and orientation == "horizontaux"):
                            raise QuoridorError('Position de mur déjà occupée')

                        # Vérifier si murs verticaux occupé
                        if ((any(check in temp_partie["murs"]["verticaux"]
                                 for check in [(mur[0], mur[1]-1),
                                               mur, (mur[0], mur[1]+1)])
                             or (mur[0]-1, mur[1]+1)
                             in temp_partie["murs"]["horizontaux"])
                                and orientation == "verticaux"):
                            raise QuoridorError('Position de mur déjà occupée')
                        # Positions valide, mais peut-être bloque un joueur...
                        temp_partie["murs"][orientation] += [tuple(mur)]

                # Vérification qu'un joueur n'est pas bloqué
                pos_1 = tuple(temp_partie["joueurs"][0]["pos"])
                pos_2 = tuple(temp_partie["joueurs"][1]["pos"])
                mur_h = temp_partie["murs"]["horizontaux"]
                mur_v = temp_partie["murs"]["verticaux"]
                graphe = construire_graphe([pos_1, pos_2], mur_h, mur_v)
                if (not nx.has_path(graphe, pos_1, 'B1')
                        or not nx.has_path(graphe, pos_2, 'B2')):
                    raise QuoridorError('Un ou plusieurs joueur est bloqué')
                self.partie = copy.deepcopy(temp_partie)
            else:
                raise QuoridorError('Les murs entrés sont invalides')
        elif not nb_murs_joueurs == 20:
            raise QuoridorError('Il n\'y a pas 20 murs au total')

    def __str__(self):
        """Cette fonction trace le damier de Quoridor
        en fonction de l'état de la partie"""
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
        for i, player in enumerate(self.partie["joueurs"]):
            players += [(" " + str(i+1) + "=" + player["nom"])]
            matrice[19 - player["pos"][1]*2][player["pos"][0]*2] = f' {i+1} '
        players = ','.join(players)

        # Murs horizontaux
        for mur in self.partie["murs"]["horizontaux"]:
            pos_x = mur[0] * 2
            pos_y = 20 - mur[1] * 2
            matrice[pos_y][pos_x] = '---'
            matrice[pos_y][pos_x + 1] = '-'
            matrice[pos_y][pos_x + 2] = '---'
        # Murs verticaux
        for mur in self.partie["murs"]["verticaux"]:
            pos_x = mur[0] * 2 - 1
            pos_y = 17 - mur[1] * 2
            matrice[pos_y][pos_x] = '|'
            matrice[pos_y + 1][pos_x] = '|'
            matrice[pos_y + 2][pos_x] = '|'
        # Construction du damier
        for i in range(len(matrice[i])):
            matrice[i] = ''.join(matrice[i])

        return 'Légende:' + players + '\n' + '\n'.join(matrice)

    def déplacer_jeton(self, joueur, position):
        """Permet de déplacer un joueur de la partie"""
        # Vérification du joueur
        if joueur not in (1, 2):
            raise QuoridorError("Ce joueur n'est pas valide, doit être 1 ou 2")
        graphe = construire_graphe([self.partie["joueurs"][0]["pos"],
                                    self.partie["joueurs"][1]["pos"]],
                                   self.partie["murs"]["horizontaux"],
                                   self.partie["murs"]["verticaux"])
        # Vérification de la position par rapport à l'état du jeu
        if (position in list(graphe.successors(
                                tuple(self.partie["joueurs"]
                                      [joueur-1]["pos"])))):
            self.partie["joueurs"][joueur-1]["pos"] = position
            return ('D', tuple(position))
        raise QuoridorError("Cette position n'est pas valide")

    def état_partie(self):
        """Retourne un dictionnaire de la partie"""
        return copy.deepcopy(self.partie)

    def jouer_coup(self, joueur):
        """Joue automatiquement un coup"""
        # Ne pas jouer s'il y a un gagnant
        if self.partie_terminé():
            raise QuoridorError('Partie terminée')
        # Vérification du numéro du joueur
        if joueur not in (1, 2):
            raise QuoridorError('Numéro de joueur invalide')
        # Définition des positions et objectifs
        i_joueur = joueur-1
        i_adverse = 1-i_joueur
        # Construction du graphique de position
        paths = self.get_players_paths()
        path_joueur, path_adverse = paths[i_joueur], paths[i_adverse]

        player_walls = self.partie["joueurs"][i_joueur]["murs"]
        losing = (len(path_adverse) <= len(path_joueur)
                  and len(path_adverse) < 8)
        # Spare wall based on how many player has left
        if player_walls:
            can_spare_wall = random.random() > 5/player_walls
        else:
            can_spare_wall = False
        # Be AHole if far from
        be_a_hole = (len(path_joueur) > 10 and can_spare_wall)
        # Place wall if losing or feeling evil
        place_wall = losing or be_a_hole
        # Si murs disponibles
        if place_wall and player_walls > 0:
            return self.block_player(i_adverse, 1, i_joueur)
        return self.déplacer_jeton(joueur, path_joueur[1])

    def get_players_paths(self):
        """Retourne le shortest path des deux joueurs"""
        pos_1 = self.partie["joueurs"][0]["pos"]
        pos_2 = self.partie["joueurs"][1]["pos"]
        graphe = construire_graphe([pos_1, pos_2],
                                   self.partie["murs"]["horizontaux"],
                                   self.partie["murs"]["verticaux"])
        path_1 = nx.shortest_path(graphe, tuple(pos_1), 'B1')
        path_2 = nx.shortest_path(graphe, tuple(pos_2), 'B2')

        return (path_1, path_2)

    def block_player(self, i_adverse, move_i, i_joueur):
        """Bloque le mouvement move_i selon le path entré"""
        # Get paths
        paths = self.get_players_paths()
        path_joueur, path_adverse = paths[i_joueur], paths[i_adverse]
        # Position du joueur à bloquer
        pos = path_adverse[move_i-1]
        # Trouver la position du mur pour bloquer
        diff_x = 1 if pos[0] < path_adverse[move_i][0] else 0
        diff_y = 1 if pos[1] < path_adverse[move_i][1] else 0
        # Orientation du mur
        if pos[0] != path_adverse[move_i][0]:
            orientation = 'vertical'
        else:
            orientation = 'horizontal'
        orient = 'MV' if orientation == 'vertical' else 'MH'
        # Deux position de mur possible pour bloquer un coup
        wall_pos_1 = [pos[0]+diff_x, pos[1]+diff_y]
        if orientation == 'vertical':
            wall_pos_2 = [pos[0]+diff_x, pos[1]-1]
        else:
            wall_pos_2 = [pos[0]-1, pos[1]+diff_y]
        # Deux position possible de mur pour bloquer
        walls = [wall_pos_1, wall_pos_2]
        # Ajout aléatoire du mur à bloquer
        # random.shuffle(walls)
        # Bloquer avec mur 1
        try:
            temp_partie = copy.deepcopy(self.partie)
            self.placer_mur(i_joueur+1, walls[0], orientation)
            new_paths = self.get_players_paths()
            # Si bloquer avec ce mur nuit au joueur, annuler le coup
            if len(new_paths[i_joueur]) > len(paths[i_joueur]):
                self.partie = copy.deepcopy(temp_partie)
                raise QuoridorError('Ce bloquage nuit au joueur')
            return (orient, walls[0])
        except QuoridorError:
            # Si mur 1 impossible, bloquer avec mur 2
            try:
                temp_partie = copy.deepcopy(self.partie)
                self.placer_mur(i_joueur+1, walls[1], orientation)
                new_paths = self.get_players_paths()
                # Si bloquer avec ce mur nuit au joueur, annuler le coup
                if len(new_paths[i_joueur]) > len(paths[i_joueur]):
                    self.partie = copy.deepcopy(temp_partie)
                    raise QuoridorError('Ce bloquage nuit au joueur')
                return (orient, walls[1])
            except QuoridorError:
                # Si mur 2 impossible, bloquer move suivant
                if move_i+2 == len(path_adverse):
                    return self.déplacer_jeton(i_joueur+1, path_joueur[1])
                # Si tous les moves non-blocable, déplacer jeton
                return self.block_player(i_adverse, move_i+1, i_joueur)

    def partie_terminé(self):
        """Vérifie si la partie est terminée"""
        # Le gagant est le joueur 1
        if self.partie["joueurs"][0]["pos"][1] == 9:
            gagnant = self.partie["joueurs"][0]["nom"]
        # Le gagant est le joueur 2
        elif self.partie["joueurs"][1]["pos"][1] == 1:
            gagnant = self.partie["joueurs"][1]["nom"]
        # Il n'y a pas de gagnant pour le momment
        else:
            return False
        return gagnant

    def placer_mur(self, joueur, position, orientation):
        """Place un mur dans la partie"""
        position = tuple(position)
        if orientation == "horizontal":
            orientation = "horizontaux"
        elif orientation == "vertical":
            orientation = "verticaux"
        else:
            raise QuoridorError('Orientation de mur invalide')
        # Numéro de joueur invalide
        if joueur not in (1, 2):
            raise QuoridorError('Numéro de joueur invalide')
        # Aucun mur disponible
        if self.partie["joueurs"][joueur-1]["murs"] <= 0:
            raise QuoridorError('Le joueur n\'a plus de murs disponibles')

        # Vérification position murs horizontaux
        if (((not 1 <= position[0] <= 8) or (not 2 <= position[1] <= 9))
                and orientation == "horizontaux"):
            raise QuoridorError('Position de mur invalide')
        # Vérification position murs verticaux
        if (((not 2 <= position[0] <= 9) or (not 1 <= position[1] <= 8))
                and orientation == "verticaux"):
            raise QuoridorError('Position de mur invalide')

        mur_v = self.partie["murs"]["verticaux"]
        mur_h = self.partie["murs"]["horizontaux"]

        # Vérifier si murs occupé
        blocking_h_h = [(position[0]-1, position[1]), tuple(position),
                        (position[0]+1, position[1])]
        blocking_h_v = (position[0]+1, position[1]-1)
        blocking_v_h = (position[0]-1, position[1]+1)
        blocking_v_v = [(position[0], position[1]-1), tuple(position),
                        (position[0], position[1]+1)]
        # Murs horizontaux
        if ((any(tuple(mur) in blocking_h_h for mur in mur_h)
             or list(blocking_h_v) in mur_v
             or tuple(blocking_h_v) in mur_v)
                and orientation == "horizontaux"):
            raise QuoridorError('Position de mur déjà occupée')
        # Murs verticaux
        if ((any(tuple(mur) in blocking_v_v for mur in mur_v)
             or list(blocking_v_h) in mur_h
             or tuple(blocking_v_h) in mur_h)
                and orientation == "verticaux"):
            raise QuoridorError('Position de mur déjà occupée')

        # - Vérifier si le nouveau mur bloque un joueur
        temp_partie = copy.deepcopy(self.partie)
        temp_partie["joueurs"][joueur-1]["murs"] -= 1
        temp_partie["murs"][orientation] += [position]

        temp_pos_1 = tuple(temp_partie["joueurs"][0]["pos"])
        temp_pos_2 = tuple(temp_partie["joueurs"][1]["pos"])
        # - Vérifier si le mouvement bloque un joueur
        graphe = construire_graphe([temp_pos_1, temp_pos_2],
                                   temp_partie["murs"]["horizontaux"],
                                   temp_partie["murs"]["verticaux"])
        if (not nx.has_path(graphe,
                            tuple(temp_partie["joueurs"][0]["pos"]),
                            'B1')
                or not nx.has_path(graphe,
                                   tuple(temp_partie["joueurs"][1]["pos"]),
                                   'B2')):
            raise QuoridorError('Un ou plusieurs joueur est bloqué')
        self.partie = copy.deepcopy(temp_partie)


def ajouter_lien_sauteur(noeud, voisin, graphe):
    """
    :param noeud: noeud de départ du lien.
    :param voisin: voisin par dessus lequel il faut sauter.
    """
    saut = 2*voisin[0]-noeud[0], 2*voisin[1]-noeud[1]

    if saut in graphe.successors(voisin):
        # ajouter le saut en ligne droite
        graphe.add_edge(noeud, saut)

    else:
        # ajouter les sauts en diagonale
        for saut in graphe.successors(voisin):
            graphe.add_edge(noeud, saut)

    return graphe

def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """Crée le graphe des déplacements admissibles pour les joueurs."""
    graphe = nx.DiGraph()

    # pour chaque colonne du damier
    for _x in range(1, 10):
        # pour chaque ligne du damier
        for _y in range(1, 10):
            # ajouter les arcs de tous les déplacements
            # possibles pour cette tuile
            if _x > 1:
                graphe.add_edge((_x, _y), (_x-1, _y))
            if _x < 9:
                graphe.add_edge((_x, _y), (_x+1, _y))
            if _y > 1:
                graphe.add_edge((_x, _y), (_x, _y-1))
            if _y < 9:
                graphe.add_edge((_x, _y), (_x, _y+1))

    # retirer tous les arcs qui croisent les murs horizontaux
    for _x, _y in murs_horizontaux:
        graphe.remove_edge((_x, _y-1), (_x, _y))
        graphe.remove_edge((_x, _y), (_x, _y-1))
        graphe.remove_edge((_x+1, _y-1), (_x+1, _y))
        graphe.remove_edge((_x+1, _y), (_x+1, _y-1))

    # retirer tous les arcs qui croisent les murs verticaux
    for _x, _y in murs_verticaux:
        graphe.remove_edge((_x-1, _y), (_x, _y))
        graphe.remove_edge((_x, _y), (_x-1, _y))
        graphe.remove_edge((_x-1, _y+1), (_x, _y+1))
        graphe.remove_edge((_x, _y+1), (_x-1, _y+1))

    # s'assurer que les positions des joueurs sont bien
    # des tuples (et non des listes)
    _j1, _j2 = tuple(joueurs[0]), tuple(joueurs[1])

    # traiter le cas des joueurs adjacents
    if _j2 in graphe.successors(_j1) or _j1 in graphe.successors(_j2):

        # retirer les liens entre les joueurs
        graphe.remove_edge(_j1, _j2)
        graphe.remove_edge(_j2, _j1)
        graphe = ajouter_lien_sauteur(_j1, _j2, graphe)
        graphe = ajouter_lien_sauteur(_j2, _j1, graphe)

    # ajouter les destinations finales des joueurs
    for _x in range(1, 10):
        graphe.add_edge((_x, 9), 'B1')
        graphe.add_edge((_x, 1), 'B2')

    return graphe
