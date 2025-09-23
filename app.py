import panel as pn      # Biblioteca Panel de Dashboard
import pandas as pd     
import hvplot.pandas
from matplotlib.figure import Figure
from matplotlib import cm
import matplotlib.pyplot as plt

import dados            # para a fonte de dados
import atendimentos
import horario
import procedencias
import demandas
import tipo


pn.extension("tabulator")
pn.extension('ipywidgets')

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

# dados_cras=pn.bind(atendimentos.info_cras, dados=source_data, cras=drop_cras)
graph_pessoas=pn.bind(atendimentos.graph_cras, dados=source_data, cras=drop_cras)

# horarios_cras=pn.bind(horario.info_cras, dados=source_data, cras=drop_cras)
graph_horarios=pn.bind(horario.graph_cras, dados=source_data, cras=drop_cras)

procedencias_cras=pn.bind(procedencias.df_cras, dados=source_data, cras=drop_cras)
top_procedencias=pn.bind(procedencias.graph_cras, dados=source_data, cras=drop_cras)

demandas_cras=pn.bind(demandas.df_cras, dados=source_data, cras=drop_cras)
top_demandas=pn.bind(demandas.graph_cras, dados=source_data, cras=drop_cras)

tipos_cras=pn.bind(tipo.df_cras, dados=source_data, cras=drop_cras)
top_tipos=pn.bind(tipo.graph_cras, dados=source_data, cras=drop_cras)

# graph_horarios=pn.bind(procedencias.horario.graph_cras, dados=source_data, cras=drop_cras)

tabs=pn.Tabs(
                ("Pessoas Atendidas",graph_pessoas),
                ("Horário de Atendimento",graph_horarios),
                ("Origem de Atendimento",pn.Column(
                        top_procedencias,
                        procedencias_cras)),
                ("Demandas",pn.Column(
                        top_demandas,
                        demandas_cras)),
                ("Tipo de Atendimentos",pn.Column(
                        top_tipos)),
            )

# texto_cras=pn.bind(value,cras=drop_cras)

pn.template.FastListTemplate(
    title="Informações CRAS Mauá",
    sidebar=[drop_cras],
    main=[tabs],
    main_layout=None,
    accent=ACCENT,
).servable()