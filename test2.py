état = {
    "joueurs": [
        {"nom": "idul", "murs": 7, "pos": [5, 5]}, 
        {"nom": "automate", "murs": 3, "pos": [8, 6]}
    ], 
    "murs": {
        "horizontaux": [[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]], 
        "verticaux": [[6, 2], [4, 4], [2, 6], [7, 5], [7, 7]]
    }
}

#organisation de la position des joueurs
pos_x_1 = état["joueurs"][0]["pos"][0]      #position du joueur 1
pos_y_1 = état["joueurs"][0]["pos"][1]      #position du joueur 1
pos_x_2 = état["joueurs"][1]["pos"][0]      #position du joueur 2
pos_y_2 = état["joueurs"][1]["pos"][1]      #position du joueur 2
joueur1 = [1,pos_x_1,pos_y_1]
joueur2 = [2,pos_x_2,pos_y_2]

#organisation de la position des murs
compte_murs_horiz = 0
compte_murs_vert = 0
for i in état["murs"]["horizontaux"]:
    compte_murs_horiz += 1
for i in état["murs"]["verticaux"]:
    compte_murs_vert += 1

pos_murs_horiz = état["murs"]["horizontaux"][compte_murs_horiz - 1]
pos_murs_vert = état["murs"]["verticaux"][compte_murs_vert - 1]
murs_horiz = ["h", pos_murs_horiz]
murs_vert = ["v", pos_murs_vert]
print(murs_vert)