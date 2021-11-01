# Fichier où stocker toutes les fonctions nécessaires au jeu

import Constantes
import random
from statistics import mean


#########################          A1 - Paquet de cartes          #########################

def paquet():
    pile = []
    for i in range(len(Constantes.COULEUR)):  # pour chaque couleur (4)
        for j in range(len(Constantes.VALEUR)):  # pour chaque valeur de carte (13)
            pile += [Constantes.VALEUR[j] + " de " + Constantes.COULEUR[i]]  # ajoute la carte à la pile
    return pile


def valeur_carte(carte):
    if carte[0] == "A":  # si la carte est un As
        return input_protege("Quelle valeur choisissez vous pour l'as", type_attendu=int, range_or_list="list", liste_reponses_possibles=[1, 11])  # demande la valeur souhaitée (1 ou 11)
    elif carte[0] in "VDR1":  # si la carte est une figure ou un 10
        return 10
    else:  # si la carte est un nombre entre 2 et 9
        return int(carte[0])


def init_pioche(n):
    pioche = paquet() * n  # crée le paquet non mélangé
    random.shuffle(pioche)
    return pioche
    # Fonction à tester


def pioche_carte(pioche):  # pioche une seule carte
    """retour = []
    for i in range(x): # autant de fois que de cartes à piocher
        retour=pioche.pop(0)  # enlève la carte de la pioche et la met dans la liste de retour
    return retour[]"""
    return pioche.pop(0)
    # Fonction à tester


#########################          A2 - Joueurs et scores          #########################

def init_joueurs(n):
    joueurs = []
    for i in range(n):  # Pour chaque joueur on demande àa l'utilisateur le nom
        joueurs.append(input_protege("Quel est le nom du joueur " + str(i+1)))
    return joueurs


def init_scores(joueurs, v=0):
    scores = {}
    for i in joueurs:   # Pour chaque joueur
        scores[i] = v   # On assigne la valeur v au score du joueur actuel
    return scores


def premier_tour(joueurs_partie, pioche):
    scores = init_scores(joueurs_partie)   # On initialise les scores
    for tour in range(2):   # on fait 2 tours de distribution de cartes (souvent le cas dans les jeux de carte)
        for i in scores.keys():     # On parcours les joueurs
            scores[i] += valeur_carte(pioche_carte(pioche))     # On augmente le score de la valeur d'une carte piochée
    return scores


def gagnant(scores):
    maximum = 0
    for i in scores.keys():     # On parcours les joueurs
        if maximum < scores[i] <= 21:
            maximum = scores[i]
            joueur_gagnant = i
    return joueur_gagnant
    # Fonction à tester


#########################          B1 - Tour d'un joueur          #########################

def continuer_tour():
    return input_protege("Souhaitez-vous piocher une autre carte? ", range_or_list="list", liste_reponses_possibles=["oui", "Oui", "OUI", "non", "Non", "NON"]) in [
        "oui", "Oui", "OUI"]


def init_continuer_tour(joueurs_partie):
    encore = {}
    for joueur in joueurs_partie:  # Pour chaque joueur
        encore[joueur] = True
    return encore


def continuer_partie():
    return input_protege("Souhaitez-vous commencer une autre partie? ", range_or_list="list", liste_reponses_possibles=["oui", "Oui", "OUI", "non", "Non", "NON"]) in [
        "oui", "Oui", "OUI"]


def tour_joueur(j, joueurs_partie, pioche, scores, encore):
    print(j, " : votre score est : ", scores[j])    # Pour se repérer
    print(pioche) # Pour le débogage
    encore[j] = continuer_tour()   # On demande au joueur s'il veut continuer
    if encore[j]:   # si le joueur veut continuer
        scores[j] += valeur_carte(pioche_carte(pioche))  # On augmente le score de la valeur de la carte piochée
    if scores[j] > 21:    # si le joueur dépasse 21 points
        joueurs_partie.remove(j)   # On l'élimine
    print(scores)  # pour le débogage
    """if scores[j] == 21:  # si le joueur atteint 21 points, on arrête la partie immédiatement
        partie_finie(joueurs_partie, scores, encore)"""
    # Fonction à tester


#########################          B2 - Une partie complète          #########################

def tour_complet(joueurs_partie, pioche, scores, encore):  # Pour chaque joueur encore dans la partie on lui fait un tour
    for j in joueurs_partie:
        if encore[j] and not(partie_finie(joueurs_partie, scores, encore)):
            tour_joueur(j, joueurs_partie, pioche, scores, encore)
    # Fonction à tester


def partie_finie(joueurs_partie, scores, encore):
    """renvoie True si un joueur a 21 points, si il ne reste plus qu'un joueur en dessous de 21 points
    ou si aucun joueur ne veut continuer à piocher"""
    return (21 in scores.values()) or (len(joueurs_partie) == 1) or not(True in encore.values())
    # Fonction à tester


def partie_complete(joueurs, pioche, scores, victoires, encore):
    while not partie_finie(joueurs, scores, encore):    # Tant que  la partie n'est pas finie on repete un tour complet
        tour_complet(joueurs, pioche, scores, encore)
        print(encore)  # pour le débogage
    victoires[gagnant(scores)] += 1     # A la fin de la partie on incremente le score du gagnant
    # Fonction à tester


#########################          C - Intelligence artificielle          #########################

def moyenne_paquet(pioche):
    valeurs = []
    for carte in pioche:
        valeurs.append(valeur_carte(carte))
    return mean(valeurs)
    # Fonction à tester


def choix_intelligent(score, pioche, risque=False, securite=False):
    estimation = moyenne_paquet(pioche)
    if (risque == securite == False) or (risque == securite == True):  # si l'algorithme doit jouer de manière optimale
        if estimation <= 21 - score:
            pass  # il faut continuer
        else:
            pass  # il faut arreter
    elif risque:  # si l'algorithme doit prendre des risques
        if estimation / 2 <= 21 - score:  # souvent vrai, risque de perdre
            pass  # il faut continuer
        else:
            pass  # il faut arreter
    else:  # si l'algorithme ne doit pas prendre de risques
        if estimation * 2 <= 21 - score:  # rarement vrai, peu de chances de perdre
            pass  # il faut continuer
        else:
            pass  # il faut arreter


#########################          E - Diverses fonctions supplémentaires          #########################

def input_protege(question, type_attendu=str, range_or_list="none", intervalle_reponses_possibles=(), liste_reponses_possibles=[]):
    """
    question = question à poser (str)
    type_attendu = type de variable attendu (str par defaut)
    range_or_list = "range" pour un intervalle, "list" pour une liste de valeur, rien pour ignorer la condition
    intervalle_reponses_possibles = à completer pour un test d'intervalle
    liste_reponses_possibles = à completer pour un test de liste
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
            if range_or_list == "range":
                if saisie_modifie in range(intervalle_reponses_possibles[0], intervalle_reponses_possibles[1]):
                    valeur_verifie = True
                else:
                    print("Votre saisie n'est pas comprise dans l'intervalle : ", intervalle_reponses_possibles,
                          ". Merci de saisir une valeur comprise dans : ", intervalle_reponses_possibles)
                    saisie = input()
            elif range_or_list == "list":
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
