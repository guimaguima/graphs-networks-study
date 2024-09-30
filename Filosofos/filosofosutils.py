import json
import gzip
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_pandas_csv():
    caminho_arquivos='../data/phi_p_i_ids.json'
    
    with open(caminho_arquivos, 'r', encoding='utf-8') as file:
        data = json.load(file)

    pandas = pd.DataFrame(columns=['id','filosofo'])
    
    array_id = []

    for phi in data['results']['bindings']:
        
        if phi['p']['id'] not in array_id:
            nova_linha = {'id': phi['p']['id'] , 'filosofo' : phi['p']['value']}
            array_id.append(phi['p']['id'])
            pandas = pandas._append(nova_linha, ignore_index = True)
        
        if phi['influenced']['id'] not in array_id:
            nova_linha = {'id': phi['influenced']['id'] , 'filosofo' : phi['influenced']['value']}
            array_id.append(phi['influenced']['id'])
            pandas = pandas._append(nova_linha, ignore_index = True)

    pandas = pandas.sort_values('id').set_index('id')
    pandas.to_csv('../data/phi.csv',index=False)

    return pandas


def get_grafo(nos_desejados=[], restritivo=False, parametro='influencia'):
    
    caminho_arquivos='../data/phi_p_i_ids.json'
    
    with open(caminho_arquivos, 'r', encoding='utf-8') as file:
        data = json.load(file)

    grafo_direcidonado = nx.DiGraph()

    for phi in data['results']['bindings']:
        if len(nos_desejados)==0 : 
            grafo_direcidonado.add_edge(phi['p']['id'],phi['influenced']['id'])
        elif restritivo and phi['influenced']['id'] not in nos_desejados:
            continue
        elif phi['p']['id'] in nos_desejados:
            grafo_direcidonado.add_edge(phi['p']['id'],phi['influenced']['id']) 

    return grafo_direcidonado

def gera_grafico(grafo,df,cor_principais='green',cor_secundarios='gray',tamanho_texto=10,largura=10,altura=10):#para testar se o grafo esta correto
    nos = np.array(grafo.nodes())
    #pega os nos

    nos_sorteados = np.random.choice(nos,50,replace=False)
    #escolhendo nos aleatorios


    grafo_amostra = get_grafo(nos_desejados=list(nos_sorteados))

    novo_nos = np.array(grafo_amostra.nodes())

    nos_nomes =  np.random.choice(novo_nos,10,replace=False)
    
    nomes_nos ={no: df.loc[no].get('filosofo') if no in nos_nomes else '' for no in novo_nos}
    #cria um dicionario para cada nó sorteado em 10

    cor_nos = [cor_principais if no in nos_nomes  else cor_secundarios for no in novo_nos]
    #cria uma lista de cores para cada nó

    grau = nx.degree(grafo_amostra)

    ax = plt.subplots(figsize=(largura, altura))

    return nx.draw_networkx(
        grafo_amostra,
        pos=nx.kamada_kawai_layout(grafo_amostra),
        with_labels=True,
        node_size=[v * 100 for _, v in grau],#tamanho do nó de acordo com seu grau
        node_color=cor_nos,
        edge_color='lightgray',
        labels= nomes_nos,
        font_weight=tamanho_texto,
    )