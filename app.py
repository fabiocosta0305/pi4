# Importar bibliotecas
import panel as pn                      # Biblioteca Panel de Dashboard
import pandas as pd                     # Pandas
import hvplot.pandas                    # Biblioteca do HVPlot para Pandas

# Bibliotecas do MatPlotLib
from matplotlib.figure import Figure    
from matplotlib import cm
import matplotlib.pyplot as plt

# Widgets e dados
import dados            # para a fonte de dados
import atendimentos     # Atendimento por mês
import horario          # Faixa de Horário
import procedencias     # Procedências
import demandas         # Demandas
import tipo             # Tipo de Atendimento
import paises           # Paises

# Extensões a serem ativadas para os gráicos
pn.extension("tabulator")
pn.extension('ipywidgets')
pn.extension('plotly')

# Apenas necessário para que não seja gerado uma série de Warnings do Panels
pd.set_option('future.no_silent_downcasting', True)

ACCENT="teal"

# Obtem dados 
#
# @pn.cache() faz com que os dados sejam gerados apenas uma vez

#@pn.cache()  # only download data once
def get_data():
    return dados.cria_dados()

source_data = get_data()


# Widget de lista dos CRAS
drop_cras = pn.widgets.Select(
    name="CRAS",
    options=sorted(source_data['lista_cras']),
    value=sorted(source_data['lista_cras'])[0],
    description="Lista Completa dos CRAS disponíveis",
)


# Fazendo os binds necessário (de modo a gerar as interações)

graph_pessoas=pn.bind(atendimentos.graph_cras, dados=source_data, cras=drop_cras)

graph_horarios=pn.bind(horario.graph_cras, dados=source_data, cras=drop_cras)

procedencias_cras=pn.bind(procedencias.df_cras, dados=source_data, cras=drop_cras)
top_procedencias=pn.bind(procedencias.graph_cras, dados=source_data, cras=drop_cras)

demandas_cras=pn.bind(demandas.df_cras, dados=source_data, cras=drop_cras)
top_demandas=pn.bind(demandas.graph_cras, dados=source_data, cras=drop_cras)

top_tipos=pn.bind(tipo.graph_cras, dados=source_data, cras=drop_cras)

# horarios_cras=pn.bind(horario.info_cras, dados=source_data, cras=drop_cras)
# dados_cras=pn.bind(atendimentos.info_cras, dados=source_data, cras=drop_cras)
#tipos_cras=pn.bind(tipo.df_cras, dados=source_data, cras=drop_cras)
#pizza_cras=pn.bind(tipo.pizza_cras, dados=source_data, cras=drop_cras)
# graph_horarios=pn.bind(procedencias.horario.graph_cras, dados=source_data, cras=drop_cras)
paises_cras=pn.bind(paises.graph_cras, dados=source_data, cras=drop_cras)
df_cras=pn.bind(paises.df_cras, dados=source_data, cras=drop_cras)

#M Montando as Tabs Principais

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
                ("Países de Atendimentos",pn.Column(
                        paises_cras,df_cras)),
            )

# texto_cras=pn.bind(value,cras=drop_cras)

# Publicação do Dashboard

pn.template.FastListTemplate(
    title="Informações CRAS Mauá",
    sidebar=[drop_cras],
    main=[tabs],
    main_layout=None,
    accent=ACCENT,
).servable()