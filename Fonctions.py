# Fichier où stocker toutes les fonctions nécessaires au jeu
import pygame

import Constantes
import random
from statistics import mean
import time
import Fonctions_pygame


#########################          A1 - Paquet de cartes          #########################


def paquet():
    pile = []
    for i in range(len(Constantes.COULEUR)):  # pour chaque couleur (4)
        for j in range(len(Constantes.VALEUR)):  # pour chaque valeur de carte (13)
            pile += [Constantes.VALEUR[j] + " de " + Constantes.COULEUR[i]]  # ajoute la carte à la pile
    return pile


def valeur_carte(fenetre, polices, carte, j, scores):
    if carte[0] == "A":  # si la carte est un As
        if j.upper()[0:3] == "IAR":  # IA qui prend des risques
            print(j, "a choisi 11 comme valeur pour l'As")
            return 11
        elif j.upper()[0:3] == "IAS":  # IA qui privilégie la sécurité
            print(j, "a choisi 1 comme valeur pour l'As")
            return 1
        elif j.upper()[0:2] == "IA":  # IA normale
            valeur = 1 + random.randint(0, 1) * 10
            print(j, "a choisi", valeur, "comme valeur pour l'As")
            return valeur  # choix aléatoire entre 1 et 11
        elif j.upper()[0:3] == "BOB":
            if scores[j] >= 11:
                print(j, "a choisi 1 comme valeur pour l'As")
                return 1
            else:
                print(j, "a choisi 11 comme valeur pour l'As")
                return 11
        else:  # si le joueur est un humain
            return input_protege(question="Quelle valeur choisissez vous pour l'as ? ", type_attendu=int,
                                 range_or_list="list", liste_reponses_possibles=[1, 11], fenetre=fenetre,
                                 polices=polices)  # demande la valeur souhaitée (1 ou 11)
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

def init_joueurs(fenetre, polices, n):
    joueurs = []
    for i in range(n):  # Pour chaque joueur on demande à l'utilisateur le nom
        nom = input_protege(question="Quel est le nom du joueur " + str(i + 1) + " ? ", fenetre=fenetre,
                            polices=polices)
        while nom in joueurs:  # contrôle pour ne pas avoir 2 fois le même nom
            nom = input_protege(question="Ce nom est déjà utilisé, merci d'en entrer un autre : ", fenetre=fenetre,
                                polices=polices)
        joueurs.append(nom)
    return joueurs


def init_scores(joueurs, v=0):
    scores = {}
    for i in joueurs:  # Pour chaque joueur
        scores[i] = v  # On assigne la valeur v au score du joueur actuel
    return scores


def premier_tour(fenetre, polices, joueurs_partie, pioche, kopecs):
    mises = init_scores(joueurs_partie)
    scores = init_scores(joueurs_partie)
    for j in joueurs_partie:
        jeu = []
        for tour in range(2):  # on leur fait piocher 2 cartes
            jeu.append(pioche_carte(pioche))
        print(j, "a pioché", jeu, "au premier tour")
        valeur_premier_tour(fenetre, polices, jeu, j, scores, kopecs, mises)
        print()
        # time.sleep(2)
    print(Constantes.AFFICHAGE + "\n")
    return scores, mises


