from quoridor import Quoridor, QuoridorError


PLAYERS = ["Bot 1", "Bot 2"]
PLAYING = True
CURRENT_PLAYER = 1

try:
    partie = Quoridor(PLAYERS)
    ERROR = False
except RuntimeError as err:
    print(err)
else:
    while PLAYING:
        print(partie)
        print('Tour au joueur:', CURRENT_PLAYER)
        KEEP = input("Keep game going? (Enter): ").lower()
        if not partie.partie_terminé():
            try:
                partie.jouer_coup(CURRENT_PLAYER)
                état = partie.état_partie()
            except QuoridorError as err:
                PLAYING = False
                print(err)
            else:
                if partie.partie_terminé():
                    print(partie)
                    print('le gagnant est: ', partie.partie_terminé())
                    PLAYING = False
                else:
                    CURRENT_PLAYER = 1 if CURRENT_PLAYER == 2 else 2
        else:
            PLAYING = False
