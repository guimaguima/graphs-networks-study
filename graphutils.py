import json
import gzip
import networkx as nx
import pandas as pd

def extract_id(txt):
    pos = txt.rfind('mn')
    return txt[pos:pos+12]

def get_data(arquivo_nome):
    caminho_arquivo = './data/'+arquivo_nome+'.gz'
    with gzip.open(caminho_arquivo) as arquivo:
        json_data = json.load(arquivo) 
        return json_data

def get_df(arquivo_nome,arquivo_ext):
    caminho_arquivo = './data/'+arquivo_nome+'.'+arquivo_ext

    if arquivo_ext.find('json') > 0:
        df = pd.read_json(caminho_arquivo)


    elif arquivo_ext.find('gz') > 0:
        with gzip.open(caminho_arquivo) as arquivo:
            df = pd.read_json(arquivo)
    
    else: 
        df = pd.read_csv(caminho_arquivo)

    return df

def get_grafo(json_data, nos_desejados=None, retritivo=False, parametro='influencer'):
    grafo_direcidonado = nx.DiGraph()
    
    if nos_desejados is None:
        nos_desejados = set(json_data.keys())
    
    for no in nos_desejados:
        data = json_data[no]
        by_set = set(map(extract_id, data[parametro]))
        for by in by_set:
            if retritivo and by not in nos_desejados:
                continue
            grafo_direcidonado.add_edge(no, by)

    return grafo_direcidonado