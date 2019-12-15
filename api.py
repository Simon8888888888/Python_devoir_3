"""Ce module permet d'interagir avec l'api quoridor du cours python Ulaval"""
import requests


URL_BASE = 'https://python.gel.ulaval.ca/quoridor/api/'


def lister_parties(idul):
    """Cette fonction permet de lister les parties actives pour un idul"""
    rep = requests.get(URL_BASE+'lister/', params={'idul': idul})
    if rep.status_code == 200:
        # La requête s'est déroulée normalement
        rep = rep.json()
        if "message" in rep:
            raise RuntimeError(f"{rep['message']}")
        return rep["parties"]
    raise RuntimeError(f"Erreur GET {URL_BASE+'lister'}: {rep.status_code}.")


def débuter_partie(idul):
    """Cette fonction permet de débuter une partie avec un idul"""
    rep = requests.post(URL_BASE+'débuter/', data={'idul': idul})
    if rep.status_code == 200:
        # La requête s'est déroulée normalement
        rep = rep.json()
        if "message" in rep:
            raise RuntimeError(f"{rep['message']}")
        return (rep["id"], rep["état"])
    raise RuntimeError(f"Erreur GET {URL_BASE+'lister'}: {rep.status_code}.")


def jouer_coup(id_partie, type_coup, position):
    """Cette fonction permet de jouer un coup pour une
       partie avec un identifiant, un type et une position"""
    rep = requests.post(URL_BASE+'jouer/',
                        data={'id': id_partie,
                              'type': type_coup,
                              'pos': position})
    if rep.status_code == 200:
        # La requête s'est déroulée normalement
        rep = rep.json()
        if "message" in rep:
            raise RuntimeError(f"{rep['message']}")
        if "gagnant" in rep:
            raise StopIteration(f"{rep['gagnant']}")

        return rep["état"]
    raise RuntimeError(f"Erreur GET {URL_BASE+'lister'}: {rep.status_code}.")
