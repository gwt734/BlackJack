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


def valeur_carte(carte, j, scores):
    if carte[0] == "A":  # si la carte est un As
        if j.upper()[0:2] == "IA":
                return 1 + random.randint(0,1) * 10  # choix aléatoire entre 1 et 11
        elif j.upper()[0:3] == "BOB":
            if scores[j] > 11:
                return 1
            else :
                return 11
        else:  # si le joueur est un humain
            return input_protege("Quelle valeur choisissez vous pour l'as ? ", type_attendu=int, range_or_list="list", liste_reponses_possibles=[1, 11])  # demande la valeur souhaitée (1 ou 11)
    elif carte[0] in "VDR1":  # si la carte est une figure ou un 10
        return 10
    else:  # si la carte est un nombre entre 2 et 9
        return int(carte[0])


def init_pioche(n):
    pioche = paquet() * n  # crée le paquet non mélangé
    random.shuffle(pioche)
    return pioche


def pioche_carte(pioche):  # pioche une seule carte
    """retour = []
    for i in range(x): # autant de fois que de cartes à piocher
        retour=pioche.pop(0)  # enlève la carte de la pioche et la met dans la liste de retour
    return retour[]"""
    return pioche.pop(0)


#########################          A2 - Joueurs et scores          #########################

def init_joueurs(n):
    joueurs = []
    for i in range(n):  # Pour chaque joueur on demande à l'utilisateur le nom
        nom = input_protege("Quel est le nom du joueur " + str(i+1)+" ?  ")
        while nom in joueurs:  # contrôle pour ne pas avoir 2 fois le même nom
            nom = input_protege("Ce nom est déjà utilisé, merci d'en entrer un autre : ")
        joueurs.append(nom)
    return joueurs


def init_scores(joueurs, v=0):
    scores = {}
    for i in joueurs:   # Pour chaque joueur
        scores[i] = v   # On assigne la valeur v au score du joueur actuel
    return scores


def premier_tour(joueurs_partie, pioche, kopecs):
    mises = init_scores(joueurs_partie)
    scores = init_scores(joueurs_partie)
    for j in joueurs_partie:   #
        jeu = []
        for tour in range(2):     # 
            jeu.append(pioche_carte(pioche))
        print(j, "a pioché", jeu, "au premier tour")
        valeur_premier_tour(jeu, j, scores, kopecs, mises)
        print()
    return scores, mises


def valeur_premier_tour(jeu, j, scores, kopecs, mises):
    for carte in jeu:     #
        scores[j] += valeur_carte(carte, j, scores)
    if j.upper()[0:2] == "IA":
        print(j,": score =", scores[j], "et kopecs restants =", kopecs[j])
        mise = ia_mise(j, kopecs)
        print(j, "a misé", mise)
    elif j.upper()[0:3] == "BOB":
        print(j,": score =", scores[j], "et kopecs restants =", kopecs[j])
        mise = bob_mise(j, scores, kopecs)
        print(j, "a misé", mise)
    else:  # si le joueur est un humain
        print(j+", votre score est de", scores[j])
        print("Et il vous reste",kopecs[j],"kopecs")
        mise = input_protege(j+" : combien voulez vous miser ? ", int, "range", (1, kopecs[j]+1))
    mises[j] = mise
    kopecs[j] -= mise
    # print("kopecs", kopecs)
    # print("mises", mises)


def gagnant(scores):
    maximum = 0
    for i in scores.keys():     # On parcourt les joueurs
        if maximum < scores[i] <= 21:
            maximum = scores[i]
            joueur_gagnant = i
    return joueur_gagnant


#########################          B1 - Tour d'un joueur          #########################

def continuer_tour():
    return input_protege("Souhaitez-vous piocher une autre carte ? ", range_or_list="list", liste_reponses_possibles=["oui", "Oui", "OUI", "non", "Non", "NON"]) in [
        "oui", "Oui", "OUI"]


def init_continuer_tour(joueurs_partie):
    encore = {}
    for joueur in joueurs_partie:  # Pour chaque joueur
        encore[joueur] = True
    return encore


def continuer_partie():
    return input_protege("Souhaitez-vous commencer une autre partie ?  ", range_or_list="list", liste_reponses_possibles=["oui", "Oui", "OUI", "non", "Non", "NON"]) in [
        "oui", "Oui", "OUI"]


