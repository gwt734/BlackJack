# Fichier où stocker toute les fonctions nécessaires au jeu

import Constantes
import random


# A1 - Paquet de cartes
def paquet():
    pile = []
    for i in range(len(Constantes.COULEUR)):  # pour chaque couleur (4)
        for j in range(len(Constantes.VALEUR)):  # pour chaque valeur de carte (13)
            pile += [Constantes.VALEUR[j] + " de " + Constantes.COULEUR[i]]  # ajoute la carte à la pile
    return pile
    # Fonction à tester


def valeur_carte(carte):
    if carte[0] == "A":  # si la carte est un As
        return input_protege(question, int, "list", [1, 11], [1, 11])  # demande la valeur souhaitée (1 ou 11)
    elif carte[0] == "V" or carte[0] == "D" or carte[0] == "R":  # si la carte est une figure
        return 10
    else:  # si la carte est un nombre entre 2 et 10
        return int(carte[0])
    # Fonction à tester


def init_pioche(n):
    pioche = paquet() * n  # crée le paquet non mélangé
    pioche2 = []
    for i in range(len(pioche)):  # pour chaque élément de la pioche
        indice = random.randint(0, 52 * n - i - 1)  # prend un indice aléatoire appartenant à la pioche
        pioche2 += pioche.pop(indice)  # enlève l'élément en question de la première pioche et le met dans la deuxième
    return pioche2
    # Fonction à completer


def pioche_carte():
    pass
    # Fonction à completer


# A2 - Joueurs et scores
def init_joueurs(n):
    pass
    # Fonction à completer


def init_scores(joueurs, v):
    pass
    # Fonction à completer


def premier_tour(joueurs):
    pass
    # Fonction à completer


def gagnant(scores):
    pass
    # Fonction à completer


# B1 - Tour d'un joueur
def continuer():
    return input_protege("Souhaitez-vous continuer?", str, "list", (), ["oui", "Oui", "OUI", "non", "Non", "NON"]) in [
        "oui", "Oui", "OUI"]


def tour_joueur(j, joueurs, pioche, scores):
    veut_continuer = continuer()
    if veut_continuer:
        scores[j] += valeur_carte(pioche[0])
    if not veut_continuer or scores[j] > 21:
        joueurs.remove(j)

    # Fonction à tester


# B2 - Une partie complète
def tour_complet(joueurs, pioche, scores):
    for j in joueurs:
        tour_joueur(j, joueurs, pioche, scores)
    # Fonction à tester


def partie_finie(joueurs, scores):
    return (21 in scores.values()) or (joueurs == [])
    # Fonction à tester


def partie_complete(joueurs, pioche, scores, victoires):
    while not partie_finie(joueurs, scores):
        tour_complet(joueurs, pioche, scores)
    victoires[gagnant(scores)] += 1
    # Fonction à tester


# E - Diverses fonctions supplémentaires
def input_protege(question, type_attendu, type_ensemble, intervalle_reponses_possibles, liste_reponses_possibles):
    """
    question=question to ask the user
    input_type=type of the input needed (example: int, float, str)
    range_or_list= wether the input needs to be part of a range or a list, "range", "list" or "none" (actually anything other than "range" or "list" will result in no value check
    range= range the input needs to be part of (example: (4, 8) here 8 is not included while 4 is) leave as empty if not applicable
    list= list the input needs to be part of (example: [4, 8] or list1 ) leave as empty if not applicable
    """
    saisie = input(question)
    type_verifie = False
    valeur_verifie = False

    while not (type_verifie and valeur_verifie):
        try:
            saisie_modifie = type_attendu(saisie)

        except:
            print("Votre saisie n'est pas du type ", type_attendu.__name__, ". Merci de saisir un ",
                  type_attendu.__name__)
            saisie = input()

        else:
            type_verifie = True
            if type_ensemble == "range":
                if saisie_modifie in range(intervalle_reponses_possibles[0], intervalle_reponses_possibles[1]):
                    valeur_verifie = True
                else:
                    print("Votre saisie n'est pas comprise dans l'intervalle : ", intervalle_reponses_possibles,
                          ". Merci de saisir une valeur comprise dans : ", intervalle_reponses_possibles)
                    print(valeur_verifie)
                    saisie = input()
            elif type_ensemble == "list":
                if saisie_modifie in liste_reponses_possibles:
                    valeur_verifie = True
                else:
                    print("Votre saisie n'est pas comprise dans la liste : ", liste_reponses_possibles,
                          ". Merci de saisir une valeur comprise dans : ", liste_reponses_possibles)
                    saisie = input()
            else:
                valeur_verifie = True
            print(valeur_verifie)
    return saisie_modifie
