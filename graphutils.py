import json
import gzip
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

def extract_id(txt):
    #organiza a nomeclatura
    pos = txt.rfind('mn')
    return txt[pos:pos+12]

def get_data_gz(arquivo_nome):
    #pega o gz definido
    caminho_arquivo = './data/'+arquivo_nome+'.gz'
    with gzip.open(caminho_arquivo) as arquivo:
        json_data = json.load(arquivo) 
        return json_data

def get_df(arquivo_nome,arquivo_ext):
    #pega um dataframe qualquer de um arquivo qualquer
    caminho_arquivo = './data/'+arquivo_nome+'.'+arquivo_ext

    if arquivo_ext.find('json') > 0:
        df = pd.read_json(caminho_arquivo)


    elif arquivo_ext.find('gz') > 0:
        with gzip.open(caminho_arquivo) as arquivo:
            json_data = json.load(arquivo)
            df = pd.read_json(json_data)
    
    else: 
        df = pd.read_csv(caminho_arquivo)

    return df

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

def get_grafo_parametros(json_data,df,parametro_primeiro,primeiro_valor,parametro_epoca=False,valor_chao=None,valor_teto=None):
    #pega os nos do grafo conforme parametros da tabela de disrupção
    if parametro_epoca:
        #pensando nas épocas e suas influências, pensa de onde começa e onde acaba
        series_nos = df[(df.get(parametro_primeiro) == primeiro_valor) & ((df.get(parametro_epoca)>=valor_chao) & (df.get(parametro_epoca)<=valor_teto))].index
        #nos
        grafo = get_grafo(json_data,series_nos)
        #grafo
    else: 
        series_nos = df[df.get(parametro_primeiro) == primeiro_valor].index
        grafo = get_grafo(json_data,series_nos)
    return grafo


def get_artistas_df():
    #pega a tabela de disruptividade
    disruptive = get_df('disrupt','csv')
    disruptive = disruptive[(disruptive.get('ni')>0) & (disruptive.get('nj')>0) & (disruptive.get('nk')>0)].set_index('label').sort_values(by='disruption',ascending=False)
    #pega a tabela de artistas com genêro e  decadas
    artistas = get_df('artist-network-degrees','csv')
    artistas = artistas.set_index('label').dropna()
    #tabela cruzada dos dois
    disruption_genero = artistas.get(['name','earliest_decade','genre']).join(disruptive.get(['ni','nj','nk','disruption','confidence'])).dropna()
    return disruption_genero

def gera_grafico(grafo,df,numero_disrupcao,cor_principais,cor_secundarios,tamanho_texto,largura,altura):
    nos = grafo.nodes()
    grau = nx.degree(grafo)
    #pega os nos e os graus

    cor_nos = [cor_principais if (no in df.index) and (df.loc[no].get('disruption') > numero_disrupcao)
                else cor_secundarios for no in nos]
    #cria uma lista dde cores para cada nó

    nomes_nos = {no: df.loc[no].get('name')
                if (no in df.index)  and (df.loc[no].get('disruption') > numero_disrupcao)
                else '' for no in nos}
    #cria um dicionario para cada nó

    ax = plt.subplots(figsize=(largura, altura))

    return nx.draw_networkx(
        grafo,
        pos=nx.spring_layout(grafo, k=0.15),
        with_labels=True,
        node_size=[v * 100 for _, v in grau],#tamanho do nó de acordo com seu grau
        node_color=cor_nos,
        edge_color='lightgray',
        labels=nomes_nos,
        font_weight=tamanho_texto,
    )

