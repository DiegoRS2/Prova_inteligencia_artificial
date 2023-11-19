from itertools import permutations


class Symbol():
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def __hash__(self):
        return hash(self.name)


class Symbol:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def evaluate(self, model):
        return model[self]

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def __hash__(self):
        return hash(self.name)


class And:
    def __init__(self, *conjuncts):
        self.conjuncts = list(conjuncts)

    def __repr__(self):
        conjunctions = ", ".join([str(conjunct) for conjunct in self.conjuncts])
        return f"And({conjunctions})"

    def evaluate(self, model):
        return all(conjunct.evaluate(model) if isinstance(conjunct, Symbol) else conjunct for conjunct in self.conjuncts)


class Not:
    def __init__(self, operand):
        self.operand = operand

    def __repr__(self):
        return f"Not({self.operand})"

    def evaluate(self, model):
        return not self.operand.evaluate(model) if isinstance(self.operand, Symbol) else self.operand


# Restante do código...


def generate_symbols(prefix, count):
    return [Symbol(f'{prefix}{i}') for i in range(1, count + 1)]


# Definição dos símbolos para cada propriedade
nacionalidade = generate_symbols('n', 5)
cor_casa = generate_symbols('c', 5)
bebida = generate_symbols('b', 5)
cigarro = generate_symbols('s', 5)
profissao = generate_symbols('p', 5)
terrorista = generate_symbols('t', 5)

# Definição das sentenças lógicas representando as informações adicionais
knowledge_base = And(
    nacionalidade[0], cor_casa[0],  # 1 - O britânico mora na casa vermelha
    nacionalidade[1], profissao[1],  # 2 - O suíço é mecânico
    nacionalidade[2], bebida[2],  # 3 - O dinamarquês bebe chá
    cor_casa[1], cor_casa[0],  # 4 - A casa verde fica imediatamente à esquerda da casa branca
    bebida[1], cor_casa[1],  # 5 - O dono da casa verde bebe café
    cigarro[1], profissao[2],  # 6 - O que fuma Pall Mall é professor
    cor_casa[2], cigarro[2],  # 7 - O dono da casa amarela fuma Dunhill
    cor_casa[2],  # 8 - O que mora na casa do meio bebe leite
    nacionalidade[3],  # 9 - O norueguês mora na primeira casa
    cigarro[3], profissao[3],  # 10 - O que fuma Blends mora ao lado do empresário
    profissao[4], cigarro[2],  # 11 - O programador mora ao lado do que fuma Dunhill
    cigarro[4], bebida[4],  # 12 - O que fuma Bluemasters bebe cerveja
    nacionalidade[4], cigarro[3],  # 13 - O alemão fuma Prince
    nacionalidade[3], cor_casa[3],  # 14 - O norueguês mora ao lado da casa azul
    cigarro[3], bebida[0]  # 15 - O que fuma Blends mora ao lado do que bebe água
)

# Definição da consulta para descobrir quem é o terrorista
query = And(
    terrorista[0], terrorista[1], terrorista[2], terrorista[3], terrorista[4],
    Not(knowledge_base)  # O terrorista é alguém que não satisfaz as condições conhecidas
)

# Função para verificar todas as combinações possíveis para descobrir o terrorista
def find_terrorist():
    symbols = nacionalidade + cor_casa + bebida + cigarro + profissao + terrorista
    permutations_list = permutations([True, False] * len(symbols), len(symbols))
    for perm in permutations_list:
        model = {symbol: value for symbol, value in zip(symbols, perm)}
        if query.evaluate(model):
            return model
    return None

# Encontrar o terrorista
terrorist_model = find_terrorist()

# Mostrar resultado
if terrorist_model:
    print("Terrorista encontrado:")
    for symbol, value in terrorist_model.items():
        if symbol in terrorista and value:
            print(f"{symbol} é o terrorista.")
else:
    print("Não foi possível determinar o terrorista com as informações fornecidas.")
