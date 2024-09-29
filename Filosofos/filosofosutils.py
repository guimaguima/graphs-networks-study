import json
import gzip
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def json_to_csv(caminho_arquivos='../data/phi.json'):
    with open(caminho_arquivos, 'r') as file:
        data = json.load(file)

    filosofos = pd.DataFrame()

    filosofos['influenciado'] = "" 
    filosofos['influencia'] = "" 

    for filosofo in data['results']['bindings']:

        nova_linha = {'influenciado': filosofo['p']['value'].split('/')[4], 'influencia' : filosofo['influenced']['value'].split('/')[4]}

        filosofos = filosofos._append(nova_linha, ignore_index = True)
        
    filosofos.to_csv('../data/phi.csv',index=False)

    return filosofos


def get_grafo(csv='../data/phi.csv', nos_desejados=None, retritivo=False, parametro='influencia'):
    grafo_direcidonado = nx.DiGraph()
    
    filosofos = pd.read_csv(csv)
    
    filosofos = filosofos.set_index('influenciado')
    
    if nos_desejados is None:
        nos_desejados = filosofos.index
    
    for no in nos_desejados:
        if no in filosofos.index: 
            data = filosofos.loc[no]
            #percorre os nos selecionados e suas conexões, desejados ou todos
            by_set = set(data[parametro])
            #certifica conexões únicas
            for by in by_set:
                if retritivo and by not in nos_desejados:
                    continue
                grafo_direcidonado.add_edge(no, by)
                #adiciona os vertices

    return grafo_direcidonado

def gera_grafico(grafo,cor_principais='green',cor_secundarios='gray',tamanho_texto=10,largura=10,altura=10):#para testar se o grafo esta correto
    nos = np.array(grafo.nodes())
    #pega os nos

    nos_sorteados = np.random.choice(nos,50,replace=False)
    #escolhendo nos aleatorios


    grafo_amostra = get_grafo(nos_desejados=list(nos_sorteados))

    novo_nos = np.array(grafo_amostra.nodes())

    nos_nomes =  np.random.choice(novo_nos,10,replace=False)

    cor_nos = [cor_principais if no in nos_nomes  else cor_secundarios for no in novo_nos]
    #cria uma lista de cores para cada nó

    nomes_nos ={no: no if no in nos_nomes else '' for no in novo_nos}
    #cria um dicionario para cada nó sorteado em 10

    grau = nx.degree(grafo_amostra)

    ax = plt.subplots(figsize=(largura, altura))

    return nx.draw_networkx(
        grafo_amostra,
        pos=nx.kamada_kawai_layout(grafo_amostra),
        with_labels=True,
        node_size=[v * 100 for _, v in grau],#tamanho do nó de acordo com seu grau
        node_color=cor_nos,
        edge_color='lightgray',
        labels=nomes_nos,
        font_weight=tamanho_texto,
    )