from itertools import permutations

def check_conditions(houses):
    for i in range(5):
        if houses[i]['nationality'] == 'norueguês' and i != 0:
            if houses[i - 1]['color'] != 'azul' and houses[i + 1]['color'] != 'azul':
                return False

        if houses[i]['color'] == 'verde':
            if i == 0 or i == 4:
                return False
            if houses[i - 1]['color'] != 'branca' or houses[i + 1]['color'] != 'branca':
                return False

        if houses[i]['nationality'] == 'britânico' and houses[i]['color'] != 'vermelha':
            return False

        if houses[i]['nationality'] == 'suíço' and houses[i]['profession'] != 'mecânico':
            return False

        if houses[i]['nationality'] == 'dinamarquês' and houses[i]['drink'] != 'chá':
            return False

        if houses[i]['color'] == 'amarela' and houses[i]['cigar'] != 'Dunhill':
            return False

        if houses[i]['profession'] == 'professor' and houses[i]['cigar'] != 'Pall Mall':
            return False

        if houses[i]['cigar'] == 'Blends':
            if (i > 0 and houses[i - 1]['profession'] != 'empresário') and (i < 4 and houses[i + 1]['profession'] != 'empresário'):
                return False

        if houses[i]['cigar'] == 'Blends':
            if (i > 0 and houses[i - 1]['drink'] != 'água') and (i < 4 and houses[i + 1]['drink'] != 'água'):
                return False

        if houses[i]['drink'] == 'leite' and i != 2:
            return False

        if houses[i]['cigar'] == 'Bluemasters' and houses[i]['drink'] != 'cerveja':
            return False

        if houses[i]['nationality'] == 'alemão' and houses[i]['cigar'] != 'Prince':
            return False

    return True

def solve_puzzle():
    colors = ['vermelha', 'verde', 'branca', 'amarela', 'azul']
    nationalities = ['britânico', 'suíço', 'dinamarquês', 'norueguês', 'alemão']
    drinks = ['chá', 'café', 'leite', 'cerveja', 'água']
    cigars = ['Pall Mall', 'Dunhill', 'Blends', 'Bluemasters', 'Prince']
    professions = ['professor', 'empresário', 'mecânico', 'programador', 'terrorista']

    all_permutations = permutations([
        {'color': color, 'nationality': nationality, 'drink': drink, 'cigar': cigar, 'profession': profession}
        for color in colors
        for nationality in nationalities
        for drink in drinks
        for cigar in cigars
        for profession in professions
    ])

    for houses in all_permutations:
        if check_conditions(houses):
            for i in range(5):
                if houses[i]['profession'] == 'terrorista':
                    return houses[i]['nationality']

# Resolvendo o quebra-cabeça e encontrando o terrorista
terrorist = solve_puzzle()
print(f"O terrorista é o {terrorist}.")
