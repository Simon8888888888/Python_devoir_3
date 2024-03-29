"""Ce module permet la gestion d'une partie de quoridor"""
import turtle
from quoridor import Quoridor


class QuoridorX(Quoridor):
    """Partie de Quoridor avec affichage graphique"""
    def __init__(self, joueurs, murs=None, auto=False):
        """Constructeur de la classe"""
        super().__init__(joueurs, murs)
        self.setup = start_game(auto)
        self.afficher()
        self.winner = None

    def afficher(self):
        """Affiche l'état présent de la partie"""
        etat = self.état_partie()
        joueur1, joueur2, murs_horiz, murs_vert = convertir(etat)
        if murs_horiz:
            placer_mur_tortue(murs_horiz, self.setup)
        if murs_vert:
            placer_mur_tortue(murs_vert, self.setup)
        deplacer_tortue(joueur1, self.setup)
        deplacer_tortue(joueur2, self.setup)

    def afficher_tortue_gagnante(self, winner):
        """Affiche sur le jeu le nom du gagnant"""
        gagnant = turtle.Turtle()
        gagnant.hideturtle()
        gagnant.penup()
        gagnant.setpos(-1.25, 5)
        style3 = ('Courier', 30)
        gagnant.color("red")
        gagnant.write(f"Le gagnant est {winner}", font=style3)
        self.winner = winner

def start_game(automatique):
    """Initialise l'affichage de la game"""
    # screen set
    screen = turtle.Screen()
    screen.title("Quoridor")
    screen.bgcolor("black")
    screen.setworldcoordinates(-2.5, -7, 18, 18)

    #  afficher position chiffre vertical
    chiffrev = turtle.Turtle()
    chiffrev.color("red")
    style = ('Courier', 15)
    chiffrev.hideturtle()
    chiffrev.penup()
    chiffrev.setpos(-2, -0.5)
    chiffrev.left(90)

    # afficher position chiffre horizontal
    chiffreh = turtle.Turtle()
    chiffreh.color("red")
    style = ('Courier', 15)
    chiffreh.hideturtle()
    chiffreh.penup()
    chiffreh.setpos(0, -2.5)

    # dot setup
    damier = turtle.Turtle()
    damier.color("yellow")
    _n = 9
    _d = 2
    damier.speed(0)
    damier.hideturtle()
    damier.penup()
    _yd = 0
    _xd = 0
    damier.setpos(_xd, _yd)

    # message d'encouragement
    style2 = ('Courier', 15)
    if automatique:
        message = 'Que la force soit avec toi trepi la tortue <3'
    else:
        message = 'Entrer vos commandes dans le terminal'
    encouragement = turtle.Turtle()
    encouragement.color("green")
    encouragement.penup()
    encouragement.hideturtle()
    encouragement.setpos(-1.25, -5)
    encouragement.write(message, font=style2)

    case = 1
    for _ in range(_n):
        chiffrev.write(f"{case}", font=style)
        chiffreh.write(f"{case}", font=style)
        _xd = 0
        damier.goto(_xd, _yd)
        for _ in range(_n):
            damier.dot()
            _xd = _xd + _d
            damier.goto(_xd, _yd)
        _yd = _yd + _d
        chiffrev.forward(_d)
        chiffreh.forward(_d)
        case += 1

    # set up cadre
    cadre1 = turtle.Turtle()
    cadre2 = turtle.Turtle()
    cadre1.color("blue")
    cadre2.color("blue")
    cadre1.hideturtle()
    cadre2.hideturtle()
    cadre1.penup()
    cadre2.penup()
    cadre1.setpos(-1, -1)
    cadre2.setpos(-0.75, -0.75)
    cadre1.pendown()
    cadre2.pendown()

    for _ in range(4):
        cadre1.forward(18)
        cadre2.forward(17.5)
        cadre1.left(90)
        cadre2.left(90)

    # setup player1 and 2
    player1 = turtle.Turtle()
    player2 = turtle.Turtle()
    player1.color("turquoise")
    player2.color("red")
    player1.shape("turtle")
    player2.shape("turtle")
    player1.hideturtle()
    player2.hideturtle()
    player1.penup()
    player2.penup()
    player1.setpos(8, 0)
    player2.setpos(8, 16)
    player1.left(90)
    player2.right(90)
    player1.showturtle()
    player2.showturtle()

    # Tortue Mur horizontal
    mur_hor = turtle.Turtle()
    mur_hor.hideturtle()
    mur_hor.pensize(5)
    mur_hor.color("blue")

    # Tortue Mur
    mur_ver = turtle.Turtle()
    mur_ver.hideturtle()
    mur_ver.pensize(5)
    mur_ver.left(90)
    mur_ver.color("blue")

    return [player1, player2, mur_hor, mur_ver]

def convertir(etat):
    """Converti un état du jeu en variables pour turtle"""
    # organisation de la position des joueurs
    pos_x_1 = etat["joueurs"][0]["pos"][0]      # position du joueur 1
    pos_y_1 = etat["joueurs"][0]["pos"][1]      # position du joueur 1
    pos_x_2 = etat["joueurs"][1]["pos"][0]      # position du joueur 2
    pos_y_2 = etat["joueurs"][1]["pos"][1]      # position du joueur 2
    joueur1 = [1, pos_x_1, pos_y_1]
    joueur2 = [2, pos_x_2, pos_y_2]

    # organisation de la position des murs
    compte_murs_horiz = 0
    compte_murs_vert = 0
    compte_murs_horiz = len(etat["murs"]["horizontaux"])
    compte_murs_vert = len(etat["murs"]["verticaux"])

    murs_horiz = None
    murs_vert = None

    if compte_murs_horiz:
        pos_murs_hor1 = etat["murs"]["horizontaux"][compte_murs_horiz - 1]
        pos_murs_hor2 = etat["murs"]["horizontaux"][compte_murs_horiz - 2]
        murs_horiz = ["h", pos_murs_hor1, pos_murs_hor2]
    if compte_murs_vert:
        pos_murs_vert1 = etat["murs"]["verticaux"][compte_murs_vert - 1]
        pos_murs_vert2 = etat["murs"]["verticaux"][compte_murs_vert - 2]
        murs_vert = ["v", pos_murs_vert1, pos_murs_vert2]

    return joueur1, joueur2, murs_horiz, murs_vert

def deplacer_tortue(player, setup):
    """Positionne une tortue sur le jeu"""
    if player[0] == 1:
        setup[0].goto((player[1]-1)*2, (player[2]-1)*2)
    if player[0] == 2:
        setup[1].goto((player[1]-1)*2, (player[2]-1)*2)

def placer_mur_tortue(mur, setup):
    """Positionne un mur sur le jeu"""
    if mur[0] == 'h':
        setup[2].penup()
        setup[2].setpos(((mur[2][0] - 1) * 2) - 1, ((mur[2][1]-1) * 2) - 1)
        setup[2].pendown()
        setup[2].forward(4)
        setup[2].penup()
        setup[2].setpos(((mur[1][0] - 1) * 2) - 1, ((mur[1][1]-1) * 2) - 1)
        setup[2].pendown()
        setup[2].forward(4)

    if mur[0] == 'v':
        setup[3].penup()
        setup[3].setpos(((mur[2][0]-1)*2)-1, ((mur[2][1]-1)*2)-1)
        setup[3].pendown()
        setup[3].forward(4)
        setup[3].penup()
        setup[3].setpos(((mur[1][0]-1)*2)-1, ((mur[1][1]-1)*2)-1)
        setup[3].pendown()
        setup[3].forward(4)