def valeur_premier_tour(fenetre, polices, jeu, j, scores, kopecs, mises):
    for carte in jeu:  #
        scores[j] += valeur_carte(fenetre, polices, carte, j, scores)
    jeu_texte = " et ".join(jeu)
    if j.upper()[0:2] == "IA":
        print(j, ": score =", scores[j], "et kopecs restants =", kopecs[j])
        mise = ia_mise(j, kopecs)
        print(j, "a misé", mise)
        fenetre.fill(Constantes.VERT_BLACKJACK)
        Fonctions_pygame.creer_boite_texte((Constantes.TAILLE_FENETRE[0] // 2, Constantes.TAILLE_FENETRE[1] // 3),
                                           j + " à pioché " + jeu_texte + " et à misé: " + str(mise), fenetre, polices["grande"])
        Fonctions_pygame.mise_a_jour_affichage(fenetre, polices)
        time.sleep(3)
    elif j.upper()[0:3] == "BOB":
        print(j, ": score =", scores[j], "et kopecs restants =", kopecs[j])
        mise = bob_mise(j, scores, kopecs)
        print(j, "a misé", mise)
        fenetre.fill(Constantes.VERT_BLACKJACK)
        Fonctions_pygame.creer_boite_texte((Constantes.TAILLE_FENETRE[0] // 2, Constantes.TAILLE_FENETRE[1] // 3),
                                           j + " à pioché " + jeu_texte + " et à misé: " + str(mise), fenetre, polices["grande"])
        Fonctions_pygame.mise_a_jour_affichage(fenetre, polices)
        time.sleep(3)
    else:  # si le joueur est un humain
        print(j + ", votre score est de", scores[j])
        print("Et il vous reste", kopecs[j], "kopecs")
        mise = input_protege(question=j + ": Vous avez pioché " + jeu_texte + "     Il vous reste " + str(
            kopecs[j]) + " kopecs" + "    Combien voulez vous miser ? ", type_attendu=int, range_or_list="range",
                             intervalle_reponses_possibles=(1, kopecs[j] + 1), fenetre=fenetre, polices=polices,
                             taille_police="petite")
    mises[j] = mise
    kopecs[j] -= mise


def gagnant(scores):
    maximum = 0
    for i in scores.keys():  # On parcourt les joueurs
        if maximum < scores[i] <= 21:
            maximum = scores[i]
            joueur_gagnant = i
    return joueur_gagnant


#########################          B1 - Tour d'un joueur          #########################

def continuer_tour(fenetre, polices, scores=None, encore=None, kopecs=None, j=None, mises=None):
    # return input_protege(question="Souhaitez-vous piocher une autre carte ? ", range_or_list="list", liste_reponses_possibles=["oui", "Oui", "OUI", "non", "Non", "NON"], fenetre=fenetre, polices=polices) in ["oui", "Oui", "OUI"]
    fenetre.fill(Constantes.VERT_BLACKJACK)
    Fonctions_pygame.creer_boite_texte((Constantes.TAILLE_FENETRE[0] // 2, Constantes.TAILLE_FENETRE[1] // 3),
                                       "Voulez-vous continuer à jouer?", fenetre, polices["grande"])
    Fonctions_pygame.creer_boite_texte((Constantes.TAILLE_FENETRE[0] // 2, 2 * Constantes.TAILLE_FENETRE[1] // 3),
                                       "* Appuyez sur ESPACE pour piocher, TAB pour arrêter de piocher *", fenetre,
                                       polices["petite"], couleur_texte=Constantes.GRIS)
    Fonctions_pygame.creer_boites_texte_scores(fenetre, polices, scores, encore, kopecs, j, mises)
    Fonctions_pygame.mise_a_jour_affichage(fenetre, polices)
    return Fonctions_pygame.pygame_bool_input()


def init_continuer_tour(joueurs_partie):
    encore = {}
    for joueur in joueurs_partie:  # Pour chaque joueur
        encore[joueur] = True
    return encore


def continuer_partie():
    # return input_protege(question="Souhaitez-vous commencer une autre partie ?  ", range_or_list="list", liste_reponses_possibles=["oui", "Oui", "OUI", "non", "Non", "NON"], fenetre=fenetre, polices=polices) in ["oui", "Oui", "OUI"]
    return Fonctions_pygame.pygame_bool_input()


def tour_joueur(fenetre, polices, j, joueurs_partie, pioche, scores, encore, kopecs, mises):
    print("Les scores actuels sont :", scores)
    print(j, " : votre score est : ", scores[j])  # Pour se repérer
    # est-ce que le joueur veut continuer à piocher ?
    fenetre.fill(Constantes.VERT_BLACKJACK)
    Fonctions_pygame.creer_boite_texte((Constantes.TAILLE_FENETRE[0] // 2, Constantes.TAILLE_FENETRE[1] // 3),
                                       "Voulez-vous continuer à jouer?", fenetre, polices["grande"])
    if j[:2].upper() != "IA" and j[:3].upper() != "BOB":
        Fonctions_pygame.creer_boite_texte((Constantes.TAILLE_FENETRE[0] // 2, 2 * Constantes.TAILLE_FENETRE[1] // 3),
                                           "* Appuyez sur ESPACE pour piocher, TAB pour arrêter de piocher *", fenetre,
                                           polices["petite"], couleur_texte=Constantes.GRIS)
    else:
        Fonctions_pygame.creer_boite_texte((Constantes.TAILLE_FENETRE[0] // 2, 2 * Constantes.TAILLE_FENETRE[1] // 3),
                                           "* " + j +" réfléchis *", fenetre,
                                           polices["petite"], couleur_texte=Constantes.GRIS)
    Fonctions_pygame.creer_boites_texte_scores(fenetre, polices, scores, encore, kopecs, j, mises)
    Fonctions_pygame.mise_a_jour_affichage(fenetre, polices)
    if j.upper()[0:3] == "IAR":  # IA qui prend des risques
        time.sleep(2)
        score = scores[j]
        encore[j] = choix_intelligent(score, pioche, risque=True)
    elif j.upper()[0:3] == "IAS":  # IA qui privilégie la sécurité
        time.sleep(2)
        score = scores[j]
        encore[j] = choix_intelligent(score, pioche, securite=True)
    elif j.upper()[0:2] == "IA":  # IA normale
        time.sleep(2)
        score = scores[j]
        encore[j] = choix_intelligent(score, pioche)
    elif j.upper()[0:3] == "BOB":
        time.sleep(2)
        encore[j] = choix_booste(scores, pioche, j)
    else:  # si le joueur est un humain
        encore[j] = continuer_tour(fenetre, polices, scores=scores, encore=encore, kopecs=kopecs,
                                   j=j, mises=mises)  # On demande au joueur s'il veut continuer
    # pioche ou non suivant la réponse précédente
    if encore[j]:  # si le joueur veut continuer
        carte = pioche_carte(pioche)
        print(j, "a pioché", carte)
        fenetre.fill(Constantes.VERT_BLACKJACK)
        Fonctions_pygame.creer_boite_texte((Constantes.TAILLE_FENETRE[0] // 2, Constantes.TAILLE_FENETRE[1] // 3),
                                           j + " a pioché " + str(carte), fenetre, polices["grande"])
        Fonctions_pygame.mise_a_jour_affichage(fenetre, polices)
        time.sleep(1)
        scores[j] += valeur_carte(fenetre, polices, carte, j,
                                  scores)  # On augmente le score de la valeur de la carte piochée
        print(j, ": votre score est maintenant de", scores[j])  # Pour se repérer
    else:
        print(j, "n'a pas pioché")
        fenetre.fill(Constantes.VERT_BLACKJACK)
        Fonctions_pygame.creer_boite_texte((Constantes.TAILLE_FENETRE[0] // 2, Constantes.TAILLE_FENETRE[1] // 3),
                                           j + " a choisi de ne pas piocher.", fenetre, polices["grande"])
        Fonctions_pygame.mise_a_jour_affichage(fenetre, polices)
        time.sleep(1)
    if scores[j] > 21:  # si le joueur dépasse 21 points
        fenetre.fill(Constantes.VERT_BLACKJACK)
        Fonctions_pygame.creer_boite_texte((Constantes.TAILLE_FENETRE[0] // 2, Constantes.TAILLE_FENETRE[1] // 3),
                                           j + " a dépassé 21 et est donc éliminé de cette manche.", fenetre,
                                           polices["grande"])
        Fonctions_pygame.mise_a_jour_affichage(fenetre, polices)
        time.sleep(1)
        joueurs_partie.remove(j)  # On l'élimine
        encore[j] = False

    # time.sleep(2)


#########################          B2 - Une partie complète          #########################

def tour_complet(fenetre, polices, joueurs_partie, pioche, scores, encore,
                 kopecs, mises):  # Pour chaque joueur encore dans la partie on lui fait un tour
    for j in scores.keys():
        if encore[j] and not (partie_finie(joueurs_partie, scores, encore)):
            tour_joueur(fenetre, polices, j, joueurs_partie, pioche, scores, encore, kopecs, mises)
            print()


def partie_finie(joueurs_partie, scores, encore):
    """renvoie True si un joueur a 21 points, si il ne reste plus qu'un joueur en dessous de 21 points
    ou si aucun joueur ne veut continuer à piocher"""
    return (21 in scores.values()) or (len(joueurs_partie) == 1) or (not (True in encore.values()))


def partie_complete(fenetre, polices, joueurs, pioche, scores, encore, kopecs, mises):
    while not partie_finie(joueurs, scores, encore):  # Tant que  la partie n'est pas finie on repete un tour complet
        tour_complet(fenetre, polices, joueurs, pioche, scores, encore, kopecs, mises)
        # print(encore)  # affiche l'état du dictionnaire, pour vérification
    vainqueur = gagnant(scores)
    gain = sum(mises.values())
    kopecs[vainqueur] += gain
    print(vainqueur, "a gagné la partie et remporte", str(gain), "kopecs !")
    fenetre.fill(Constantes.VERT_BLACKJACK)
    Fonctions_pygame.creer_boite_texte((Constantes.TAILLE_FENETRE[0] // 2, Constantes.TAILLE_FENETRE[1] // 3),
                                       vainqueur + " a gagné la partie et remporte " + str(gain) + " kopecs !", fenetre,
                                       polices["grande"])
    Fonctions_pygame.creer_boite_texte((Constantes.TAILLE_FENETRE[0] // 2, Constantes.TAILLE_FENETRE[1] // 2 - 100),
                                       "Les scores finaux sont: ", fenetre, polices["moyenne"], )
    Fonctions_pygame.creer_boite_texte((Constantes.TAILLE_FENETRE[0] // 2, 4 * Constantes.TAILLE_FENETRE[1] // 5),
                                       "* Appuyez sur ESPACE pour continuer, ECHAP pour quitter le jeu *", fenetre,
                                       polices["petite"], couleur_texte=Constantes.GRIS)
    Fonctions_pygame.creer_boites_texte_scores(fenetre, polices, scores, encore, kopecs, mises=mises)
    Fonctions_pygame.creer_boite_texte((Constantes.TAILLE_FENETRE[0] // 2, 2*Constantes.TAILLE_FENETRE[1] // 3 - 100),
                                       "Les kopecs restants: ", fenetre, polices["moyenne"], )
    Fonctions_pygame.creer_boites_texte_kopecs(fenetre, polices, kopecs, mises, scores)
    Fonctions_pygame.creer_boites_texte_gains(fenetre, polices, kopecs, vainqueur, gain, mises, scores)
    Fonctions_pygame.mise_a_jour_affichage(fenetre, polices)


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
    """Intelligence artificielle qui décide de continuer ou non en fonction de son score et des cartes déjà tirées de la pioche"""
    estimation = moyenne_paquet(pioche)  # autour de 6.5
    if not (risque or securite) or (risque and securite):  # si l'algorithme doit jouer de manière optimale
        return score <= 21 - estimation
    elif risque:  # si l'algorithme doit prendre des risques
        return score <= 21 - estimation / 1.5  # souvent vrai, risque de dépasser 21
    else:  # si l'algorithme ne doit pas prendre de risques
        return score <= 21 - estimation * 1.5  # rarement vrai, peu de chances de dépasser 21


def choix_booste(scores, pioche, j):
    """ Intelligence artificielle qui tient compte de son score, de la pioche et de la main des autres joueurs"""
    estimation = moyenne_paquet(pioche)
    if estimation <= 21 - scores[j]:
        return True  # il faut continuer
    points = dict(scores)  # création d'un dictionnaire intermédiaire ne servant qu'à cette IA
    for joueur in scores:  # il contient tous les scores en dessous de 21, donc les joueurs encore dans la partie
        if scores[joueur] > 21:
            del points[joueur]
    meilleur = max(points.values())  # nous pouvons donc rechercher le max des valeurs de ce dictionnaire
    if meilleur != scores[j]:  # si un joueur a plus de points que Bob
        return True
    return False


def ia_mise(j, kopecs):
    """mise arbitraire dépendant du nombre de kopecs restants"""
    valeur = int(0.3 * kopecs[j]) + 10
    while valeur > kopecs[j]:  # pour pas que le nombre de kopecs misés soit supérieur au nombre de kopecs restants
        valeur -= 1
    return valeur


def bob_mise(j, scores, kopecs):
    """mise qui dépend du score du joueur et du score des autres"""
    if scores[j] == 21:
        valeur = kopecs[j]
    elif scores[j] in [20, 19] and (21 not in scores.values()):
        valeur = int(0.4 * kopecs[j]) + 1
    else:
        valeur = int(0.2 * kopecs[j]) + 10
        while valeur > kopecs[j]:  # pour pas que le nombre de kopecs misés soit supérieur au nombre de kopecs restants
            valeur -= 1
    return valeur


#########################          E - Diverses fonctions supplémentaires          #########################

def input_protege(question="", type_attendu=str, range_or_list="none", intervalle_reponses_possibles=(),
                  liste_reponses_possibles=None, fenetre=None, polices=None, valeur_par_default="",
                  avertissement="", affiche_scores=False, encore=None, scores=None, kopecs=None, j=-1,
                  taille_police="moyenne", mises=None):
    """
    question = question à poser (str)
    type_attendu = type de variable attendu (str par defaut)
    range_or_list = "range" pour un intervalle, "list" pour une liste de valeur, rien pour ignorer la condition
    intervalle_reponses_possibles = à completer pour un test d'intervalle
    liste_reponses_possibles = à completer pour un test de liste
    """
    if liste_reponses_possibles is None:
        liste_reponses_possibles = []
    saisie = Fonctions_pygame.texte_input(fenetre, polices, question, valeur_par_default=valeur_par_default,
                                          avertissement=avertissement, affiche_scores=affiche_scores, scores=scores,
                                          encore=encore, kopecs=kopecs, j=j, taille_police=taille_police)
    type_verifie = False
    valeur_verifie = False

    while not (type_verifie and valeur_verifie):
        try:
            saisie_modifie = type_attendu(saisie)

        except:
            avertissement = "Votre saisie n'est pas du type" + type_attendu.__name__ + ". Merci de saisir un" + type_attendu.__name__
            saisie = Fonctions_pygame.texte_input(fenetre, polices, question, valeur_par_default=valeur_par_default,
                                                  avertissement=avertissement, affiche_scores=affiche_scores,
                                                  scores=scores,
                                                  encore=encore, kopecs=kopecs, j=j, taille_police=taille_police)

        else:
            type_verifie = True
            if range_or_list == "range":
                if saisie_modifie in range(intervalle_reponses_possibles[0], intervalle_reponses_possibles[1]):
                    valeur_verifie = True
                else:
                    avertissement = "Votre saisie n'est pas comprise entre" + str(
                        intervalle_reponses_possibles[0]) + "et" + str(intervalle_reponses_possibles[
                                                                           1] - 1) + ". Merci de saisir une valeur comprise dans cet intervalle"
                    saisie = Fonctions_pygame.texte_input(fenetre, polices, question,
                                                          valeur_par_default=valeur_par_default,
                                                          avertissement=avertissement, affiche_scores=affiche_scores,
                                                          scores=scores, encore=encore, kopecs=kopecs, j=j,
                                                          taille_police=taille_police)
            elif range_or_list == "list":
                if saisie_modifie in liste_reponses_possibles:
                    valeur_verifie = True
                else:
                    avertissement = "Votre saisie n'est pas comprise dans la liste : " + str(
                        liste_reponses_possibles) + ". Merci de saisir une valeur comprise dans : " + str(
                        liste_reponses_possibles)
                    saisie = Fonctions_pygame.texte_input(fenetre, polices, question,
                                                          valeur_par_default=valeur_par_default,
                                                          avertissement=avertissement, affiche_scores=affiche_scores,
                                                          scores=scores,
                                                          encore=encore, kopecs=kopecs, j=j,
                                                          taille_police=taille_police, mises=mises)
            else:
                valeur_verifie = True
            # print(valeur_verifie)
    return saisie_modifie


def fin_de_partie(kopecs, joueurs):
    """affichage de fin de partie pour que les joueurs se repèrent"""
    print(Constantes.AFFICHAGE)
    for joueur in kopecs:
        if kopecs[joueur] == 0:
            print(joueur, "est éliminé")
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
    diff = sorted(difference.items(), key=lambda t: t[1],
                  reverse=True)  # trie le dictionnaire et rend une liste de couples
    if nb_parties == 1:
        print("\nSur la partie :")
    else:
        print("\nSur l'ensemble des", nb_parties, "parties :")
    for couple in diff:
        if couple[1] == -100:
            print(couple[0], "a tout perdu")
        elif couple[1] < 0:
            print(couple[0], "a perdu", abs(couple[1]), "kopecs  (" + str(couple[1] + 100) + " restants)")
        else:
            print(couple[0], "a gagné", couple[1], "kopecs  (" + str(couple[1] + 100) + " restants)")
