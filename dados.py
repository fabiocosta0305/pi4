import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def cria_dados():
    # pd.set_option('future.no_silent_downcasting', True)
    
    arquivo = "CONSOLIDADO 2024 JAN-DEZ.xlsx"
    # df_raw = pd.read_excel(arquivo, header=None)
    # df_raw.iloc[:30, :40]
    
    # df_raw.info()
   
   
   # SEPARAÇÃO PARA OBTER QUANTIDADE DE PESSOAS

    # Lendo a planilha sem cabeçalho
    #df_raw = pd.read_excel("/kaggle/input/consolidadorma/CONSOLIDADO 2024 JAN-DEZ.xlsx",sheet_name='CRAS GERAL', header=None)
    lista_cras=['CRAS FALCHI',
                'CRAS FEITAL',
                'CRAS MACUCO',
                'CRAS ORATORIO',
                'CRAS PARQUE',
                'CRAS SAO JOAO',
                'CRAS VILA',
                'CRAS ZAIRA',
                'CRAS GERAL',]
    # Janeiro até Dezembro (colunas 39 a 50)
    meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
             "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    col_inicio = 39  # coluna Janeiro
    col_fim = 50     # coluna Dezembro

    # print(lista_cras)
    
    dados_pessoas=pd.DataFrame()

    for cras in lista_cras:
        # print(cras)
        # Pegar as três linhas da seção 1.1 (Total, Individual, Coletivo)
        df_raw=pd.read_excel(arquivo,sheet_name=cras,header=None)
        if (cras=='CRAS GERAL'):
            dados = df_raw.iloc[13:16, col_inicio:col_fim+1]
        else:
            dados = df_raw.iloc[12:15, col_inicio:col_fim+1]
        # Zerar os NaN
        # dados.fillna(value=0,inplace=True) 
        dados.columns = meses
        dados['Tipo'] = ["Total", "Individual", "Coletivo"]
        dados['Unidade'] = cras
        dados_pessoas=pd.concat([dados_pessoas,dados])
    dados_pessoas.fillna(value=0,inplace=True) # Ajustando valores vazios

    # DataFrame com dados de Atendimento por Faixa de Horário

    dados_horario=pd.DataFrame()
    
    for cras in lista_cras:
        df_raw=pd.read_excel(arquivo,sheet_name=cras,header=None)
        if (cras=='CRAS GERAL'):
            dados = df_raw.iloc[17:22, col_inicio:col_fim+1]
        else:
            dados = df_raw.iloc[16:21, col_inicio:col_fim+1]
    
        # Definir os índices corretamente
        dados.index = ["08h as 09h59", "10h00 as 11h59", "12h00 as 12h59","13h00 as 14h59","15h00 as 17h00"]
        dados.columns = meses
        dados['Unidade'] = cras
        dados_horario=pd.concat([dados_horario,dados])
    dados_horario.fillna(value=0,inplace=True) # Ajustando valores vazios
    
    # DataFrame de Procedências

    dados_procedencias=pd.DataFrame()


    tipos_procedencia = [
        "Associações", "Atendimento Agendado", "Busca Ativa", "Cadastro Único",
        "Câmara Municipal", "Conselho Tutelar", "Defensoria Pública",
        "Demanda Espontânea", "Educação", "Indicação Informal", "INSS",
        "Retorno de Acompanhamento", "Retorno de Agendamento",
        "Retorno de Atividades do CRAS", "Saúde",
        "Secretaria de Assistência Social", "Segurança Alimentar",
        "Unidades PSB", "Unidades PSE", "Usuário do CRAS", "Outro"
    ]

    for cras in lista_cras:
        df_raw=pd.read_excel(arquivo,sheet_name=cras,header=None)
        if (cras=='CRAS GERAL'):
            procedencia = df_raw.iloc[23:44, col_inicio:col_fim+1]
        else:
            procedencia = df_raw.iloc[22:43, col_inicio:col_fim+1]
        # procedencia.index = tipos_procedencia[:len(procedencia)]
        # dados = df_raw.iloc[16:21, col_inicio:col_fim+1]

        # Definir os índices corretamente
        procedencia.columns = meses
        procedencia['procedencia']=tipos_procedencia[:len(procedencia)]
        procedencia['Unidade'] = cras
        dados_procedencias=pd.concat([dados_procedencias,procedencia])
        # print(procedencia)
    dados_procedencias.fillna(value=0,inplace=True) # Ajustando valores vazios
    # dados_procedencias

    # Dados de Demandas

    dados_demandas = pd.DataFrame()

    # df_raw=pd.read_excel(arquivo,sheet_name='CRAS GERAL',header=None)
    # Pegar os nomes das demandas na coluna A (coluna 0)

    for cras in lista_cras:
        df_raw=pd.read_excel(arquivo,sheet_name=cras,header=None)
        if (cras=='CRAS GERAL'):
            nomes_demandas = df_raw.iloc[46:77, 0].tolist()
            demandas = df_raw.iloc[45:76, col_inicio:col_fim+1]
        else:
            nomes_demandas = df_raw.iloc[45:76, 0].tolist()
            demandas = df_raw.iloc[44:74, col_inicio:col_fim+1]
        demandas.columns = meses
        demandas['demandas']=nomes_demandas[:len(demandas)]
        demandas['Unidade'] = cras
        # print(demandas)
        dados_demandas=pd.concat([dados_demandas,demandas])
    dados_demandas.fillna(value=0,inplace=True) # Ajustando valores vazios
    # dados_demandas

    # Dados sobre Tipo de Atendimento

    dados_tipo_atendimentos=pd.DataFrame()

    # df_raw=pd.read_excel(arquivo,sheet_name='CRAS GERAL',header=None)
    # Pegar os nomes das demandas na coluna A (coluna 0)

    for cras in lista_cras:
        df_raw=pd.read_excel(arquivo,sheet_name=cras,header=None)
        # Pegar as três linhas da seção
        if (cras=='CRAS GERAL'):
            tipo_atendimentos = df_raw.iloc[81:84, col_inicio:col_fim+1]
            lista_tipo_atendimentos = df_raw.iloc[81:84, 0].tolist()
            # print(tipo_atendimentos)
        else:
            tipo_atendimentos = df_raw.iloc[80:83, col_inicio:col_fim+1]
            lista_tipo_atendimentos = df_raw.iloc[80:83, 0].tolist()
        
        # Pegar os nomes das demandas na coluna A (coluna 0)
        tipo_atendimentos.columns=meses
        tipo_atendimentos['tipo_atendimentos']=lista_tipo_atendimentos[:len(tipo_atendimentos)]
        tipo_atendimentos['Unidade']=cras
        dados_tipo_atendimentos=pd.concat([dados_tipo_atendimentos,tipo_atendimentos])
    dados_tipo_atendimentos.fillna(value=0,inplace=True)
    # dados_tipo_atendimentos

    # Dados sobre Nacionalidade

    dados_nacionalidade=pd.DataFrame()
    for cras in lista_cras:
        df_raw=pd.read_excel(arquivo,sheet_name=cras,header=None)
        if (cras=='CRAS GERAL'):
            nacionalidade = df_raw.iloc[85:92, col_inicio:col_fim+1]
            lista_nacionalidade = df_raw.iloc[85:92, 0].tolist()
        else:
            nacionalidade = df_raw.iloc[84:91, col_inicio:col_fim+1]
            lista_nacionalidade = df_raw.iloc[84:91, 0].tolist()
        
        # Pegar os nomes das demandas na coluna A (coluna 0)
        nacionalidade.columns=meses
        nacionalidade['nacionalidade']=lista_nacionalidade[:len(nacionalidade)]
        nacionalidade['Unidade']=cras
        dados_nacionalidade=pd.concat([dados_nacionalidade,nacionalidade])
    dados_nacionalidade.fillna(value=0,inplace=True)
    # dados_nacionalidade

    dados_totais={'pessoas': dados_pessoas,
                  'horarios': dados_horario,
                  'procedencias': dados_procedencias,
                  'demandas': dados_demandas,
                  'atendimentos': dados_tipo_atendimentos,
                  'nacionalidade': dados_nacionalidade,
                  'lista_cras': lista_cras}
    return dados_totais