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
        elif not len(joueurs) == 2:
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
                elif joueurs[0]["pos"] == joueurs[1]["pos"]:
                    raise QuoridorError('Position d\'un joueur invalide')
                else:
                    # Nombre de mur invalide
                    if joueur["murs"] > 10 or joueur["murs"] < 0:
                        raise QuoridorError('Nb mur invalide pour un joueur')
                    # Position du joueur hors limites
                    elif ((not 1 <= joueur["pos"][0] <= 9)
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
                        elif ((any(check in temp_partie["murs"]["horizontaux"]
                                   for check in [(mur[0]-1, mur[1]),
                                                 mur, (mur[0]+1, mur[1])])
                               or (mur[0]+1, mur[1]-1)
                               in temp_partie["murs"]["verticaux"])
                              and orientation == "horizontaux"):
                            raise QuoridorError('Position de mur déjà occupée')

                        # Vérifier si murs verticaux occupé
                        elif ((any(check in temp_partie["murs"]["verticaux"]
                                   for check in [(mur[0], mur[1]-1),
                                                 mur, (mur[0], mur[1]+1)])
                               or (mur[0]-1, mur[1]+1)
                               in temp_partie["murs"]["horizontaux"])
                              and orientation == "verticaux"):
                            raise QuoridorError('Position de mur déjà occupée')
                        # Positions valide, mais peut-être bloque un joueur...
                        temp_partie["murs"][orientation] += [tuple(mur)]

                # Vérification qu'un joueur n'est pas bloqué
                graphe = construire_graphe([temp_partie["joueurs"][0]["pos"],
                                            temp_partie["joueurs"][1]["pos"]],
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
        else:
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
        elif joueur not in (1, 2):
            raise QuoridorError('Numéro de joueur invalide')
        # Construction du graphique de position
        graphe = construire_graphe([self.partie["joueurs"][0]["pos"],
                                    self.partie["joueurs"][1]["pos"]],
                                   self.partie["murs"]["horizontaux"],
                                   self.partie["murs"]["verticaux"])
        # Coup possible du joueur 2
        # Si le chemin le plus court de l'adversaire est plus petit,
        # placer un mur
        objectif_joueur = 'B1' if joueur == 1 else 'B2'
        objectif_adverse = 'B2' if joueur == 1 else 'B1'
        if (len(nx.shortest_path(graphe,
                                 tuple(self.partie["joueurs"][0]["pos"]),
                                 objectif_adverse))
                < len(nx.shortest_path(graphe,
                                       tuple(self.partie["joueurs"][1]["pos"]),
                                       objectif_joueur))
                and self.partie["joueurs"][joueur-1]["murs"] > 0):
            try:
                self.placer_mur(joueur,
                                (random.randrange(1, 9),
                                 random.randrange(1, 9)),
                                random.choice(["vertical", "horizontal"]))
            except QuoridorError:
                self.jouer_coup(joueur)
        # Sinon, meilleur coup
        else:
            shortes_paths = nx.shortest_path(graphe,
                                             tuple(self.partie["joueurs"]
                                                   [joueur-1]["pos"]),
                                             objectif_joueur)
            self.déplacer_jeton(joueur, shortes_paths[1])

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
        elif self.partie["joueurs"][joueur-1]["murs"] <= 0:
            raise QuoridorError('Le joueur n\'a plus de murs disponibles')

        # Vérification position murs horizontaux
        if (((not 1 <= position[0] <= 8) or (not 2 <= position[1] <= 9))
                and orientation == "horizontaux"):
            raise QuoridorError('Position de mur invalide')
        # Vérification position murs verticaux
        if (((not 2 <= position[0] <= 9) or (not 1 <= position[1] <= 8))
                and orientation == "verticaux"):
            raise QuoridorError('Position de mur invalide')

        # Vérifier si murs horizontaux occupé
        if ((any(mur in self.partie["murs"]["horizontaux"] for mur
                 in [(position[0]-1, position[1]), position,
                     (position[0]+1, position[1])])
             or (position[0]+1, position[1]-1)
             in self.partie["murs"]["verticaux"])
                and orientation == "horizontaux"):
            raise QuoridorError('Position de mur déjà occupée')
        # Vérifier si murs verticaux occupé
        if ((any(mur in self.partie["murs"]["verticaux"] for mur
                 in [(position[0], position[1]-1), position,
                     (position[0], position[1]+1)])
             or (position[0]-1, position[1]+1)
             in self.partie["murs"]["horizontaux"])
                and orientation == "verticaux"):
            raise QuoridorError('Position de mur déjà occupée')

        # - Vérifier si le nouveau mur bloque un joueur
        temp_partie = copy.deepcopy(self.partie)
        temp_partie["joueurs"][joueur-1]["murs"] -= 1
        temp_partie["murs"][orientation] += [position]

        # - Vérifier si le mouvement bloque un joueur
        graphe = construire_graphe([temp_partie["joueurs"][0]["pos"],
                                    temp_partie["joueurs"][1]["pos"]],
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


def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """Crée le graphe des déplacements admissibles pour les joueurs."""
    graphe = nx.DiGraph()

    # pour chaque colonne du damier
    for x in range(1, 10):
        # pour chaque ligne du damier
        for y in range(1, 10):
            # ajouter les arcs de tous les déplacements
            # possibles pour cette tuile
            if x > 1:
                graphe.add_edge((x, y), (x-1, y))
            if x < 9:
                graphe.add_edge((x, y), (x+1, y))
            if y > 1:
                graphe.add_edge((x, y), (x, y-1))
            if y < 9:
                graphe.add_edge((x, y), (x, y+1))

    # retirer tous les arcs qui croisent les murs horizontaux
    for x, y in murs_horizontaux:
        graphe.remove_edge((x, y-1), (x, y))
        graphe.remove_edge((x, y), (x, y-1))
        graphe.remove_edge((x+1, y-1), (x+1, y))
        graphe.remove_edge((x+1, y), (x+1, y-1))

    # retirer tous les arcs qui croisent les murs verticaux
    for x, y in murs_verticaux:
        graphe.remove_edge((x-1, y), (x, y))
        graphe.remove_edge((x, y), (x-1, y))
        graphe.remove_edge((x-1, y+1), (x, y+1))
        graphe.remove_edge((x, y+1), (x-1, y+1))

    # s'assurer que les positions des joueurs sont bien
    # des tuples (et non des listes)
    j1, j2 = tuple(joueurs[0]), tuple(joueurs[1])

    # traiter le cas des joueurs adjacents
    if j2 in graphe.successors(j1) or j1 in graphe.successors(j2):

        # retirer les liens entre les joueurs
        graphe.remove_edge(j1, j2)
        graphe.remove_edge(j2, j1)

        def ajouter_lien_sauteur(noeud, voisin):
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

        ajouter_lien_sauteur(j1, j2)
        ajouter_lien_sauteur(j2, j1)

    # ajouter les destinations finales des joueurs
    for x in range(1, 10):
        graphe.add_edge((x, 9), 'B1')
        graphe.add_edge((x, 1), 'B2')

    return graphe
