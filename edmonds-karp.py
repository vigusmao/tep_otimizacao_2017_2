def inicializar_grafo(n):
    G = [None] * (n+1)
    pesos = {}
    return G, pesos

def adicionar_aresta(origem, destino, peso,
                     G, pesos):
    vizinhos_origem = G[origem]
    if vizinhos_origem is None:  # lazy instantiation
        vizinhos_origem = set()
        G[origem] = vizinhos_origem
        
    vizinhos_origem.add(destino)
    pesos[(origem, destino)] = peso


"""
    Cria um grafo a partir do input via teclado.

    Retorna uma tupla (G, pesos), onde:
    'G' eh um array, em enderecamento direto
        (vertice i armazenado na posicao i), em que cada posicao
        aponta para um hash set contendo seus vizinhos de saida
        (os vertices de G sao os inteiros 1, 2, ..., n);
    'pesos' eh um hash map {aresta -> peso}.
"""
def ler_grafo():
    n = int(input("Quantos vertices? "))
    if n < 0:
        return None
    G, pesos = inicializar_grafo(n)
    print("Digite as arestas." + \
          "\nFormato 'origem, destino, peso' (sem plics)." + \
          "\n[-1 para terminar]")
    
    while True:
        aresta = eval(input("Aresta: "))
        if aresta == -1:
            break
        origem = aresta[0]
        destino = aresta[1]
        peso = aresta[2]
        adicionar_aresta(origem, destino, peso, G, pesos)
        
    return G, pesos
        

"""
   G: grafo representado por um array, em enderecamento direto
      (vertice i armazenado na posicao i), em que cada posicao
      aponta para um hash set contendo seus vizinhos de saida.
      Obs: os vertices de G sao os inteiros 1, 2, ..., n

   origem: um vertice que serah a raiz da busca
   destino: o vertice que se deseja encontrar (a busca serah
            interrompida quando/se o encontrarmos)

   Retorna um caminho minimo entre origem e destino, se existir;
           None, caso nao exista
"""
def busca_largura(G, origem, destino):
    n = len(G) - 1
    pais = [None] * (n+1)
    pais[origem] = origem
    
    fila = [origem]
    fila_head = 0

    while fila_head < len(fila):  # enquanto fila nao vazia
        v = fila[fila_head]
        fila_head += 1
        if G[v] is None:
            continue  # v nao tem vizinhos de saida
        for vizinho_de_saida in G[v]:
            if pais[vizinho_de_saida] is None:
                fila.append(vizinho_de_saida)  # enfileira o vizinho
                pais[vizinho_de_saida] = v
                if vizinho_de_saida == destino:
                    # Achei!!!!
                    fila_head = len(fila)  # para tambem interromper o while
                    break  # interrompendo o for

    if pais[destino] is None:
        return None

    caminho = [destino]
    v = destino
    while v != origem:
        v = pais[v]
        caminho.append(v)

    return caminho[-1::-1]


def busca_profundidade(G, raiz, buscado):

    def busca(G, raiz, buscado, caminho, pais):
        if raiz == buscado:
            return True
        vizinhos = G[raiz]
        if vizinhos is not None:
            for vizinho in vizinhos:
                if pais[vizinho] is None:
                    pais[vizinho] = raiz
                    caminho.append(vizinho)
                    resultado = busca(G, vizinho, buscado,
                                      caminho, pais)
                    if resultado is True:
                        return True
                    caminho.pop()

        return False


    n = len(G) - 1
    pais = [None] * (n+1)
    pais[raiz] = raiz
    
    return busca(G, raiz, buscado, [raiz], pais)
    

def aumentar_fluxo(origem, destino, delta, fluxos):
    fluxo_contrario = fluxos.get((destino, origem), 0)

    if fluxo_contrario > 0:
        diminuicao = min(fluxo_contrario, delta)
        fluxos[(destino, origem)] -= diminuicao
        delta -= diminuicao

    fluxos[(origem, destino)] += delta


def criar_rede_residual_inicial(G, capacidades):
##    rede_residual = [set(G[v]) if G[v] is not None else None
##                     for v in range(1, n+1)]
    n = len(G) - 1
    rede_residual = [None] * (n+1)
    for v in range(1, n+1):
        vizinhos_v = G[v]
        if vizinhos_v is not None:
            vizinhos_na_rede = set()
            rede_residual[v] = vizinhos_na_rede
            for w in vizinhos_v:
                vizinhos_na_rede.add(w)
            
    capacidades_rede = {aresta : capacidades[aresta] \
                        for aresta in capacidades}

    return rede_residual, capacidades_rede