def tour_joueur(j, joueurs_partie, pioche, scores, encore):
    print(j, " : votre score est : ", scores[j])    # Pour se repérer
    # print(pioche[:4]) # Pour le débogage
    # est-ce que le joueur veut continuer à piocher ?
    if j.upper()[0:2] == "IA":
        score = scores[j]
        encore[j] = choix_intelligent(score, pioche)
    elif j.upper()[0:3] == "BOB":
        encore[j] = choix_booste(scores, pioche, j)
    else:  # si le joueur est un humain
        encore[j] = continuer_tour()   # On demande au joueur s'il veut continuer
    # pioche ou non suivant la réponse précédente
    if encore[j]:   # si le joueur veut continuer
        carte = pioche_carte(pioche)
        print(j,"a pioché",carte)
        scores[j] += valeur_carte(carte, j, scores)  # On augmente le score de la valeur de la carte piochée
    else:
        print(j,"n'a pas pioché")
    if scores[j] > 21:    # si le joueur dépasse 21 points
        joueurs_partie.remove(j) # On l'élimine
        encore[j] = False
    print(scores)  #


#########################          B2 - Une partie complète          #########################

def tour_complet(joueurs_partie, pioche, scores, encore):  # Pour chaque joueur encore dans la partie on lui fait un tour
    for j in scores.keys():
        if encore[j] and not(partie_finie(joueurs_partie, scores, encore)):
            tour_joueur(j, joueurs_partie, pioche, scores, encore)
            print("*\n**\n*")


def partie_finie(joueurs_partie, scores, encore):
    """renvoie True si un joueur a 21 points, si il ne reste plus qu'un joueur en dessous de 21 points
    ou si aucun joueur ne veut continuer à piocher"""
    return (21 in scores.values()) or (len(joueurs_partie) == 1) or (not(True in encore.values()))


def partie_complete(joueurs, pioche, scores, encore, kopecs, mises):
    while not partie_finie(joueurs, scores, encore):    # Tant que  la partie n'est pas finie on repete un tour complet
        tour_complet(joueurs, pioche, scores, encore)
        # print(encore)  # pour le débogage
    vainqueur = gagnant(scores)
    gain = sum(mises.values())
    kopecs[vainqueur] += gain
    print(vainqueur,"a gagné la partie et remporte", str(gain), "kopecs !")
    


#########################          C - Intelligence artificielle          #########################

def moyenne_paquet(pioche):
    """fonction qui calcule la valeur moyenne d'un paquet de carte"""
    valeurs = []
    for carte in pioche:
        if carte[0] == "A":
            valeurs.append(1)  # l'as vaut 1 par défaut et l'IA choisira sa valeur en fonction de son score
        elif carte[0] in "VDR1":  # si la carte est une figure ou un 10
            valeurs.append(10)
        else:  # si la carte est un nombre entre 2 et 9
            valeurs.append(int(carte[0]))
    return mean(valeurs)


def choix_intelligent(score, pioche, risque=False, securite=False):
    estimation = moyenne_paquet(pioche)
    if (not(risque) and not(securite)) or (risque and securite):  # si l'algorithme doit jouer de manière optimale
        if estimation <= 21 - score:
            return True  # il faut continuer
        else:
            return False  # il faut arreter
    elif risque:  # si l'algorithme doit prendre des risques
        if estimation / 2 <= 21 - score:  # souvent vrai, risque de dépasser 21
            return True # il faut continuer
        else:
            return False # il faut arreter
    else:  # si l'algorithme ne doit pas prendre de risques
        if estimation * 2 <= 21 - score:  # rarement vrai, peu de chances de dépasser 21
            return True  # il faut continuer
        else:
            return False  # il faut arreter


def choix_booste(scores, pioche, j):  # El famoso BOB
    """ Intelligence artificielle qui tient compte de la main des autres joueurs"""
    estimation = moyenne_paquet(pioche)
    if estimation <= 21 - scores[j]:
        return True  # il faut continuer
    meilleur = max(scores.values())
    if meilleur != scores[j]:  # si un joueur a plus de points que Bob
        return True
    return False


def ia_mise(j, kopecs):
    valeur = int(0.2 * kopecs[j])+10
    while valeur > kopecs[j]:
        valeur -= 1
    return valeur


def bob_mise(j, scores, kopecs):
    if scores[j] == 21:
        valeur = kopecs[j]
    elif scores[j] in [20,19,14,13] and (not 21 in scores.values()):
        valeur = int(0.5 * kopecs[j]) + 1
    else:
        valeur = int(0.2 * kopecs[j]) + 10
        while valeur > kopecs[j]:
            valeur -= 1
    return valeur



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
            # print(valeur_verifie)
    return saisie_modifie


def fin_de_jeu(kopecs, nb_parties):
    """Affiche les résultats totaux après l'ensemble des parties"""
    difference = init_scores(kopecs.keys())
    for joueur in kopecs:
        difference[joueur] = kopecs[joueur] - 100
    diff = sorted(difference.items(), key=lambda t: t[1], reverse=True)  # trie le dictionnaire et rend une liste de couples
    print("Sur l'ensemble des", nb_parties, "parties :")
    for couple in diff:
        if couple[1] < 0:
            print(couple[0], "a perdu", abs(couple[1]), "kopecs")
        else:
            print(couple[0], "a gagné", couple[1], "kopecs")
