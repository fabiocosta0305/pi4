import panel as pn      # Biblioteca Panel de Dashboard
import pandas as pd     
import hvplot.pandas
#import dados            # para a fonte de dados

@pn.cache()
def info_cras(dados,cras):
    # print(dados)
    # print(cras)e
    dados_pessoas=dados['horarios']
    dados_plotar=dados_pessoas[dados_pessoas['Unidade']==cras]
    dados_plotar.index.names=['Período']
    # print(dados_plotar) 
    # tipos=pd.concat([pd.Series('Mês'),dados_plotar['Tipo']])
    # tipos.insert(loc=0,column='Tipo', value='Mês')
    # print(tipos)
    # tipos=dados_plotar['Tipo']
    # dados_plotar.index=dados_plotar['Tipo']
    dados_plotar=dados_plotar.loc[:,'Janeiro':'Dezembro']
    # print(dados_plotar)
    return dados_plotar   

# @pn.cache()
def graph_cras(dados,cras):
    dados_plotar=info_cras(dados,cras)
    dados_plotarT = dados_plotar.T.reset_index().rename(columns={"index": "Mês"})
    # print(dados_plotarT)
    fig=dados_plotarT.hvplot.line(
        x="Mês",
        title=cras,
        shared_axes=False,
        rot=45,
    )   
    table = pn.pane.DataFrame(dados_plotar, 
                              name=f"# {cras}",
                              sizing_mode='stretch_both',
                             )
    return pn.Column(
        f"# Horário de Atendimento - {cras}",
        fig,
        table,
        sizing_mode='stretch_both',
    )