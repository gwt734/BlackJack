# Fichier où stocker toutes les fonctions nécessaires à l'affichage du jeu
import time

import pygame

import Constantes

import sys


def initialisation_fenetre():
    pygame.init()
    fenetre = pygame.display.set_mode(Constantes.TAILLE_FENETRE)
    pygame.display.set_caption('BlackJack')
    polices = {}
    polices[police_petite] = pygame.font.Font('freesansbold.ttf', 18)
    police_moyenne = pygame.font.Font('freesansbold.ttf', 24)
    police_grande = pygame.font.Font('freesansbold.ttf', 32)
    mise_a_jour_affichage(fenetre, police, "Bonjour")
    return fenetre, polices


def pygame_bool_input():
    while True:
        for evenement in pygame.event.get():
            if evenement.type == pygame.KEYDOWN:

                if evenement.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif evenement.key == pygame.K_SPACE:
                    return True
                elif evenement.key == pygame.K_TAB:
                    return False


def mise_a_jour_affichage(fenetre, police, texte_a_afficher):
    fenetre.fill(Constantes.VERT_BLACKJACK)
    creer_boite_texte((Constantes.TAILLE_FENETRE[0] // 2, Constantes.TAILLE_FENETRE[1] // 2), texte_a_afficher, fenetre, police)
    creer_boite_texte((Constantes.TAILLE_FENETRE[0] * 0.1, Constantes.TAILLE_FENETRE[1] * 0.9), "espace pour oui tab pour non", fenetre, police)
    pygame.display.update()


def creer_boite_texte(position, texte_a_afficher, fenetre, police, couleur_texte=Constantes.BLANC, couleur_fond=None):
    texte = police.render(texte_a_afficher, True, couleur_texte, couleur_fond)
    boite_texte = texte.get_rect()
    boite_texte.center = (position[0], position[1])
    fenetre.blit(texte, boite_texte)


def texte_input(fenetre, police, question, valeur_par_default, avertissement="", affiche_scores=False, scores={}, joueurs_partie=[], encore={}):
    print("texte_input")
    saisie = str(valeur_par_default)
    valide = False
    dernier_tick = time.time()
    affiche_curseur = True
    fenetre.fill(Constantes.VERT_BLACKJACK)
    creer_boite_texte((Constantes.TAILLE_FENETRE[0] // 2, Constantes.TAILLE_FENETRE[1] // 2), saisie + "|"*int(affiche_curseur) + " "*(10-len(saisie)-1*int(affiche_curseur)), fenetre, police, couleur_fond=Constantes.VERT_OMBRE)
    creer_boite_texte((Constantes.TAILLE_FENETRE[0] // 2, Constantes.TAILLE_FENETRE[1] // 3), question, fenetre, police)
    creer_boite_texte((Constantes.TAILLE_FENETRE[0] // 2, Constantes.TAILLE_FENETRE[1] // 1.5), avertissement, fenetre, police, couleur_texte=Constantes.ROUGE)
    if affiche_scores:
        creer_boites_texte_scores(fenetre, police, scores, joueurs_partie, encore)
    pygame.display.update()
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
        creer_boite_texte((Constantes.TAILLE_FENETRE[0] // 2, Constantes.TAILLE_FENETRE[1] // 2), saisie + "|"*int(affiche_curseur) + " "*(10-len(saisie)-1*int(affiche_curseur)), fenetre, police, couleur_fond=Constantes.VERT_OMBRE)
        creer_boite_texte((Constantes.TAILLE_FENETRE[0] // 2, Constantes.TAILLE_FENETRE[1] // 3), question, fenetre, police)
        creer_boite_texte((Constantes.TAILLE_FENETRE[0] // 2, Constantes.TAILLE_FENETRE[1] // 1.5), avertissement, fenetre, police, couleur_texte=Constantes.ROUGE)
        if affiche_scores:
            creer_boites_texte_scores(fenetre, police, scores, joueurs_partie, encore)
        pygame.display.update()
        if time.time()-dernier_tick > 0.5:
            dernier_tick = time.time()
            affiche_curseur = not affiche_curseur  # Inverse la valeur
    return saisie


def creer_boites_texte_scores(fenetre, police, scores, joueurs_partie, encore):
    nombre_de_joueurs = len(joueurs_partie)
    for index_joueur in range(nombre_de_joueurs):
        nom_joueur = joueurs_partie[index_joueur]
        score = scores[nom_joueur]
        if score > 21:
            couleur_texte = Constantes.ROUGE
        elif score == 21:
            couleur_texte = Constantes.OR
        elif not encore[nom_joueur]:
            couleur_texte = Constantes.GRIS
        else:
            couleur_texte = Constantes.BLANC
        print(couleur_texte)
        creer_boite_texte(((Constantes.TAILLE_FENETRE[0] // nombre_de_joueurs)*index_joueur, Constantes.TAILLE_FENETRE[1] // 4), nom_joueur+" : "+str(scores[nom_joueur]), fenetre, police, couleur_texte=couleur_texte)
