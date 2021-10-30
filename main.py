# Programme principal où est effectuée l'exécution
import Fonctions


def main():
    nb_joueurs = Fonctions.input_protege("Combien de joueurs jouerons?", type_attendu=int, range_or_list="range", intervalle_reponses_possibles=(1, 15)) # Demande le nombre de joueurs
    joueurs = Fonctions.init_joueurs(nb_joueurs)    # Créé la liste des joueurs
    veut_rejouer = True
    victoires = Fonctions.init_scores(joueurs)
    while veut_rejouer:
        joueurs_partie = list(joueurs)
        pioche = Fonctions.init_pioche(nb_joueurs)
        print(pioche)  # pour le débogage
        encore = Fonctions.init_continuer_tour(joueurs_partie)
        print(encore)  # pour le débogage
        scores = Fonctions.premier_tour(joueurs_partie, pioche)
        print(pioche)  # pour le débogage
        Fonctions.partie_complete(joueurs_partie, pioche, scores, victoires, encore)
        print(victoires)
        veut_rejouer = Fonctions.continuer_partie()
    # détermination du gagnant global
    nb_victoires=0
    for item in victoires.items():
        if item[1] > nb_victoires:
            vainqueur = item[0]
            nb_victoires = item[1]
    print("Le grand gagnant est", vainqueur, "avec", nb_victoires, "victoires !")

    # Fonction à tester


if __name__ == '__main__':
    main()
