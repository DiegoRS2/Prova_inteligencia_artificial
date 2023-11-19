import random
from collections import deque
import tkinter as tk
import copy
import threading

def gerar_cidade_conectada(linhas, colunas):
    cidade = [[1 for _ in range(colunas)] for _ in range(linhas)]

    # Inicializa as ruas nas posições ímpares
    for i in range(1, linhas, 2):
        for j in range(1, colunas, 2):
            cidade[i][j] = 0

    # Gera caminhos aleatórios para conectar as ruas
    for i in range(1, linhas, 2):
        for j in range(1, colunas, 2):
            direcoes = [(0, 2), (2, 0), (0, -2), (-2, 0)]
            random.shuffle(direcoes)

            for di, dj in direcoes:
                ni, nj = i + di, j + dj
                if 0 <= ni < linhas and 0 <= nj < colunas and cidade[ni][nj] == 0:
                    cidade[(i + ni) // 2][(j + nj) // 2] = 0
                    break

    return cidade

def exibir_cidade_grafica(cidade, nome):
    if (cidade is None):
        return

    root = tk.Tk()
    root.title(nome)

    canvas = tk.Canvas(root, width=len(cidade[0]) * 10, height=len(cidade) * 10)
    canvas.pack()

    for i in range(len(cidade)):
        for j in range(len(cidade[0])):
            cor = 'white' if cidade[i][j] == 0 else 'black' if cidade[i][j] == 1 else 'green' if cidade[i][j] == 'X' else 'red' 
            canvas.create_rectangle(j * 10, i * 10, (j + 1) * 10, (i + 1) * 10, fill=cor)

    root.mainloop()

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
                    print(f"Coordenada percorrida no DFS: {vizinho}")

    return None

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

def marcar_caminho_encontrado(matriz, caminho):
    if caminho is None:
        return
    
    matriz_temp = copy.deepcopy(matriz)

    caminho_set = set(caminho)
    for i in range(len(matriz_temp)):
        for j in range(len(matriz_temp[0])):
            if (i, j) in caminho_set:
                matriz_temp[i][j] = 'X'
    
    return matriz_temp

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


def coloca_impedimentos(matriz, quantidade_blocos):
    linhas = len(matriz)
    colunas = len(matriz[0])

    # Obtém as posições de todos os campos com valor 1
    posicoes_1 = [(i, j) for i in range(linhas) for j in range(colunas) if matriz[i][j] == 1]

    # Verifica se há posições suficientes para a quantidade desejada de blocos
    if quantidade_blocos > len(posicoes_1):
        raise ValueError("Não há posições suficientes para adicionar a quantidade desejada de blocos.")

    # Escolhe aleatoriamente posições para substituir por 2
    posicoes_2 = random.sample(posicoes_1, quantidade_blocos)

    # Substitui os valores nas posições escolhidas por 2
    for i, j in posicoes_2:
        matriz[i][j] = 2

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

tamanho_matriz = 50

labirinto = gerar_cidade_conectada(tamanho_matriz,tamanho_matriz)  # Tamanho da matriz (10x10) - pode ser ajustado
coloca_impedimentos(labirinto, 10)
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

caminho_city = marcar_caminho_encontrado(labirinto, caminho_encontrado_bfs)

thread1 = threading.Thread(target=exibir_cidade_grafica,args=(caminho_city,'BFS'))

# Encontrar o caminho usando DFS e imprimir na matriz
print("\nExecutando DFS...")
caminho_encontrado_dfs = dfs_encontrar_caminho(labirinto, origem, destino)
print("\nCaminho encontrado pelo DFS:")
imprimir_caminho_encontrado(labirinto, caminho_encontrado_dfs)

caminho_city = marcar_caminho_encontrado(labirinto, caminho_encontrado_dfs)

thread2 = threading.Thread(target=exibir_cidade_grafica,args=(caminho_city,'DFS'))

thread1.start()
thread2.start()
