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
# Função para imprimir o caminho encontrado na matriz
def imprimir_caminho_encontrado(matriz, caminho):
    if caminho is None:
        print("Nenhum caminho encontrado.")
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
def gerar_labirinto(rows, cols):
    labirinto = [[random.randint(0, 1) for _ in range(cols)] for _ in range(rows)]
    return labirinto

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
labirinto = gerar_labirinto(10, 10)  # Tamanho da matriz (10x10) - pode ser ajustado

origem, destino = pontos_aleatorios(labirinto)

print("Matriz gerada:")
imprimir_matriz(labirinto)
print()

print(f"Origem: {origem}, Destino: {destino}")

# Avaliar tempo de execução do BFS - Busca em Largura
tempo_bfs = timeit.timeit(lambda: bfs_encontrar_caminho(labirinto, origem, destino), number=1)
print(f"Tempo de execução do BFS: {tempo_bfs:.6f} segundos")

# Avaliar tempo de execução do DFS - Busca em Profundidade
tempo_dfs = timeit.timeit(lambda: dfs_encontrar_caminho(labirinto, origem, destino), number=1)
print(f"Tempo de execução do DFS: {tempo_dfs:.6f} segundos")

# Encontrar o caminho usando BFS e imprimir na matriz
caminho_encontrado_bfs = bfs_encontrar_caminho(labirinto, origem, destino)
print("\nCaminho encontrado pelo BFS:")
imprimir_caminho_encontrado(labirinto, caminho_encontrado_bfs)

# Encontrar o caminho usando DFS e imprimir na matriz
caminho_encontrado_dfs = dfs_encontrar_caminho(labirinto, origem, destino)
print("\nCaminho encontrado pelo DFS:")
imprimir_caminho_encontrado(labirinto, caminho_encontrado_dfs)
