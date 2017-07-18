VALOR = 0
PESO = 1


def extrai_bit(numero, bit_idx):
    mascara = 1 << bit_idx
    return 1 if numero & mascara > 0 else 0


'''
   parametros:
      itens: uma lista de tuplas (v_i, w_i) com valor e peso de cada item
          W: o peso maximo suportado pela mochila

   saida: uma lista contendo os indices dos items de uma solucao otima e
          o valor obtido   
'''
def mochila_enumeracao(itens, W):
    n = len(itens)
    quant_mochilas = 2**n
    valor_otimo = 0
    mochila_idx_otimo = 0
    
    for mochila_idx in range(quant_mochilas):
        peso = 0
        valor = 0
        for item_idx in range(n):
            item = itens[item_idx]
            # o item estah na mochila?
            if extrai_bit(mochila_idx, item_idx) == 1:
                valor += item[VALOR]
                peso += item[PESO]
        # solucao viavel?
        if peso <= W:
            if valor > valor_otimo:
                valor_otimo = valor
                mochila_idx_otimo = mochila_idx
                
    mochila_otima = []
    for item_idx in range(n):
        # o item estah na mochila?
        if extrai_bit(mochila_idx_otimo, item_idx) == 1:
            mochila_otima.append(item_idx)
    return mochila_otima, valor_otimo
            

'''
   parametros:
      itens: uma lista de tuplas (v_i, w_i) com valor e peso de cada item
          W: o peso maximo suportado pela mochila

   saida: uma lista contendo os indices dos items de uma solucao otima e
          o valor obtido   
'''
def mochila_backtracking(itens, W):
    def copia_mochila(destino, origem):
        destino[:] = []  # clear
        for elemento in origem:
            destino.append(elemento)
        
    mochila_otima = []
    global valor_otimo
    valor_otimo = 0

    def backtrack(mochila_corrente, peso_corrente, valor_corrente):
        # otimizou?
        if valor_corrente > valor_otimo:
            copia_mochila(mochila_otima, mochila_corrente)
            global valor_otimo
            valor_otimo = valor_corrente

        proximo_candidato = 0
        if len(mochila_corrente) > 0:
            proximo_candidato = mochila_corrente[-1] + 1
            
        for candidato_idx in range(proximo_candidato, len(itens)):
            candidato = itens[candidato_idx]
            if candidato[PESO] + peso_corrente <= W:  # cabe na mochila
                mochila_corrente.append(candidato_idx)
                peso_corrente += candidato[PESO]
                valor_corrente += candidato[VALOR]

                backtrack(mochila_corrente, peso_corrente, valor_corrente)

                mochila_corrente.pop()
                peso_corrente -= candidato[PESO]
                valor_corrente -= candidato[VALOR]

    
    #--------------

    mochila_otima = []
    estado_corrente = []
    backtrack(estado_corrente, 0, 0)
    return mochila_otima, valor_otimo


    





### Main

itens = []
itens.append((100, 10))
itens.append((500, 3))
itens.append((8, 1))
itens.append((25, 6))
capacidade = 18

mochila, valor = mochila_enumeracao(itens, capacidade)
print("enumeracao")
print("mochila -->", mochila)
print("valor -->", valor)

mochila, valor = mochila_backtracking(itens, capacidade)
print("backtracking")
print("mochila -->", mochila)
print("valor -->", valor)


            
            
                
    
