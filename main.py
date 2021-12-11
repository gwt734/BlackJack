# Programme principal où est effectuée l'exécution
import Fonctions
import Constantes


def main():
    nb_joueurs = Fonctions.input_protege("Combien de joueurs jouerons ? ", type_attendu=int, range_or_list="range", intervalle_reponses_possibles=(1, 15)) # Demande le nombre de joueurs
    print()
    joueurs = Fonctions.init_joueurs(nb_joueurs)    # Créé la liste des joueurs
    veut_rejouer = True
    kopecs = Fonctions.init_scores(joueurs, v=100)
    nb_parties = 0
    while veut_rejouer:
        nb_parties += 1
        joueurs_partie = []
        for j in joueurs:  # avant chaque partie on vérifie qu'il reste de l'argent à tous les joueurs
            if kopecs[j] > 0:
                joueurs_partie.append(j)  # si c'est le cas, on les ajoute à la partie

        pioche = Fonctions.init_pioche(nb_joueurs)
        # print(pioche[:7])  # pour le débogage
        encore = Fonctions.init_continuer_tour(joueurs_partie)
        print(Constantes.AFFICHAGE)
        scores, mises = Fonctions.premier_tour(joueurs_partie, pioche, kopecs)
        # print(pioche[:6])  # pour le débogage
        Fonctions.partie_complete(joueurs_partie, pioche, scores, encore, kopecs, mises)
        # print(Fonctions.gagnant(scores),"a gagné la partie !")
        print(Constantes.AFFICHAGE)
        for joueur in kopecs:
            print("Il reste", kopecs[joueur], "kopecs à", joueur)
        print(Constantes.AFFICHAGE)
        veut_rejouer = Fonctions.continuer_partie()
    Fonctions.fin_de_jeu(kopecs, nb_parties)


if __name__ == '__main__':
    main()
