from itertools import permutations

class Sentence():

    def evaluate(self, model):
        """Evaluates the logical sentence."""
        raise Exception("nothing to evaluate")

    def formula(self):
        """Returns string formula representing logical sentence."""
        return ""

    def symbols(self):
        """Returns a set of all symbols in the logical sentence."""
        return set()

    @classmethod
    def validate(cls, sentence):
        if not isinstance(sentence, Sentence):
            raise TypeError("must be a logical sentence")

    @classmethod
    def parenthesize(cls, s):
        """Parenthesizes an expression if not already parenthesized."""
        def balanced(s):
            """Checks if a string has balanced parentheses."""
            count = 0
            for c in s:
                if c == "(":
                    count += 1
                elif c == ")":
                    if count <= 0:
                        return False
                    count -= 1
            return count == 0
        if not len(s) or s.isalpha() or (
            s[0] == "(" and s[-1] == ")" and balanced(s[1:-1])
        ):
            return s
        else:
            return f"({s})"

class Symbol(Sentence):

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def __hash__(self):
        return hash(("symbol", self.name))

    def __repr__(self):
        return self.name

    def evaluate(self, model):
        try:
            return bool(model[self.name])
        except KeyError:
            print(f"variable {self.name} not in model")

    def formula(self):
        return self.name

    def symbols(self):
        return {self.name}


class And(Sentence):
    def __init__(self, *conjuncts: 'Sentence'):
        for conjunct in conjuncts:
            Sentence.validate(conjunct)
        self.conjuncts = list(conjuncts)

    def __repr__(self):
        conjunctions = ", ".join([str(conjunct) for conjunct in self.conjuncts])
        return f"And({conjunctions})"

    # def evaluate(self, model):
    #     return all(conjunct.evaluate(model) if isinstance(conjunct, Symbol) else conjunct for conjunct in self.conjuncts)
    
    def evaluate(self, model):
        return all(conjunct.evaluate(model) for conjunct in self.conjuncts)

    def formula(self):
        if len(self.conjuncts) == 1:
            return self.conjuncts[0].formula()
        return " ∧ ".join([Sentence.parenthesize(conjunct.formula())
                           for conjunct in self.conjuncts])

    def symbols(self):
        return set.union(*[conjunct.symbols() for conjunct in self.conjuncts])
    
    def add(self, conjunct):
        Sentence.validate(conjunct)
        self.conjuncts.append(conjunct)
    


class Or(Sentence):
    def __init__(self, *disjuncts: 'Sentence'):
        for disjunct in disjuncts:
            Sentence.validate(disjunct)
        self.disjuncts = list(disjuncts)

    def __eq__(self, other):
        return isinstance(other, Or) and self.disjuncts == other.disjuncts

    def __hash__(self):
        return hash(
            ("or", tuple(hash(disjunct) for disjunct in self.disjuncts))
        )

    def __repr__(self):
        disjuncts = ", ".join([str(disjunct) for disjunct in self.disjuncts])
        return f"Or({disjuncts})"

    def evaluate(self, model):
        return any(disjunct.evaluate(model) for disjunct in self.disjuncts)

    def formula(self):
        if len(self.disjuncts) == 1:
            return self.disjuncts[0].formula()
        return " ∨  ".join([Sentence.parenthesize(disjunct.formula())
                            for disjunct in self.disjuncts])

    def symbols(self):
        return set.union(*[disjunct.symbols() for disjunct in self.disjuncts])

class Not(Sentence):
    def __init__(self, operand: 'Sentence'):
        self.operand = operand

    def __repr__(self):
        return f"Not({self.operand})"

    def evaluate(self, model):
        return not self.operand.evaluate(model) if isinstance(self.operand, Symbol) else self.operand


# Restante do código...


def generate_symbols(prefix, count):
    return [Symbol(f'{prefix}{i}') for i in range(1, count + 1)]


# Definição dos símbolos para cada propriedade
pos_casas = generate_symbols('pc', 5)
nacionalidades = generate_symbols('n', 5)
cor_casas = generate_symbols('c', 5)
bebidas = generate_symbols('b', 5)
cigarros = generate_symbols('s', 5)
profissoes = generate_symbols('p', 5)

knowledge_base = And()

