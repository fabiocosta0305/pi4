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
    dados_pessoas=dados['demandas']
    dados_plotar=dados_pessoas[dados_pessoas['Unidade']==cras]
    indice=dados_plotar['demandas']
    dados_plotar.index=indice[:len(dados_plotar)]
    dados_plotar=dados_plotar.loc[:,'Janeiro':'Dezembro']
    return dados_plotar   

def df_cras(dados,cras):
    dados_plotar=info_cras(dados,cras)
    dados_plotar.index.names=['Demandas']
    table = pn.pane.DataFrame(dados_plotar, 
                                 name=f"# {cras}",
                                 sizing_mode='stretch_both',
                                )
    row=pn.Card(
                table,
                collapsed=True,
                title=f"Dados total - {cras}",
                sizing_mode='stretch_both',
              )
    return row

def top10(dados):
    totais = dados.sum(axis=1)
    top_procedencia = totais.sort_values(ascending=False).head(5)
    return top_procedencia

@pn.cache()
def graph_cras(dados,cras):
    dados_plotar=top10(info_cras(dados,cras))
    dados_plotarT = dados_plotar.T.reset_index().rename(columns={"index": "Demandas"})
    dados_plotar.index.names=['Demandas']
    dados_plotar.rename('Total',inplace=True)
    table = pn.pane.DataFrame(dados_plotar, 
                              name=f"# {cras}",
                              sizing_mode='stretch_both',
                             )
    # Cria gráfico de barras
    bar_plot = dados_plotar.hvplot.bar(
        x="Demandas", 
        stacked=False,
        rot=45,
        title=f"# {cras}",
        shared_axes=False,
        sizing_mode='stretch_both',
        legend='right',              # garante exibição
    )

    exibe_dados=pn.Row(
        bar_plot,
        table,)
    return pn.Column(
        f"# Demandas Mais Procuradas - {cras}",
        exibe_dados, 
        sizing_mode='stretch_both',
    )
