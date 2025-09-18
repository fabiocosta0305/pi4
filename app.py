import panel as pn      # Biblioteca Panel de Dashboard
import pandas as pd     
import hvplot.pandas
import dados            # para a fonte de dados

pn.extension("tabulator")

ACCENT="teal"

styles = {
    "box-shadow": "rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, rgba(0, 0, 0, 0.3) 0px 3px 7px -3px",
    "border-radius": "4px",
    "padding": "10px",
}

image = pn.pane.JPG("https://assets.holoviz.org/panel/tutorials/wind_turbines_sunset.png")

# Extract Data

@pn.cache()  # only download data once
def get_data():
    return dados.cria_dados()

# Transform Data

source_data = get_data()
# min_year = int(source_data["p_year"].min())
# max_year = int(source_data["p_year"].max())

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

def graph_cras(dados,cras):
    dados_plotar=info_cras(dados,cras)
    dados_plotarT = dados_plotar.T.reset_index().rename(columns={"index": "Mês"})
    # dados_plotar.index=dados_plotar['index']
    # dados_plotar=dados_plotar.loc[:,'Total':'Coletivo']
    dados_plotar.rename(columns={'index':'Mês'}, inplace=True)
    # print(dados_plotarT)
    table = pn.pane.DataFrame(dados_plotar, 
                                 name=f"# {cras}",
                                 sizing_mode='stretch_both',
                                 index=False,
                                 height=200)
    # Cria gráfico de barras
    bar_plot = dados_plotarT.hvplot.bar(
        x="Mês", 
        y=dados_plotar.index,   # usa as métricas como séries
        stacked=False,
        rot=45,
        title=f"# {cras}",
        shared_axes=False,
        sizing_mode='stretch_both',
        legend='top',              # garante exibição
        #legend_position='top_right' # posição da legenda
    )
    return pn.Column(
        f"# Número de Pessoas Atendidas - {cras}",
        bar_plot,
        table,
    )
    
drop_cras = pn.widgets.Select(
    name="CRAS",
    options=sorted(source_data['lista_cras']),
    value=sorted(source_data['lista_cras'])[0],
    description="Lista Completa dos CRAS disponíveis",
)

dados_cras=pn.bind(info_cras, dados=source_data, cras=drop_cras)
graph=pn.bind(graph_cras, dados=source_data, cras=drop_cras)

# texto_cras=pn.bind(value,cras=drop_cras)

pn.template.FastListTemplate(
    title="Informações CRAS Mauá",
    sidebar=[drop_cras],
    main=[graph],
    main_layout=None,
    accent=ACCENT,
).servable()