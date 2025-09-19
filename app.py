import panel as pn      # Biblioteca Panel de Dashboard
import pandas as pd     
import hvplot.pandas
import dados            # para a fonte de dados
import atendimentos

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

    
drop_cras = pn.widgets.Select(
    name="CRAS",
    options=sorted(source_data['lista_cras']),
    value=sorted(source_data['lista_cras'])[0],
    description="Lista Completa dos CRAS disponíveis",
)

dados_cras=pn.bind(atendimentos.info_cras, dados=source_data, cras=drop_cras)
graph=pn.bind(atendimentos.graph_cras, dados=source_data, cras=drop_cras)

tabs=pn.Tabs(("Pessoas Atendidas",graph))

# texto_cras=pn.bind(value,cras=drop_cras)

pn.template.FastListTemplate(
    title="Informações CRAS Mauá",
    sidebar=[drop_cras],
    main=[tabs],
    main_layout=None,
    accent=ACCENT,
).servable()