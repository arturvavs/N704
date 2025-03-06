import duckdb
import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import warnings
from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output, State
from dash_ag_grid import AgGrid

warnings.simplefilter("ignore", UserWarning)
dados_gestao = pd.read_excel('lotes_gestao.xlsx',engine='openpyxl')
dados_analitico = pd.read_excel('lotes_analitico.xlsx',engine='openpyxl')

def definir_formatador(formato: str): #Função de Alta Ordem + Alicação de Closure
    def formatar_data(x):
        return x.strftime(formato) if pd.notna(x) else ''
    return formatar_data

def formatar_coluna_data(df, formato: str):
    coluna_data = [col for col in df.columns if 'DT' in col] #Faço uma busca em cada coluna que contém o termo 'DT'
    df[coluna_data] = df[coluna_data].replace('NULL', pd.NA) #Caso haja alguma célular em que a Data não esteja preenchida, transformo o valor em 'NA'
    df[coluna_data] = df[coluna_data].apply(pd.to_datetime, errors='coerce')#Transformo todas as colunas no formato datetime
    
    formatador = definir_formatador(formato) #Aplico o conceito da Closure, armazenando uma função na variável formatador
    df[coluna_data] = df[coluna_data].map(formatador) #Utilizo o map para aplicar o formato desejado em cada célula de data

    return df

dados_analitico = formatar_coluna_data(dados_analitico, formato='%d/%m/%Y %H:%M:%S')
dados_analitico['NR_SEQ_CLASSIF'] = dados_analitico['NR_SEQ_CLASSIF'].apply(lambda x: '![](/assets/muito_urgente.png)' if x == 13 else '![](/assets/pouco_urgente.png)') #Função Lambda
dados_analitico = dados_analitico.iloc[:,[0,2,3,6,7,13]]
dados_analitico.columns = ['Nº LOTE','TURNO','SETOR','ENTREGA PREVISTA','STATUS','URGENCIA']

dash.register_page(
    __name__, 
    path='/n704',
    name='Atividade - N704'
    )

layout = html.Div(children=[
    html.Div([
        AgGrid(
            rowData=dados_analitico.to_dict('records'),
            columnDefs=[{"field":i} for i in dados_analitico.columns], #List comprehension
            defaultColDef={"cellRenderer": "markdown"},
            columnSize="responsiveSizeToFit"
        )
    ])
])