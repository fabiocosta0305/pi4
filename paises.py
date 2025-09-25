import panel as pn      # Biblioteca Panel de Dashboard
import pandas as pd     
import hvplot.pandas
import matplotlib.pyplot as plt

# Específico para produzir o gráfico de pizza
from math import pi

from bokeh.palettes import Category20c, Category20
from bokeh.plotting import figure
from bokeh.transform import cumsum

@pn.cache()
def info_cras(dados,cras):
    # print(dados)
    # print(cras)e
    # print("Aqui!")
    dados_pessoas=dados['nacionalidade']
    dados_plotar=dados_pessoas[dados_pessoas['Unidade']==cras]
    indice=dados_plotar['nacionalidade']
    dados_plotar.index=indice[:len(dados_plotar)]
    # print(dados_plotar) 
    # tipos=pd.concat([pd.Series('Mês'),dados_plotar['Tipo']])
    # tipos.insert(loc=0,column='Tipo', value='Mês')
    # print(tipos)
    # tipos=dados_plotar['Tipo']
    # dados_plotar.index=dados_plotar['Tipo']
    dados_plotar=dados_plotar.loc[:,'Janeiro':'Dezembro']
    # print(dados_plotar)
    return dados_plotar   

def df_cras(dados,cras):
    # print("Aqui - df!")
    dados_plotar=info_cras(dados,cras)
    dados_plotar.index.names=['nacionalidade']
    table = pn.pane.DataFrame(dados_plotar, 
                                 name=f"# {cras}",
                                 sizing_mode='stretch_both',
                                )
    row=pn.Row(
                table,
                sizing_mode='stretch_both',
              )
    return row

# @pn.cache()
def graph_cras(dados,cras):
    dados_plotar=info_cras(dados,cras)
    meses=dados_plotar.columns.tolist()
    lista_paises=dados_plotar.index.tolist()
    lista_paises=lista_paises[1:]
    # print(lista_paises)
    # dados_estrangeiros=dados_plotar[dados_plotar
    dados_estrangeiros=dados_plotar[dados_plotar.index.isin(lista_paises)]
    # print(dados_estrangeiros)
    dados_plotarT = dados_plotar.T.reset_index().rename(columns={"index": "Mês"})
    # print(dados_plotar)
    dados_brasil=dados_plotarT['Brasileiro']
    dados_brasil.index=meses
    df_brasil=dados_brasil.to_frame()
    print(df_brasil)
    # print(dados_plotarT)
    dados_estrangeirosT = dados_estrangeiros.T.reset_index().rename(columns={"index": "Mês"})

    bar_plot = dados_estrangeirosT.hvplot.bar(
        x="Mês", 
        stacked=False,
        rot=45,
        title=f"Atendimento Para Estrandeiros",
        shared_axes=False,
        sizing_mode='stretch_both',
        legend='right',              # garante exibição
        #legend_position='top_right' # posição da legenda
    )

    
    # fig=df_brasil.hvplot.bar(
    #     y="Mês", 
    #     stacked=False,
    #     rot=45,
    #     title=f"Atendimento Para Brasileiros",
    #     shared_axes=False,
    #     sizing_mode='stretch_both',
    #     legend='right',              # garante exibição
    #     #legend_position='top_right' # posição da legenda
    # )

    fig = df_brasil.hvplot.bar(
        y="Brasileiro",
        title="Atendimentos por Mês",
        xlabel="Mês",
        ylabel="Quantidade",
        rot=45   # gira os rótulos do eixo X para melhor visualização
    )
    
    return pn.Row(
            fig,
            bar_plot,
            sizing_mode='stretch_both',
    )

