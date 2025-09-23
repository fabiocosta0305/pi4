import panel as pn      # Biblioteca Panel de Dashboard
import pandas as pd     
import hvplot.pandas
import matplotlib.pyplot as plt

# # Específico para produzir o gráfico de pizza
# from math import pi

# from bokeh.palettes import Category20c, Category20
# from bokeh.plotting import figure
# from bokeh.transform import cumsum

@pn.cache()
def info_cras(dados,cras):
    # print(dados)
    # print(cras)e
    # print("Aqui!")
    dados_pessoas=dados['atendimentos']
    # print(dados_pessoas)
    dados_plotar=dados_pessoas[dados_pessoas['Unidade']==cras]
    indice=dados_plotar['tipo_atendimentos']
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
    dados_plotar.index.names=['Procedência']
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
    # print(top_procedencia)
    return top_procedencia

# @pn.cache()
def graph_cras(dados,cras):
    dados_plotar=top10(info_cras(dados,cras))
    # print(dados_plotar)
    dados_plotarT = dados_plotar.T.reset_index().rename(columns={"index": "Tipo de Atendimento"})
    # dados_plotar.index=dados_plotar['index']
    # dados_plotar=dados_plotar.loc[:,'Total':'Coletivo']
    tipo_atendimentos=dados_plotar.index
    print(tipo_atendimentos)
    dados_plotar.index.names=['Tipo de Atendimento']
    # dados_plotar.rename(columns={0:'Total'}, inplace=True)
    dados_plotar.rename('Total',inplace=True)
    print(dados_plotar)
    # print(dados_plotarT)
    table = pn.pane.DataFrame(dados_plotar, 
                              name=f"# {cras}",
                              sizing_mode='stretch_both',
                              # index=False,
                             )
    # Cria gráfico de barras
    bar_plot = dados_plotar.hvplot.bar(
        y="Total", 
        x="Tipo de Atendimento",
        stacked=False,
        rot=45,
        title=f"# {cras}",
        shared_axes=False,
        sizing_mode='stretch_both',
        legend='top',              # garante exibição
        #legend_position='top_right' # posição da legenda
    )

    # Gráfico de Pizza
    # plt.figure(figsize=(12,6))
    # fig,ax = plt.subplots()
    # plt.title(f"Principais procedências dos Usuários - {cras} 2024", fontsize=14, fontweight='bold')
    # labels=dados_plotar.reset_index()
    # dados=dados_plotar
    # # print(dados)
    # wedges, text = ax.pie(dados)
    # ax.legend(wedges,dados_plotar.index,
    #           title="Procedência",
    #           loc='center left',
    #           bbox_to_anchor=(1, 0, 0.5, 1))
    # # plt.show()
    exibe_dados=pn.Row(
        bar_plot,
        table,)
    return pn.Column(
        f"# Número de Pessoas Atendidas - {cras}",
        exibe_dados, 
        sizing_mode='stretch_both',
    )
