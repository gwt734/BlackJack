# Programme principal où est effectuée l'exécution
import Fonctions
import Constantes
import Fonctions_pygame


def main():
    fenetre, polices = Fonctions_pygame.initialisation_fenetre()
    nb_joueurs = Fonctions.input_protege(question="Combien de joueurs jouerons ? ", type_attendu=int,
                                         range_or_list="range", intervalle_reponses_possibles=(2, 16), fenetre=fenetre,
                                         polices=polices, valeur_par_default=3)  # Demande le nombre de joueurs
    print()
    joueurs = Fonctions.init_joueurs(fenetre, polices, nb_joueurs)  # Créé la liste des joueurs
    joueurs_partie = list(joueurs)
    veut_rejouer = True
    kopecs = Fonctions.init_scores(joueurs, v=100)
    nb_parties = 0
    while veut_rejouer:
        nb_parties += 1

        pioche = Fonctions.init_pioche(nb_joueurs)
        # print(pioche[:7])  # affiche les 7 cartes sur le haut de la pioche, pour vérification
        encore = Fonctions.init_continuer_tour(joueurs_partie)
        print(Constantes.AFFICHAGE)  # pour un affichage aéré dans la console
        scores, mises = Fonctions.premier_tour(fenetre, polices, joueurs_partie, pioche, kopecs)
        # print(pioche[:6])  # affiche les 6 cartes sur le haut de la pioche, pour vérification
        Fonctions.partie_complete(fenetre, polices, joueurs_partie, pioche, scores, encore, kopecs, mises)
        joueurs_partie = Fonctions.fin_de_partie(kopecs,
                                                 joueurs)  # calcul des joueurs restants + affichage de fin de partie

        if len(joueurs_partie) == 1:  # si il ne reste qu'un joueur avec des kopecs, le jeu s'arrête
            print(joueurs_partie[0], "est le seul joueur en mesure de continuer, nous avons notre grand gagant !")
            fenetre.fill(Constantes.VERT_BLACKJACK)
            Fonctions_pygame.creer_boite_texte((Constantes.TAILLE_FENETRE[0] // 2, Constantes.TAILLE_FENETRE[1] // 3),
                                               joueurs_partie[0] + " est le seul joueur en mesure de continuer, nous avons notre grand gagant !", fenetre,
                                               polices["moyenne"])
            Fonctions_pygame.mise_a_jour_affichage(fenetre, polices)
            Fonctions_pygame.fin_partie()
            break

        veut_rejouer = Fonctions.continuer_partie()
    Fonctions.affichage_fin_de_jeu(kopecs, nb_parties, fenetre, polices, scores, mises)  # affichage récapitulatif des parties


if __name__ == '__main__':
    main()
