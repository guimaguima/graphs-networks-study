from graphutils import *  # noqa: F403
import numpy as np

def seleciona_no_aleatorio(df, no_escolhido, ano, grafo,samples ,tipo='ini'):

    if df.empty or (not grafo.has_node(no_escolhido)):
        return None
    

    if tipo == 'ini':
        df_filtrado = df[df['earliest_decade'] < ano]
    else:
        df_filtrado = df[df['earliest_decade'] > ano]

    
    size = min(samples,len(df_filtrado.index))

    nos_anteriores = np.random.choice(df_filtrado.index, size=size, replace=False)
    
    nos = [ 
            no 
            for no in nos_anteriores 
            if grafo.has_node(no) and (nx.has_path(grafo, no, no_escolhido) or nx.has_path(grafo, no_escolhido, no))
        ]

    return nos


def calcula_short_path_comparision(no_inicial,no_final,no,grafo):
    results = []

    for ni in no_inicial:
        for nj in no_final:
            grafo_retirar = grafo.copy()

            referencia = len(nx.shortest_path(grafo_retirar,source=nj,target=ni)) if nx.has_path(grafo_retirar, nj, ni) else 0

            grafo_retirar.remove_node(no)

            alterado = len(nx.shortest_path(grafo_retirar,source=nj,target=ni))  if nx.has_path(grafo_retirar, nj, ni) else 0
            
            if referencia!=0:
                calculo_resultado = -(1-(alterado/referencia))
                results.append(calculo_resultado if calculo_resultado!=-1 else 1)
        
    return results



def grafo_simulation_short_path(df,genero='Jazz',disrupcao=0,samples=50):

    data_desejada = get_data_gz('artists.json')
    grafo  = get_grafo_parametros(data_desejada,df,'genre',genero)

    operando = '>' if disrupcao >= 0 else '<'

    if operando == '>':
        nos_disruptivos =  df[(df.get('genre')==genero) & (df.get('disruption')>disrupcao) &  (df.get('disruption')<disrupcao+.1 )].index
    else:
        nos_disruptivos =  df[(df.get('genre')==genero) & (df.get('disruption')<disrupcao) &  (df.get('disruption')>disrupcao-.1)].index

    short_paths = []
    for no in nos_disruptivos:
        decada_inicial =   df.loc[no].get('earliest_decade')

        no_inicial = seleciona_no_aleatorio(df,no,decada_inicial,grafo,samples)

        no_final = seleciona_no_aleatorio(df,no,decada_inicial,grafo,samples, tipo='fim')

        atual_diferenca = calcula_short_path_comparision(no_inicial,no_final,no,grafo)

        short_paths += atual_diferenca


    return short_paths