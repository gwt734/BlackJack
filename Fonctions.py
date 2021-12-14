# Fichier où stocker toutes les fonctions nécessaires au jeu

import Constantes
import random
from statistics import mean
import time


#########################          A1 - Paquet de cartes          #########################

def paquet():
    pile = []
    for i in range(len(Constantes.COULEUR)):  # pour chaque couleur (4)
        for j in range(len(Constantes.VALEUR)):  # pour chaque valeur de carte (13)
            pile += [Constantes.VALEUR[j] + " de " + Constantes.COULEUR[i]]  # ajoute la carte à la pile
    return pile


def valeur_carte(carte, j, scores):
    """Affecte une valeur à une carte, cas particulier de l'As pour chacune des 5 situations suivantes :
    le joueur est une des 4 IA (4 différentes manières de choisir) ou le joueur est un humain (on lui demande)"""
    if carte[0] == "A":  # si la carte est un As
        if j.upper()[0:3] == "IAR":  # IA qui prend des risques
            print(j, "a choisi 11 comme valeur pour l'As")
            return 11
        elif j.upper()[0:3] == "IAS":  # IA qui privilégie la sécurité
            print(j, "a choisi 1 comme valeur pour l'As")
            return 1
        elif j.upper()[0:2] == "IA":  # IA normale
            valeur = 1 + random.randint(0,1) * 10  # choix aléatoire entre 1 et 11
            print(j, "a choisi", valeur, "comme valeur pour l'As")
            return valeur
        elif j.upper()[0:3] == "BOB":  # choix en fonction du score
            if scores[j] >= 11:  # test pour ne pas dépasser 21
                print(j, "a choisi 1 comme valeur pour l'As")
                return 1
            else:
                print(j, "a choisi 11 comme valeur pour l'As")
                return 11
        else:  # si le joueur est un humain
            return input_protege("Quelle valeur choisissez vous pour l'as ? ", type_attendu=int, range_or_list="list", liste_reponses_possibles=[1, 11])  # demande la valeur souhaitée (1 ou 11)
    elif carte[0] in "VDR1":  # si la carte est une figure ou un 10
        return 10
    else:  # si la carte est un nombre entre 2 et 9
        return int(carte[0])


def init_pioche(n):
    """Crée la pioche en fonction du nombre de joueurs"""
    pioche = paquet() * n  # crée le paquet non mélangé
    random.shuffle(pioche)
    return pioche


def pioche_carte(pioche):
    """Nous avons décidé que cette fonction ne ferait piocher qu'une carte, le cas particulier du premier tour étant géré différemment"""
    return pioche.pop(0)


#########################          A2 - Joueurs et scores          #########################

def init_joueurs(n):
    """Crée la liste des joueurs de taille n, chaque joueur ayant un nom différent"""
    joueurs = []
    for i in range(n):  # Pour chaque joueur on demande à l'utilisateur le nom
        nom = input_protege("Quel est le nom du joueur " + str(i+1)+" ? ")
        while nom in joueurs:  # contrôle pour ne pas avoir 2 fois le même nom
            nom = input_protege("Ce nom est déjà utilisé, merci d'en entrer un autre : ")
        joueurs.append(nom)
    return joueurs


def init_scores(joueurs, v=0):
    """Fonction utile pour créer tous les dictionnaires relatifs à la partie avec différentes valeurs de v"""
    scores = {}
    for joueur in joueurs:   # Pour chaque joueur
        scores[joueur] = v   # On assigne la valeur v au score du joueur actuel
    return scores


