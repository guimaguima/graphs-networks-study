from graphutils import *  # noqa: F403
import numpy as np

def centralidade(metodo=nx.degree_centrality,genero='Jazz',arquivo='artists.json'):
    df = get_artistas_df()
    data_desejada = get_data_gz(arquivo)
    grafo  = get_grafo_parametros(data_desejada,df,'genre',genero)

    df = df[(df.get('genre') == genero)]

    medida = metodo(grafo)

    keys = list(medida.keys())
    values = list(medida.values())
    index_sorteados = np.argsort(values)
    result = {keys[i]: values[i] for i in index_sorteados}

    return result # resultado

