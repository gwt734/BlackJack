# Fichier où stocker toute les fonctions nécessaires au jeu

# A1 - Paquet de cartes
def paquet():
    pass
    # Fonction à completer


def valeur_carte(carte):
    pass
    # Fonction à completer


def init_pioche(n):
    pass
    # Fonction à completer


def pioche_carte():
    pass
    # Fonction à completer


# A2 - Joueurs et scores
def init_joueurs(n):
    pass
    # Fonction à completer


def init_scores(joueurs, v):
    pass
    # Fonction à completer


def premier_tour(joueurs):
    pass
    # Fonction à completer


def gagnant(scores):
    pass
    # Fonction à completer


# B1 - Tour d'un joueur
def continuer():
    pass
    # Fonction à completer


def tour_joueur(j):
    pass
    # Fonction à completer


# B2 - Une partie complète
def tour_complet():
    pass
    # Fonction à completer


def partie_finie():
    pass
    # Fonction à completer


def partie_complete():
    pass
    # Fonction à completer


# E - Diverses fonctions supplémentaires
def protected_input(question, input_type, range_or_list, range_to_fit_in, list_to_fit_in):
    """
    question=question to ask the user
    input_type=type of the input needed (example: int, float, str)
    range_or_list= wether the input needs to be part of a range or a list, "range", "list" or "none" (actually anything other than "range" or "list" will result in no value check
    range= range the input needs to be part of (example: (4, 8) here 8 is not included while 4 is) leave as empty if not applicable
    list= list the input needs to be part of (example: [4, 8] or list1 ) leave as empty if not applicable
    """
    raw_input = input(question)
    type_was_checked = False
    value_was_checked = False

    while not(type_was_checked and value_was_checked):
        try:
            partially_processed_input = input_type(raw_input)

        except:
            print("Your input was not a ", input_type.__name__, ". Please enter a ", input_type.__name__)
            raw_input = input()

        else:
            type_was_checked = True
            if range_or_list == "range":
                if partially_processed_input in range(range_to_fit_in[0], range_to_fit_in[1]):
                    value_was_checked = True
                else:
                    print("Your input was not in range ", range_to_fit_in, ". Please enter a number in range ", range_to_fit_in)
                    print(value_was_checked)
                    raw_input = input()
            elif range_or_list == "list":
                if partially_processed_input in list_to_fit_in:
                    value_was_checked = True
                else:
                    print("Your input was not in list ", list_to_fit_in, ". Please enter a number in list ", list_to_fit_in)
                    raw_input = input()
            else:
                value_was_checked = True
            print(value_was_checked)
    return partially_processed_input
