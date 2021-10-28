# Programme principal où est effectuée l'exécution
import Fonctions


def main():
    nb_joueurs = Fonctions.input_protege("Combien de joueurs jouerons?", int, "range", (1, 15))
    joueurs = Fonctions.init_joueurs(nb_joueurs)
    veut_continuer = True
    victoires = Fonctions.init_scores(joueurs)
    while veut_continuer:
        pioche = Fonctions.init_pioche(nb_joueurs)
        print(pioche)
        scores = Fonctions.premier_tour(joueurs, pioche)
        print(pioche)
        Fonctions.partie_complete(joueurs, pioche, scores, victoires)
        print(victoires)
        veut_continuer = Fonctions.continuer()

    # Fonction à tester


if __name__ == '__main__':
    main()