for nacionalidade in nacionalidades:
    for nacionalidade_temp in nacionalidades:
        if (nacionalidade != nacionalidade_temp):
            knowledge_base.add(And(nacionalidade, 
                                Or(pos_casas[0],
                                   pos_casas[1],
                                   pos_casas[2],
                                   pos_casas[3],
                                   pos_casas[4]),
                                Not(And(nacionalidade_temp))))

    for nacionalidade_temp in nacionalidades:
        if (nacionalidade != nacionalidade_temp):
            knowledge_base.add(And(nacionalidade, 
                                   
                                   Or(cor_casas[0],
                                      cor_casas[1],
                                      cor_casas[2],
                                      cor_casas[3],
                                      cor_casas[4]),
                                   Not(And(nacionalidade_temp))))

    for nacionalidade_temp in nacionalidades:
        if (nacionalidade != nacionalidade_temp):
            knowledge_base.add(And(nacionalidade, 
                                    Or(bebidas[0],
                                       bebidas[1],
                                       bebidas[2],
                                       bebidas[3],
                                       bebidas[4]),
                                    Not(And(nacionalidade_temp))))

    for nacionalidade_temp in nacionalidades:
        if (nacionalidade != nacionalidade_temp):
            knowledge_base.add(And(nacionalidade, 
                                Or(cigarros[0],
                                   cigarros[1],
                                   cigarros[2],
                                   cigarros[3],
                                   cigarros[4]),
                                Not(And(nacionalidade_temp))))

    for nacionalidade_temp in nacionalidades:
        if (nacionalidade != nacionalidade_temp):
            knowledge_base.add(And(nacionalidade, 
                                   Or(profissoes[0],
                                      profissoes[1],
                                      profissoes[2],
                                      profissoes[3],
                                      profissoes[4]),
                                   Not(And(nacionalidade_temp))))


def model_check(knowledge, query):
    """Checks if knowledge base entails query."""

    def check_all(knowledge, query, symbols, model):
        """Checks if knowledge base entails query, given a particular model."""

        # If model has an assignment for each symbol
        if not symbols:

            # If knowledge base is true in model, then query must also be true
            if knowledge.evaluate(model):
                return query.evaluate(model)
            return True
        else:

            # Choose one of the remaining unused symbols
            remaining = symbols.copy()
            p = remaining.pop()

            # Create a model where the symbol is true
            model_true = model.copy()
            model_true[p] = True

            # Create a model where the symbol is false
            model_false = model.copy()
            model_false[p] = False

            # Ensure entailment holds in both models
            return (check_all(knowledge, query, remaining, model_true) and
                    check_all(knowledge, query, remaining, model_false))

    # Get all symbols in both knowledge and query
    symbols = set.union(knowledge.symbols(), query.symbols())

    # Check that knowledge entails query
    return check_all(knowledge, query, symbols, dict())

# Definição das sentenças lógicas representando as informações adicionais
knowledge_base.conjuncts.append(And(
    And(nacionalidades[0],cor_casas[0]),
    And(nacionalidades[1],profissoes[1]),
    And(nacionalidades[2],bebidas[2]),
    Not(And(cor_casas[1], pos_casas[4])),
    And(cor_casas[1],bebidas[1]),
    And(cigarros[1],profissoes[2]),
    And(cor_casas[3],cigarros[2]),
    And(bebidas[0], pos_casas[2]),
    And(nacionalidades[3], pos_casas[0]),
    And(cigarros[4],bebidas[3]),
    And(nacionalidades[4],cigarros[3]),
))

# Definição da consulta para descobrir quem é o terrorista
# query = And(
#     #terrorista[0], terrorista[1], terrorista[2], terrorista[3], terrorista[4],
#     Not()  # O terrorista é alguém que não satisfaz as condições conhecidas
# )

# Função para verificar todas as combinações possíveis para descobrir o terrorista
def find_terrorist():
    symbols = nacionalidades + cor_casas + bebidas + cigarros + profissoes

    simbolos = []
    # permutations_list = permutations([True, False] * len(symbols), len(symbols))
    # for perm in permutations_list:
    #     model = {symbol: value for symbol, value in zip(symbols, perm)}
    #     if knowledge_base.evaluate(model):
    #         return model
    for symbol in symbols:
        if model_check(knowledge_base, symbol):
            simbolos.append(symbol)
    return simbolos



# Encontrar o terrorista
terrorist_model = find_terrorist()

# Mostrar resultado
if terrorist_model:
    print("Terrorista encontrado:")
    for symbol, value in terrorist_model.items():
        print(f"{symbol} é o terrorista.")
else:
    print("Não foi possível determinar o terrorista com as informações fornecidas.")