def atualizar_rede_residual(origem, destino, rede_residual,
                            capacidades_rede, capacidades_grafo,
                            fluxos):
    def atualizar_aresta(x, y):
        nova_capacidade_xy = \
            capacidades_grafo.get((x,y), 0) - fluxos.get((x,y), 0) \
                                            + fluxos.get((y,x), 0)
        vizinhos_x = rede_residual[x]
        if nova_capacidade_xy == 0:
            capacidades_rede.pop((x,y), None)
            if vizinhos_x is not None:
                rede_residual[x].remove(y)
        else:
            capacidades_rede[(x,y)] = nova_capacidade_xy
            if vizinhos_x is None:
                vizinhos_x = set()
                rede_residual[x] = vizinhos_x
            rede_residual[x].add(y)

    atualizar_aresta(origem, destino) 
    atualizar_aresta(destino, origem)


def edmonds_karp(G, capacidades, produtor, consumidor):
    f = 0
    fluxos = {aresta : 0 for aresta in capacidades}
    
    rede_residual, capacidades_rede = criar_rede_residual_inicial(
        G, capacidades)

    while True:

        caminho_aumentante = busca_largura(
            rede_residual, produtor, consumidor)

        # se nao existir, interrompe
        if caminho_aumentante is None:
            break

        # encontra o gargalo do caminho aumentante
        delta = -1  # capacidade do gargalo
        for indice in range(len(caminho_aumentante) - 1):
            # aresta x-->y
            x = caminho_aumentante[indice]
            y = caminho_aumentante[indice + 1]
            capacidade_xy = capacidades_rede[(x,y)]
            if delta == -1 or \
               capacidade_xy < delta:
                delta = capacidade_xy

        # atualiza o fluxo e a rede, usando o caminho aumentante
        f += delta
        for indice in range(len(caminho_aumentante) - 1):
            # aresta x-->y
            x = caminho_aumentante[indice]
            y = caminho_aumentante[indice + 1]
            aumentar_fluxo(x, y, delta, fluxos)

            atualizar_rede_residual(
                x, y, rede_residual, capacidades_rede,
                capacidades, fluxos)

    return f, fluxos
            

def ford_fulkerson(G, capacidades, produtor, consumidor):
    f = 0
    fluxos = {aresta : 0 for aresta in capacidades}
    
    rede_residual, capacidades_rede = criar_rede_residual_inicial(
        G, capacidades)

    while True:

        caminho_aumentante = busca_profundidade(
            rede_residual, produtor, consumidor)

        # se nao existir, interrompe
        if caminho_aumentante is None:
            break

        # encontra o gargalo do caminho aumentante
        delta = -1  # capacidade do gargalo
        for indice in range(len(caminho_aumentante) - 1):
            # aresta x-->y
            x = caminho_aumentante[indice]
            y = caminho_aumentante[indice + 1]
            capacidade_xy = capacidades_rede[(x,y)]
            if delta == -1 or \
               capacidade_xy < delta:
                delta = capacidade_xy

        # atualiza o fluxo e a rede, usando o caminho aumentante
        f += delta
        for indice in range(len(caminho_aumentante) - 1):
            # aresta x-->y
            x = caminho_aumentante[indice]
            y = caminho_aumentante[indice + 1]
            aumentar_fluxo(x, y, delta, fluxos)

            atualizar_rede_residual(
                x, y, rede_residual, capacidades_rede,
                capacidades, fluxos)

    return f, fluxos


def teste():
    G, capacidades = inicializar_grafo(4)
    adicionar_aresta(1, 2, 1000, G, capacidades)
    adicionar_aresta(2, 4, 1000, G, capacidades)
    adicionar_aresta(1, 3, 1000, G, capacidades)
    adicionar_aresta(3, 4, 1000, G, capacidades)
    adicionar_aresta(2, 3, 1, G, capacidades)

    rede, cap_rede = criar_rede_residual_inicial(G, capacidades)
    fluxos = {aresta : 0 for aresta in capacidades}

    # adicionando fluxo em 1-->2-->4
    fluxos[(1, 2)] = 5
    fluxos[(2, 4)] = 5

    atualizar_rede_residual(1, 2, rede, cap_rede, capacidades, fluxos)
    atualizar_rede_residual(2, 4, rede, cap_rede, capacidades, fluxos)

            

# Main
G, capacidades = inicializar_grafo(4)
adicionar_aresta(1, 2, 10**1, G, capacidades)
adicionar_aresta(2, 4, 10**1, G, capacidades)
adicionar_aresta(1, 3, 10**1, G, capacidades)
adicionar_aresta(3, 4, 10**1, G, capacidades)
adicionar_aresta(2, 3, 1, G, capacidades)

fluxo_maximo, fluxos = ford_fulkerson(G, capacidades, 1, 4)

print("fluxo maximo = %d" % fluxo_maximo)
for aresta, fluxo in fluxos.items():
    print("fluxo(%d,%d) = %d" % (aresta[0], aresta[1], fluxo))

        

    
    




    

    

                
        
        
    
    
                
    
    
    
