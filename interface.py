import turtle
import os


# screen setup
screen = turtle.Screen()
screen.bgcolor("black")
screen.setworldcoordinates(-2.5, -4, 18, 18)


#  afficher position chiffre vertical
chiffrev = turtle.Turtle()
chiffrev.color("blue")
style = ('Courier', 20)
chiffrev.hideturtle()
chiffrev.penup()
chiffrev.setpos(-2, -0.5)
chiffrev.left(90)

# afficher position chiffre horizontal 
chiffreh = turtle.Turtle()
chiffreh.color("blue")
style = ('Courier', 20)
chiffreh.hideturtle()
chiffreh.penup()
chiffreh.setpos(0, -2)


# dot setup
damier = turtle.Turtle()
damier.color("yellow")
n = 9
d =2 
damier.speed(0)
damier.hideturtle()
damier.penup()
yd = 0
xd = 0
damier.setpos(xd, yd)


case = 1
for i in range(n):
    chiffrev.write(f"{case}", font=style)
    chiffreh.write(f"{case}", font=style)
    xd= 0
    damier.goto(xd, yd)
    for j in range(n):
        damier.dot()
        xd = xd + d
        damier.goto(xd, yd)
    yd = yd + d
    chiffrev.forward(d)
    chiffreh.forward(d)
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
for side in range(4):
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


# Tortue Mur vertical
mur_ver = turtle.Turtle()
mur_ver.hideturtle()
mur_ver.pensize(5)
mur_ver.left(90)
mur_ver.color("blue")

def déplacer_tortue(player):
    if player[0] == 1:
        player1.goto((player[1]-1)*2, (player[2]-1)*2)
    if player[0] == 2:
        player2.goto((player[1]-1)*2, (player[2]-1)*2)

def placer_mur_tortue(mur):
    if mur[0] == 'h':
        mur_hor.penup()
        mur_hor.setpos(((mur[1][0] - 1) * 2) - 1, ((mur[1][1]-1) * 2) - 1)
        mur_hor.pendown()
        mur_hor.forward(4)
    if mur[0] == 'v':
        mur_ver.penup()
        mur_ver.setpos(((mur[1][0]-1)*2)-1, ((mur[1][1]-1)*2)-1)
        mur_ver.pendown()
        mur_ver.forward(4)
       




déplacer_tortue([1, 2, 1])
placer_mur_tortue(['h', [8, 8]])
placer_mur_tortue(['v', [7, 7]])

    

    




turtle.done()