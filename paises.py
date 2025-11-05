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
    dados_pessoas=dados['nacionalidade']
    dados_plotar=dados_pessoas[dados_pessoas['Unidade']==cras]
    indice=dados_plotar['nacionalidade']
    dados_plotar.index=indice[:len(dados_plotar)]
    dados_plotar=dados_plotar.loc[:,'Janeiro':'Dezembro']
    return dados_plotar   

def df_cras(dados,cras):
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

@pn.cache()
def graph_cras(dados,cras):
    dados_plotar=info_cras(dados,cras)
    meses=dados_plotar.columns.tolist()
    lista_paises=dados_plotar.index.tolist()
    lista_paises=lista_paises[1:]
    dados_estrangeiros=dados_plotar[dados_plotar.index.isin(lista_paises)]
    dados_plotarT = dados_plotar.T.reset_index().rename(columns={"index": "Mês"})
    dados_brasil=dados_plotarT['Brasileiro']
    dados_brasil.index=meses
    df_brasil=dados_brasil.to_frame()
    dados_estrangeirosT = dados_estrangeiros.T.reset_index().rename(columns={"index": "Mês"})

    bar_plot = dados_estrangeirosT.hvplot.bar(
        x="Mês", 
        stacked=False,
        rot=45,
        title=f"Atendimento Para Estrandeiros",
        shared_axes=False,
        sizing_mode='stretch_both',
        legend='right',              # garante exibição
    )

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

