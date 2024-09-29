from grafoutils import *  # noqa: F403
import numpy as np

def seleciona_nos(df, no_escolhido, ano, grafo ,tipo='ini'):

    if df.empty or (not grafo.has_node(no_escolhido)):
        return None
    

    if tipo == 'ini':
        df_filtrado = df[df['earliest_decade'] <= ano]
    else:
        df_filtrado = df[df['earliest_decade'] >= ano]

    
    nos_anteriores = list(df_filtrado.index)
    
    nos = [ 
            no 
            for no in nos_anteriores 
            if grafo.has_node(no) 
            and no!=no_escolhido
            and (nx.has_path(grafo, no, no_escolhido) 
                 or nx.has_path(grafo, no_escolhido, no))
        ]

    return nos

def calculo_media(total):
    somatorio = 0
    divisor = 1

    for i in total:
        somatorio += len(i)

    if len(total) > 0: 
        divisor = len(total)

    media = somatorio/divisor

    return media

def subgrafo_randomico_media(no_inicial_lista,no_final_lista,no_desejado,repeticoes=10000):

    data_desejada = get_data_gz('artists.json')

    medias = []
    for _ in range(repeticoes):
        total_base = []
        total_alterado = []

        if not( no_inicial_lista == [] ) and not (no_final_lista == []): 
            no_inicial = np.random.choice(no_inicial_lista,replace=False)
            no_final = np.random.choice(no_final_lista,replace=False)

            nos_aleatorios = [no_inicial,no_final,no_desejado]
            grafo_aleatorio = get_grafo(data_desejada,nos_aleatorios)

            valor_base = (
                    nx.all_shortest_paths(grafo_aleatorio,no_final,no_inicial) 
                    if nx.has_path(grafo_aleatorio,no_final,no_inicial) 
                    else []
                    )

            total_base += valor_base

            grafo_aleatorio.remove_node(no_desejado)

            valor_alterado = (
                    nx.all_shortest_paths(grafo_aleatorio,no_final,no_inicial) 
                    if nx.has_path(grafo_aleatorio,no_final,no_inicial) 
                    else []
                    )

            total_alterado += valor_alterado

            media_base = calculo_media(total_base)
            media_alterado = calculo_media(total_alterado)

            if not (media_base == 0):
                medias.append(abs(media_base - media_alterado))


    return medias






def grafo_simulation_short_path(genero='Jazz',disrupcao=0.2):
    df = get_artistas_df()
    data_desejada = get_data_gz('artists.json')
    grafo  = get_grafo_parametros(data_desejada,df,'genre',genero)

    operando = '>' if disrupcao >= 0 else '<'

    if operando == '>':
        nos_disruptivos =  df[(df.get('genre')==genero) & (df.get('disruption')>=disrupcao) &  (df.get('disruption')<disrupcao+.1 )].index
    else:
        nos_disruptivos =  df[(df.get('genre')==genero) & (df.get('disruption')<disrupcao) &  (df.get('disruption')>disrupcao-.1)].index

    short_paths_mean = np.array([])
    for no in nos_disruptivos:
        decada_inicial =   df.loc[no].get('earliest_decade')
        
        no_inicial_lista = seleciona_nos(df,no,decada_inicial,grafo)

        no_final_lista = seleciona_nos(df,no,decada_inicial,grafo, tipo='fim')

        short_paths_mean = np.append(short_paths_mean,subgrafo_randomico_media(no_inicial_lista,no_final_lista,no))

    return short_paths_mean