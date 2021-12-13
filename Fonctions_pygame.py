# Fichier où stocker toutes les fonctions nécessaires à l'affichage du jeu
import time

import pygame

import Constantes

import sys

import Fonctions


def initialisation_fenetre():
    pygame.init()
    fenetre = pygame.display.set_mode(Constantes.TAILLE_FENETRE)
    pygame.display.set_caption('BlackJack')
    polices = {"petite": pygame.font.Font('freesansbold.ttf', Constantes.POLICE_TAILLE_PETITE),
               "moyenne": pygame.font.Font('freesansbold.ttf', Constantes.POLICE_TAILLE_MOYENNE),
               "grande": pygame.font.Font('freesansbold.ttf', Constantes.POLICE_TAILLE_GRANDE)}
    creer_boite_texte((Constantes.TAILLE_FENETRE[0] // 2, Constantes.TAILLE_FENETRE[1] // 2), "Bonjour", fenetre,
                      polices["grande"])
    creer_boite_texte((Constantes.TAILLE_FENETRE[0] * 0.1, Constantes.TAILLE_FENETRE[1] * 0.9),
                      "espace pour oui tab pour non", fenetre, polices["moyenne"])
    mise_a_jour_affichage(fenetre, polices)
    return fenetre, polices


def pygame_bool_input():
    """Fonction qui attends une touche de l'utilisateur et retourne vrai si ESPACE est touché et faux si TAB est touché."""
    while True:
        for evenement in pygame.event.get():  # Parcours tous les évenements recus depuis le dernier tick
            if evenement.type == pygame.KEYDOWN:   #

                if evenement.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif evenement.key == pygame.K_SPACE:
                    return True
                elif evenement.key == pygame.K_TAB:
                    return False


def mise_a_jour_affichage(fenetre, polices):
    #fenetre.fill(Constantes.VERT_BLACKJACK)
    affichages_statiques(fenetre, polices)
    pygame.display.update()


def creer_boite_texte(position, texte_a_afficher, fenetre, police, couleur_texte=Constantes.BLANC, couleur_fond=None):
    texte = police.render(texte_a_afficher, True, couleur_texte, couleur_fond)
    boite_texte = texte.get_rect()
    boite_texte.center = (position[0], position[1])
    fenetre.blit(texte, boite_texte)


def texte_input(fenetre, polices, question, valeur_par_default="", avertissement="", affiche_scores=False, scores=None,
                joueurs_partie=None, encore=None, kopecs=None, j=-1, taille_police=None):
    if scores is None:
        scores = {}
    if encore is None:
        encore = {}
    if joueurs_partie is None:
        joueurs_partie = []
    saisie = str(valeur_par_default)
    valide = False
    dernier_tick = time.time()
    affiche_curseur = True
    fenetre.fill(Constantes.VERT_BLACKJACK)
    creer_boite_texte((Constantes.TAILLE_FENETRE[0] // 2, Constantes.TAILLE_FENETRE[1] // 2),
                      saisie + "|" * int(affiche_curseur) + " " * (10 - len(saisie) - 1 * int(affiche_curseur)),
                      fenetre, polices["moyenne"], couleur_fond=Constantes.VERT_OMBRE)
    creer_boite_texte((Constantes.TAILLE_FENETRE[0] // 2, Constantes.TAILLE_FENETRE[1] // 3), question, fenetre,
                      polices["grande"])
    creer_boite_texte((Constantes.TAILLE_FENETRE[0] // 2, Constantes.TAILLE_FENETRE[1] // 1.5), avertissement, fenetre,
                      polices["petite"], couleur_texte=Constantes.ROUGE)
    fenetre.fill(Constantes.VERT_BLACKJACK)
    if affiche_scores:
        creer_boites_texte_scores(fenetre, polices, scores, encore, kopecs, j)
    mise_a_jour_affichage(fenetre, polices)
    while not valide:
        for evenement in pygame.event.get():
            if evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif evenement.key == pygame.K_RETURN:
                    valide = True
                elif evenement.key == pygame.K_BACKSPACE:
                    saisie = saisie[:-1]
                else:
                    if len(saisie) < 10:
                        saisie += evenement.unicode
        fenetre.fill(Constantes.VERT_BLACKJACK)
        creer_boite_texte((Constantes.TAILLE_FENETRE[0] // 2, Constantes.TAILLE_FENETRE[1] // 2),
                          saisie + "|" * int(affiche_curseur) + " " * (10 - len(saisie) - 1 * int(affiche_curseur)),
                          fenetre, polices["moyenne"], couleur_fond=Constantes.VERT_OMBRE)
        creer_boite_texte((Constantes.TAILLE_FENETRE[0] // 2, Constantes.TAILLE_FENETRE[1] // 3), question, fenetre,
                          polices[taille_police])
        creer_boite_texte((Constantes.TAILLE_FENETRE[0] // 2, Constantes.TAILLE_FENETRE[1] // 1.5), avertissement,
                          fenetre,
                          polices["petite"], couleur_texte=Constantes.ROUGE)
        if affiche_scores:
            creer_boites_texte_scores(fenetre, polices, scores, encore, kopecs, j)
        affichages_statiques(fenetre, polices)
        pygame.display.update()
        if time.time() - dernier_tick > 0.5:
            dernier_tick = time.time()
            affiche_curseur = not affiche_curseur  # Inverse la valeur
    return saisie


def creer_boites_texte_scores(fenetre, polices, scores, encore, kopecs, j=-1):
    joueurs_restants = []
    for joueur in scores.keys():
        if kopecs[joueur] != 0:  #mises
            joueurs_restants.append(joueur)
    nombre_de_joueurs = len(joueurs_restants)
    for index_joueur in range(nombre_de_joueurs):
        nom_joueur = joueurs_restants[index_joueur]
        score = scores[nom_joueur]
        taille_police = "moyenne"
        if nom_joueur == j:
            taille_police = "grande"
        if score > 21:
            couleur_texte = Constantes.ROUGE
        elif nom_joueur == Fonctions.gagnant(scores):
            couleur_texte = Constantes.OR
        elif not encore[nom_joueur]:
            couleur_texte = Constantes.GRIS
        else:
            couleur_texte = Constantes.BLANC
        print(couleur_texte)
        creer_boite_texte(((Constantes.TAILLE_FENETRE[0] // (nombre_de_joueurs+1))*(index_joueur+1), Constantes.TAILLE_FENETRE[1] // 2), "*"*(j == nom_joueur)+nom_joueur+" : "+str(scores[nom_joueur])+"*"*(j == nom_joueur), fenetre, polices[taille_police], couleur_texte=couleur_texte)


def affichages_statiques(fenetre, polices):
    creer_boite_texte((Constantes.TAILLE_FENETRE[0] * 0.07, Constantes.TAILLE_FENETRE[1] * 0.02), "ECHAP pour fermer", fenetre,
                      polices["petite"])