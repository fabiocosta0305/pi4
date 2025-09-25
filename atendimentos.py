import panel as pn      # Biblioteca Panel de Dashboard
import pandas as pd     
import hvplot.pandas
#import dados            # para a fonte de dados

@pn.cache()
def info_cras(dados,cras):
    # print(dados)
    # print(cras)e
    dados_pessoas=dados['pessoas']
    dados_plotar=dados_pessoas[dados_pessoas['Unidade']==cras]
    # tipos=pd.concat([pd.Series('Mês'),dados_plotar['Tipo']])
    # tipos.insert(loc=0,column='Tipo', value='Mês')
    # print(tipos)
    tipos=dados_plotar['Tipo']
    dados_plotar.index=dados_plotar['Tipo']
    dados_plotar=dados_plotar.loc[:,'Janeiro':'Dezembro']
    # print(dados_plotar)
    return dados_plotar   

@pn.cache()
def graph_cras(dados,cras):
    # pn.extension('plotly')  # ativa integração com Plotly
    # print(dados_plotar)
    dados_plotar=info_cras(dados,cras)
    dados_plotarT = dados_plotar.T.reset_index().rename(columns={"index": "Mês"})
    # dados_plotar.index=dados_plotar['index']
    # dados_plotar=dados_plotar.loc[:,'Total':'Coletivo']
    # print(dados_plotarT)
    table = pn.pane.DataFrame(dados_plotar, 
                              name=f"# {cras}",
                              sizing_mode='stretch_both',
                              index=False,
                             )
    # Cria gráfico de barras
    bar_plot = dados_plotarT.hvplot.bar(
        x="Mês", 
        y=dados_plotar.index,   # usa as métricas como séries
        stacked=False,
        rot=45,
        title=f"# {cras}",
        shared_axes=False,
        sizing_mode='stretch_both',
        legend='right',              # garante exibição
        #legend_position='top_right' # posição da legenda
    )
    
    return pn.Column(
        f"# Número de Pessoas Atendidas - {cras}",
        bar_plot,
        table,
        sizing_mode='stretch_both',
    )
