import json
import gzip
import networkx as nx
import pandas as pd

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


def get_grafo(json_data, nos_desejados=None, retritivo=False, parametro='influencer'):
    grafo_direcidonado = nx.DiGraph()
    #cria um grafo direcionado
    
    if nos_desejados is None:
        #caso não possua nos desejados, utiliza de todas as conexões
        nos_desejados = set(json_data.keys())
    
    for no in nos_desejados:
        data = json_data[no]
        #percorre os nos selecionados e suas conexões, desejados ou todos
        by_set = set(map(extract_id, data[parametro]))
        #certifica conexões únicas
        for by in by_set:
            if retritivo and by not in nos_desejados:
                continue
            grafo_direcidonado.add_edge(no, by)
            #adiciona os vertices

    return grafo_direcidonado

def gera_grafico(grafo,df,numero_disrupcao=0,cor_principais='green',cor_secundarios='gray',tamanho_texto=10,largura=10,altura=10):
    nos = grafo.nodes()
    grau = nx.degree(grafo)
    #pega os nos e os graus

    
    condicao_disrupcao = df[df.get('disruption') >= numero_disrupcao] if numero_disrupcao >= 0 else df[df.get('disruption') <= numero_disrupcao]
    #cria df filtrado por mais ou menos disrupção

    cor_nos = [cor_principais if no in condicao_disrupcao.index else cor_secundarios for no in nos]
    #cria uma lista de cores para cada nó

    nomes_nos = {no: df.loc[no].get('name') if no in condicao_disrupcao.index else '' for no in nos}
    #cria um dicionario para cada nó


    ax = plt.subplots(figsize=(largura, altura))

    return nx.draw_networkx(
        grafo,
        pos=nx.kamada_kawai_layout(grafo),
        with_labels=True,
        node_size=[v * 100 for _, v in grau],#tamanho do nó de acordo com seu grau
        node_color=cor_nos,
        edge_color='lightgray',
        labels=nomes_nos,
        font_weight=tamanho_texto,
    )