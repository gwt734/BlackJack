# Programme principal où est effectuée l'exécution
import Fonctions


def main():
    nb_joueurs = Fonctions.input_protege("Combien de joueurs jouerons?", type_attendu=int, range_or_list="range", intervalle_reponses_possibles=(1, 15)) # Demande le nombre de joueurs
    joueurs = Fonctions.init_joueurs(nb_joueurs)    # Créé la liste des joueurs
    veut_rejouer = True
    victoires = Fonctions.init_scores(joueurs)
    while veut_rejouer:
        joueurs_partie = joueurs
        pioche = Fonctions.init_pioche(nb_joueurs)
        print(pioche)
        scores = Fonctions.premier_tour(joueurs_partie, pioche)
        print(pioche)
        Fonctions.partie_complete(joueurs_partie, pioche, scores, victoires)
        print(victoires)
        veut_rejouer = Fonctions.continuer()

    # Fonction à tester


if __name__ == '__main__':
    main()
