import json
import gzip
import networkx as nx
import pandas as pd

def extract_id(txt):
    #organiza a nomeclatura
    pos = txt.rfind('mn')
    return txt[pos:pos+12]

def get_data_gz(arquivo_nome):
    #pega o gz definido
    caminho_arquivo = '../data/Artistas/'+arquivo_nome+'.gz'
    with gzip.open(caminho_arquivo) as arquivo:
        json_data = json.load(arquivo) 
        return json_data

def get_df(arquivo_nome,arquivo_ext):
    #pega um dataframe qualquer de um arquivo qualquer
    caminho_arquivo = '../data/Artistas/'+arquivo_nome+'.'+arquivo_ext

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
        if valor_teto is None and valor_chao is not None:
            valor_teto = valor_chao
        #pensando nas épocas e suas influências, pensa de onde começa e onde acaba
        series_nos = df[(df.get(parametro_primeiro) == primeiro_valor) & ((df.get(parametro_epoca)>=valor_chao) & (df.get(parametro_epoca)<=valor_teto))].index
        #nos
    else: 
        series_nos = df[df.get(parametro_primeiro) == primeiro_valor].index
    
    grafo = get_grafo(json_data,series_nos)
    #grafo
    return grafo


def get_artistas_df():
    #pega a tabela de disruptividade
    disruptive = get_df('disrupt','csv')
    disruptive = disruptive[(disruptive.get('ni')>0) & (disruptive.get('nj')>0)].set_index('label').sort_values(by='disruption',ascending=False)
    #pega a tabela de artistas com genêro e  decadas
    artistas = get_df('artist-network-degrees','csv')
    artistas = artistas.set_index('label').dropna()
    #tabela cruzada dos dois
    disruption_genero = artistas.get(['name','earliest_decade','genre']).join(disruptive.get(['ni','nj','nk','disruption','confidence'])).dropna()
    return disruption_genero
