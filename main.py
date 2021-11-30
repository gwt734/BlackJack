# Programme principal où est effectuée l'exécution
import Fonctions


def main():
    nb_joueurs = Fonctions.input_protege("Combien de joueurs jouerons ?  ", type_attendu=int, range_or_list="range", intervalle_reponses_possibles=(1, 15)) # Demande le nombre de joueurs
    joueurs = Fonctions.init_joueurs(nb_joueurs)    # Créé la liste des joueurs
    veut_rejouer = True
    kopecs = Fonctions.init_scores(joueurs, v=100)
    while veut_rejouer:
        joueurs_partie = []
        for j in joueurs:
            if kopecs[j] > 0:
                joueurs_partie.append(j)

        pioche = Fonctions.init_pioche(nb_joueurs)
        print(pioche[:7])  # pour le débogage
        encore = Fonctions.init_continuer_tour(joueurs_partie)
        scores, mises = Fonctions.premier_tour(joueurs_partie, pioche, kopecs)
        # print(pioche[:6])  # pour le débogage
        Fonctions.partie_complete(joueurs_partie, pioche, scores, encore, kopecs, mises)
        print(Fonctions.gagnant(scores),"a gagné la partie !")
        print("*\n**\n***\n****\n***\n**\n*")
        veut_rejouer = Fonctions.continuer_partie()

    # Fonction à tester


if __name__ == '__main__':
    main()
