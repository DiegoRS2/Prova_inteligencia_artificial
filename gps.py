import random
import timeit
from collections import deque

# Implementação do algoritmo BFS para encontrar o caminho entre dois pontos na matriz
def bfs_encontrar_caminho(matriz, origem, destino):
    linhas = len(matriz)
    colunas = len(matriz[0])
    visitados = set()
    fila = deque([[origem]])

    while fila:
        caminho = fila.popleft()
        atual = caminho[-1]

        if atual == destino:
            return caminho

        if atual not in visitados:
            visitados.add(atual)
            vizinhos = []
            for direcao in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                novo_x = atual[0] + direcao[0]
                novo_y = atual[1] + direcao[1]
                if 0 <= novo_x < linhas and 0 <= novo_y < colunas and matriz[novo_x][novo_y] == 1:
                    vizinhos.append((novo_x, novo_y))

            for vizinho in vizinhos:
                novo_caminho = list(caminho)
                novo_caminho.append(vizinho)
                fila.append(novo_caminho)
                # Impressão das coordenadas percorridas
                print(f"Coordenada percorrida no BFS: {vizinho}")

    return None

# Implementação do algoritmo DFS para encontrar o caminho entre dois pontos na matriz
def dfs_encontrar_caminho(matriz, origem, destino):
    linhas = len(matriz)
    colunas = len(matriz[0])
    visitados = set()
    pilha = deque([origem])
    caminho = {origem: None}

    while pilha:
        atual = pilha.pop()

        if atual == destino:
            caminho_encontrado = reconstruir_caminho(caminho, origem, destino)
            return caminho_encontrado

        if atual not in visitados:
            visitados.add(atual)
            vizinhos = []
            for direcao in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                novo_x = atual[0] + direcao[0]
                novo_y = atual[1] + direcao[1]
                if 0 <= novo_x < linhas and 0 <= novo_y < colunas and matriz[novo_x][novo_y] == 1:
                    vizinhos.append((novo_x, novo_y))

            for vizinho in vizinhos:
                if vizinho not in visitados:
                    pilha.append(vizinho)
                    caminho[vizinho] = atual
                    # Impressão das coordenadas percorridas
                    print(f"Coordenada percorrida no DFS: {vizinho}")

    return None

# Implementação da função auxiliar para reconstruir o caminho
def reconstruir_caminho(caminho, origem, destino):
    caminho_encontrado = []
    atual = destino
    while atual != origem:
        caminho_encontrado.append(atual)
        atual = caminho[atual]
    caminho_encontrado.append(origem)
    return list(reversed(caminho_encontrado))

# Função para imprimir a matriz na tela
def imprimir_matriz(matriz):
    for linha in matriz:
        print(" ".join(str(elem) for elem in linha))

# Função para imprimir o caminho encontrado na matriz
def imprimir_caminho_encontrado(matriz, caminho):
    if caminho is None:
        return
    
    caminho_set = set(caminho)
    for i, linha in enumerate(matriz):
        for j, elem in enumerate(linha):
            if (i, j) in caminho_set:
                print("X", end=" ")  # Marca o caminho com X
            else:
                print(elem, end=" ")
        print()

# Gerar uma matriz de exemplo (labirinto)
def gerar_cidade(linhas, colunas):
    cidade = [[0 for _ in range(colunas)] for _ in range(linhas)]

    # Adiciona ruas horizontais
    for i in range(1, linhas, 2):
        cidade[i] = [1] * colunas

    # Adiciona ruas verticais
    for j in range(1, colunas, 2):
        for i in range(linhas):
            cidade[i][j] = 1

    # Adiciona interseções aleatórias
    for i in range(1, linhas, 2):
        for j in range(1, colunas, 2):
            cidade[i][j] = 1

    return cidade

# Exemplo de uso
linhas = 100
colunas = 100
cidade = gerar_cidade(linhas, colunas)


def coloca_impedimentos(labirinto):
   labirinto[3][5] = 2
   labirinto[3][1] = 2
   labirinto[3][2] = 2
   labirinto[3][3] = 2
   labirinto[3][0] = 2
   labirinto[3][4] = 2
   labirinto[3][6] = 2
   labirinto[3][7] = 2
   labirinto[3][8] = 2

# Definir pontos de origem e destino aleatórios na matriz
def pontos_aleatorios(matriz):
    linhas = len(matriz)
    colunas = len(matriz[0])
    origem = (random.randint(0, linhas - 1), random.randint(0, colunas - 1))
    destino = (random.randint(0, linhas - 1), random.randint(0, colunas - 1))
    while matriz[origem[0]][origem[1]] == 0 or matriz[destino[0]][destino[1]] == 0 or origem == destino:
        origem = (random.randint(0, linhas - 1), random.randint(0, colunas - 1))
        destino = (random.randint(0, linhas - 1), random.randint(0, colunas - 1))
    return origem, destino

# Testar e comparar os algoritmos com a matriz gerada
labirinto = gerar_cidade(50,50)  # Tamanho da matriz (10x10) - pode ser ajustado
coloca_impedimentos(labirinto)
origem, destino = pontos_aleatorios(labirinto)

print("Matriz gerada:")
imprimir_matriz(labirinto)
print()

print(f"Origem: {origem}, Destino: {destino}")

# Encontrar o caminho usando BFS e imprimir na mclearatriz
print("\nExecutando BFS...")
caminho_encontrado_bfs = bfs_encontrar_caminho(labirinto, origem, destino)
print("\nCaminho encontrado pelo BFS:")
imprimir_caminho_encontrado(labirinto, caminho_encontrado_bfs)

# Encontrar o caminho usando DFS e imprimir na matriz
print("\nExecutando DFS...")
caminho_encontrado_dfs = dfs_encontrar_caminho(labirinto, origem, destino)
print("\nCaminho encontrado pelo DFS:")
imprimir_caminho_encontrado(labirinto, caminho_encontrado_dfs)
