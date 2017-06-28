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
    G = [None] * (n+1)
    pesos = {}
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

        vizinhos_origem = G[origem]
        if vizinhos_origem is None:  # lazy instantiation
            vizinhos_origem = set()
            G[origem] = vizinhos_origem
            
        vizinhos_origem.add(destino)
        pesos[(origem, destino)] = peso

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


def edmonds_karp(G, capacidades, produtor, consumidor):
    n = len(G) - 1
    f = 0
    fluxos = {aresta : 0 for aresta in capacidades}
    
##    rede_residual = [set(G[v]) if G[v] is not None else None
##                     for v in range(1, n+1)]
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

        # atualiza o fluxo, usando o caminho aumentante
        for indice in range(len(caminho_aumentante) - 1):
            # aresta x-->y
            x = caminho_aumentante[indice]
            y = caminho_aumentante[indice + 1]
            
            
        
        
            

        # atualiza a rede residual
        

    
    




    

    

                
        
        
    
    
                
    
    
    