def premier_tour(joueurs_partie, pioche, kopecs):
    """Fonction qui gère la distribution de 2 cartes par personne, le choix des mises et assure un bel affichage"""
    print(Constantes.AFFICHAGE)  # pour un affichage aéré dans la console
    mises = init_scores(joueurs_partie)  # création du dictionnaire des mises et scores avec pour valeur 0
    scores = init_scores(joueurs_partie)
    for j in joueurs_partie:
        jeu = []
        for tour in range(2):  # on leur fait piocher 2 cartes
            jeu.append(pioche_carte(pioche))
        print(j, "a pioché", jeu, "au premier tour")
        valeur_premier_tour(jeu, j, scores, kopecs, mises)  # fonction ci-dessous
        print()
        time.sleep(2)  # ajout d'un délai (2 secondes) pour permettre aux humains de lire les choix des IA
    print(Constantes.AFFICHAGE+"\n")
    return scores, mises


def valeur_premier_tour(jeu, j, scores, kopecs, mises):
    """Fonction intermédiaire appelée pour chaque joueur qui gère le choix des mises et l'affichage du choix des IA
    si le joueur est une IA, on appelle les fonctions correspondates aux mises des 2 types d'IA"""
    for carte in jeu:
        if carte[0] == "A" and j.upper()[0:2] == "IA" and scores[j] == 11:  # cas très particulier où "IAr" ou "IA"
            scores[j] += 1                          # pioche 2 As au premier tour et choisirait 2 fois la valeur 11
        else:
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


def gagnant(scores):
    """Fonction appelée en fin de partie qui renvoie le nom du gagnant"""
    maximum = 0
    for i in scores.keys():     # On parcourt les joueurs
        if maximum < scores[i] <= 21:  # en cas d'égalité, c'est le premier joueur qui l'emporte
            maximum = scores[i]
            joueur_gagnant = i
    return joueur_gagnant


#########################          B1 - Tour d'un joueur          #########################

def continuer_tour():
    """réponses limitées à OUI ou NON (majuscules ou pas) par le input_protege()
    renvoie un booléen représentant si la réponse est un OUI"""
    return input_protege("Souhaitez-vous piocher une autre carte ? ", range_or_list="list", liste_reponses_possibles=["oui", "Oui", "OUI", "non", "Non", "NON"]) in [
        "oui", "Oui", "OUI"]


def continuer_partie():
    """réponses limitées à OUI ou NON (majuscules ou pas) par le input_protege()
    renvoie un booléen représentant si la réponse est un OUI"""
    return input_protege("Souhaitez-vous commencer une autre partie ?  ", range_or_list="list", liste_reponses_possibles=["oui", "Oui", "OUI", "non", "Non", "NON"]) in [
        "oui", "Oui", "OUI"]


def tour_joueur(j, joueurs_partie, pioche, scores, encore):
    """Fonction appelée pour chaque joueur qui affiche son score et lui demande s'il veut piocher
    Si le joueur est une IA, on appelle les fonctions correspondates aux choix des 4 IA différentes"""
    print("Les scores actuels sont :",scores)
    print(j, " : votre score est : ", scores[j])    # Pour se repérer
    # est-ce que le joueur veut continuer à piocher ?
    if j.upper()[0:3] == "IAR":  # IA qui prend des risques
        score = scores[j]
        encore[j] = choix_intelligent(score, pioche, risque=True)
    elif j.upper()[0:3] == "IAS":  # IA qui privilégie la sécurité
        score = scores[j]
        encore[j] = choix_intelligent(score, pioche, securite=True)
    elif j.upper()[0:2] == "IA":  # IA normale
        score = scores[j]
        encore[j] = choix_intelligent(score, pioche)
    elif j.upper()[0:3] == "BOB":  # IA boostée qui prend plus de paramètres en compte
        encore[j] = choix_booste(scores, pioche, j)
    else:  # si le joueur est un humain
        encore[j] = continuer_tour()   # On demande au joueur s'il veut continuer
    # pioche ou non suivant la réponse précédente
    if encore[j]:   # si le joueur veut continuer
        carte = pioche_carte(pioche)
        print(j,"a pioché",carte)
        scores[j] += valeur_carte(carte, j, scores)  # On augmente le score de la valeur de la carte piochée
        print(j, ": votre score est maintenant de", scores[j])  # Pour se repérer
    else:
        print(j,"n'a pas pioché")
    if scores[j] > 21:    # si le joueur dépasse 21 points
        joueurs_partie.remove(j) # On l'élimine
        encore[j] = False
    time.sleep(2)  # ajout d'un délai (2 secondes) pour permettre aux humains de lire les choix des IA


