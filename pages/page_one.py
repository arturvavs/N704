import duckdb
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import warnings
from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output, State
from dash_ag_grid import AgGrid

warnings.simplefilter("ignore", UserWarning)
dados_gestao = pd.read_excel('lotes_gestao.xlsx',engine='openpyxl') #Realiza o carregamento do arquivo xlsx
dados_analitico = pd.read_excel('lotes_analitico.xlsx',engine='openpyxl') #Realiza o carregamento do arquivo xlsx


def definir_formatador(formato: str): # Função de alta ordem (higher-order function) - recebe e retorna funções
    def formatar_data(x): # Closure - a função interna captura e "lembra" da variável formato do escopo externo
        return x.strftime(formato) if pd.notna(x) else '' # Expressão condicional que segue o paradigma de avaliação preguiçosa (lazy evaluation)
    return formatar_data # Retorna a função como um valor de primeira classe

def formatar_colunas_de_data(df, formato: str): # Função que aplica transformações de forma declarativa aos dados do dataframe
    colunas_de_data = [col for col in df.columns if 'DT' in col]  # List comprehension - forma declarativa de criar listas
    df[colunas_de_data] = df[colunas_de_data].replace('NULL', pd.NA) #Converte o que está nulo para o formato 'NA' para evitar erros na formatação da data
    df[colunas_de_data] = df[colunas_de_data].apply(pd.to_datetime, errors='coerce') #Converte o tipo de dados das colunas de data para 'datetime'
    
    formatador = definir_formatador(formato) # Utilização da função de alta ordem criada anteriormente
    df[colunas_de_data] = df[colunas_de_data].map(formatador) # Aplicação de função como valor (map) - operação funcional clássica

    return df 

dados_analitico = formatar_colunas_de_data(dados_analitico, formato='%d/%m/%Y %H:%M:%S') 
dados_analitico['NR_SEQ_CLASSIF'] = dados_analitico['NR_SEQ_CLASSIF'].apply(lambda x: '![](/assets/muito_urgente.png)' if x == 13 else '![](/assets/pouco_urgente.png)') # Uso de função lambda (função anônima) - característica funcional
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
            columnDefs=[{"field":i} for i in dados_analitico.columns], # List comprehension - forma funcional e declarativa de criar listas
            defaultColDef={"cellRenderer": "markdown"},
            columnSize="responsiveSizeToFit"
        )
    ])
])
