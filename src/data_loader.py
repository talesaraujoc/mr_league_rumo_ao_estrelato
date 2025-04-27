import gspread
import pandas as pd
from gspread_dataframe import get_as_dataframe
from google.oauth2.service_account import Credentials

# Variáveis fixas para o seu projeto
SHEET_ID = "1_OQkQpER2aKNnSqezZb15L9u93i-kn2kBUDBwvjqeQI"
NOME_ABA = "main"
ARQUIVO_CREDENCIAL = "service_account.json"

# Critérios de pontos
CRITERIOS = {
    'ATA': {'V': 7, 'E': 0, 'D': -4, 'GOL': 7, 'ASS': 4, 'STG': 2, 'GC': -10, 'AMA': -4, 'AZUL': -8, 'VER': -16, 'PP': -10, 'GS': 0, 'DD': 0, 'DP': 0},
    'MEI': {'V': 7, 'E': 0, 'D': -4, 'GOL': 8.5, 'ASS': 5, 'STG': 2.5, 'GC': -10, 'AMA': -4, 'AZUL': -8, 'VER': -16, 'PP': -10, 'GS': 0, 'DD': 0, 'DP': 0},
    'ZAG': {'V': 7, 'E': 0, 'D': -4, 'GOL': 10, 'ASS': 6, 'STG': 3, 'GC': -10, 'AMA': -4, 'AZUL': -8, 'VER': -16, 'PP': -10, 'GS': 0, 'DD': 0, 'DP': 0},
    'GK':  {'V': 6, 'E': 0, 'D': -3, 'GOL': 16, 'ASS': 10, 'STG': 4, 'GC': -10, 'AMA': -4, 'AZUL': -8, 'VER': -16, 'PP': -10, 'GS': -5, 'DD': 5, 'DP': 20}
}

def carregar_dados_google_sheets(sheet_id: str = SHEET_ID, nome_aba: str = NOME_ABA) -> pd.DataFrame:
    """
    Carrega e trata os dados de uma aba do Google Sheets.
    """
    try:
        scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = Credentials.from_service_account_file(ARQUIVO_CREDENCIAL, scopes=scopes)
        client = gspread.authorize(credentials)
        sheet = client.open_by_key(sheet_id)
        worksheet = sheet.worksheet(nome_aba)

        df = get_as_dataframe(worksheet, evaluate_formulas=True, dtype=str)
        #df = df.dropna(how='all').dropna(axis=1, how='all')

        df = tratar_dataframe(df)

        #print(f"[INFO] Dados carregados e tratados: {df.shape[0]} linhas, {df.shape[1]} colunas.")
        return df

    except Exception as e:
        #print(f"[ERRO] Falha ao carregar dados do Google Sheets: {str(e)}")
        return pd.DataFrame()


def tratar_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Trata o DataFrame: converte tipos e cria a coluna de pontos (PTS).
    """
    # 1. Lista de colunas que devem ser numéricas
    colunas_para_int = ['V', 'E', 'D', 'GOL', 'ASS', 'STG', 'GC', 'AMA', 'AZUL', 'VER', 'PP', 'GS', 'DD', 'DP', 'FALTA']

    # 2. Converte essas colunas para int, preenchendo valores ausentes com 0 antes
    for col in colunas_para_int:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].fillna(0), errors='coerce').fillna(0).astype(int)

    # 3. Função interna para calcular pontos linha a linha
    def calcular_pontos(row):
        posicao = row['POSIÇÃO']
        if posicao not in CRITERIOS:
            return 0  # posição desconhecida
        pontos = sum(row[col] * CRITERIOS[posicao].get(col, 0) for col in CRITERIOS[posicao])
        return pontos

    # 4. Aplica a função no DataFrame
    df['PTS'] = df.apply(calcular_pontos, axis=1)

    return df