#########################          B2 - Une partie complète          #########################

def tour_complet(joueurs_partie, pioche, scores, encore):
    """Pour chaque joueur encore dans la partie, si le joueur veut continuer et que la partie n'est pas finie, on lui fait un tour"""
    for j in scores.keys():
        if encore[j] and not(partie_finie(joueurs_partie, scores, encore)):
            tour_joueur(j, joueurs_partie, pioche, scores, encore)
            print()  # saut de ligne pour aérer l'affichage


def partie_finie(joueurs_partie, scores, encore):
    """renvoie True si un joueur a 21 points, si il ne reste plus qu'un joueur en dessous de 21 points
    ou si aucun joueur ne veut continuer à piocher"""
    return (21 in scores.values()) or (len(joueurs_partie) == 1) or (not(True in encore.values()))


def partie_complete(joueurs, pioche, scores, encore, kopecs, mises):
    """appelle la fonction tour_complet jusqu'à ce que la partie soit finie"""
    while not partie_finie(joueurs, scores, encore):    # Tant que  la partie n'est pas finie on repete un tour complet
        tour_complet(joueurs, pioche, scores, encore)
        # print(encore)  # affiche l'état du dictionnaire, pour vérification
    vainqueur = gagnant(scores)
    gain = sum(mises.values())
    kopecs[vainqueur] += gain
    print(vainqueur,"a gagné la partie et remporte", str(gain), "kopecs !")
    

#########################          C - Intelligence artificielle          #########################

def moyenne_paquet(pioche):
    """Fonction qui calcule la valeur moyenne d'un paquet de carte, à la manière d'un joueur qui compterait les cartes
    Fcontion utilisée par les 2 types IA"""
    valeurs = []
    for carte in pioche:
        if carte[0] == "A":
            valeurs.append(1)  # l'as vaut 1 par défaut (valeur minimale) et l'IA choisira sa vraie valeur après
        elif carte[0] in "VDR1":  # si la carte est une figure ou un 10
            valeurs.append(10)
        else:  # si la carte est un nombre entre 2 et 9
            valeurs.append(int(carte[0]))
    return mean(valeurs)


def choix_intelligent(score, pioche, risque=False, securite=False):
    """Intelligence artificielle qui décide de continuer ou non en fonction de son score et des cartes déjà tirées de la pioche
    Renvoie un booléen (piocher ou non) qui correspondra a la valeur du joueur dans le dictionnaire 'encore'
    Appelée par le nom 'IA' avec potentiellement la lettre 'r' ou 's' après indiquant s'il l'IA prend des risques ou joue la sécurité"""
    estimation = moyenne_paquet(pioche)  # autour de 6.5
    if not(risque or securite) or (risque and securite):  # si l'algorithme doit jouer de manière optimale, raisonnée
        return score <= 21 - estimation
    elif risque:  # si l'algorithme doit prendre des risques
        return score <= 21 - estimation / 1.5  # souvent vrai, risque de dépasser 21
    else:  # si l'algorithme ne doit pas prendre de risques
        return score <= 21 - estimation * 1.5  # rarement vrai, peu de chances de dépasser 21


def choix_booste(scores, pioche, j):
    """Intelligence artificielle qui tient compte de son score, de la pioche et de la main des autres joueurs
    Renvoie un booléen (piocher ou non) qui correspondra a la valeur du joueur dans le dictionnaire 'encore'
    Appelée par le nom 'Bob' """
    estimation = moyenne_paquet(pioche)
    if estimation <= 21 - scores[j]:  # si on peut piocher sans trop de risques
        return True  # il faut continuer
    points = dict(scores)  # création d'un dictionnaire local ne servant qu'à cette IA
    for joueur in scores:  # il contient tous les scores en dessous de 21, donc les joueurs encore dans la partie
        if scores[joueur] > 21:
            del points[joueur]
    meilleur = max(points.values())  # nous pouvons donc rechercher le max des valeurs de ce dictionnaire
    if meilleur != scores[j]:  # si un joueur a plus de points que Bob
        return True  # il faut piocher
    return False


