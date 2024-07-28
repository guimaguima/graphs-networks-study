from graphutils import *  # noqa: F403
import matplotlib.pyplot as plt

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

def lista_histograma(lista,largura=10,altura=8,title='Porcentagem de alteração do menor caminho',xlabel='Alteração Positiva',ylabel='Frequência Absoluta'):
    plt.subplots(figsize=(10, 8))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.hist(lista, rwidth=0.9)
    plt.show()