def ia_mise(j, kopecs):
    """Mise arbitraire dépendant du nombre de kopecs restants"""
    valeur = int(0.3 * kopecs[j])+10
    while valeur > kopecs[j]:  # pour pas que le nombre de kopecs misés soit supérieur au nombre de kopecs restants
        valeur -= 1
    return valeur


def bob_mise(j, scores, kopecs):
    """Mise qui dépend du score du joueur et du score des autres"""
    if scores[j] == 21:
        valeur = kopecs[j]  # tapis si 21 dès le premier tour
    elif scores[j] in [20,19] and (21 not in scores.values()):
        valeur = int(0.4 * kopecs[j]) + 1
    else:
        valeur = int(0.2 * kopecs[j]) + 10
        while valeur > kopecs[j]:  # pour pas que le nombre de kopecs misés soit supérieur au nombre de kopecs restants
            valeur -= 1
    return valeur


#########################          E - Diverses fonctions supplémentaires          #########################

def input_protege(question, type_attendu=str, range_or_list="none", intervalle_reponses_possibles=(), liste_reponses_possibles=[]):
    """
    Fonction qui permet d'effectuer des inputs sans risques d'erreur fatales au programme. (utilisée pour toutes les demandes à l'utilisateur)
    elle permet aussi de spécifier un type et un intervalle ou une liste de réponses possibles comme c'est souvent nécessaire.
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
            print("Votre saisie n'est pas du type", type_attendu.__name__, ". Merci de saisir un",
                  type_attendu.__name__)
            saisie = input()

        else:
            type_verifie = True
            if range_or_list == "range":
                if saisie_modifie in range(intervalle_reponses_possibles[0], intervalle_reponses_possibles[1]):
                    valeur_verifie = True
                else:
                    print("Votre saisie n'est pas comprise entre", intervalle_reponses_possibles[0], "et",
                          str(intervalle_reponses_possibles[1]-1),". Merci de saisir une valeur comprise dans cet intervalle")
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


def fin_de_partie(kopecs, joueurs):
    """Affichage de fin de partie pour que les joueurs se repèrent et calcul de la liste des joueurs restants"""
    print(Constantes.AFFICHAGE)
    for joueur in kopecs:
        if kopecs[joueur] == 0:
            print(joueur,"est éliminé")
        else:
            print("Il reste", kopecs[joueur], "kopecs à", joueur)
    print(Constantes.AFFICHAGE)
    joueurs_partie = []
    for j in joueurs:  # après chaque partie on vérifie qu'il reste de l'argent à chaque joueur
        if kopecs[j] > 0:
            joueurs_partie.append(j)  # si c'est le cas, on les ajoute à la partie
    return joueurs_partie


def affichage_fin_de_jeu(kopecs, nb_parties):
    """Affiche les résultats totaux après l'ensemble des parties"""
    difference = init_scores(kopecs.keys())
    for joueur in kopecs:
        difference[joueur] = kopecs[joueur] - 100
    diff = sorted(difference.items(), key=lambda t: t[1], reverse=True)  # trie le dictionnaire et rend une liste de couples
    if nb_parties == 1:
        print("\nSur la partie :")
    else:
        print("\nSur l'ensemble des", nb_parties, "parties :")
    for couple in diff:
        if couple[1] == -100:
            print(couple[0], "a tout perdu")
        elif couple[1] < 0:
            print(couple[0], "a perdu", abs(couple[1]), "kopecs  ("+str(couple[1]+100)+" restants)")
        else:
            print(couple[0], "a gagné", couple[1], "kopecs  ("+str(couple[1]+100)+" restants)")
