# !pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client pymysql


import os
import pymysql
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

api_google_sheets = os.getenv("api_google_sheets")

data_select = {
    "API": api_google_sheets,
    "Navegação": "1iOeJtnc_TzU67WMP4JdKuUKBVVo7T2G48Gp_3lgxUR8",
}

# Configurações do banco de dados MySQL
db_config = {
    "host": "srv720.hstgr.io",
    "user": "u611546537_DBA_Bot_Music",
    "password": "S3nh@DBABM@@vjb2024$$$",
    "database": "u611546537_bot_music",
}

# Configurações do Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SERVICE_ACCOUNT_FILE = r"audit-robot-423614-cc520521f536.json"

RANGE_NAME = "Sheet1!A1"

# Cabeçalhos esperados
HEADER = [
    "Artista",
    "Data",
    "Visualizacao",
    "Plataforma",
    "Estimativa_de_Lucro",
    "Diferenca_View",
    "Origem",
    "Tempo_de_Navegacao",
    "Qtde_Perfils_Navegados",
]
# TODO: Artista	Data	Visualizacao	Plataforma	Estimativa_de_Lucro	Diferenca_View		Origem	Tempo_de_Navegacao	Qtde_Perfils_Navegados


def buscar_dados_semanal(origem):
    conexao = pymysql.connect(**db_config)
    cursor = conexao.cursor()

    data_semana_passada = (datetime.now() - timedelta(days=7)).strftime(
        "%Y-%m-%d 00:00:00"
    )
    # data_ano_passado = (datetime.now() - timedelta(days=360)).strftime("%Y-%m-%d 00:00:00")

    query_youtube = """
    SELECT artista, data, visualizacao, plataforma, estimativa_de_lucro, diferenca_view,origem,tempo_de_navegacao_seconds,qtde_perfis_navegados
    FROM Auditoria_musicas
    WHERE plataforma = 'YouTube' AND data >= %s AND origem = %s
    """
    query_spotify = """
    SELECT artista, data, visualizacao, plataforma, estimativa_de_lucro, diferenca_view,origem,tempo_de_navegacao_seconds,qtde_perfis_navegados
    FROM Auditoria_musicas
    WHERE plataforma = 'Spotify' AND data >= %s AND origem = %s
    """
    query_deezer = """
    SELECT artista, data, visualizacao, plataforma, estimativa_de_lucro, diferenca_view,origem,tempo_de_navegacao_seconds,qtde_perfis_navegados
    FROM Auditoria_musicas
    WHERE plataforma = 'Deezer' AND data >= %s AND origem = %s
    """
    query_tiktok = """
    SELECT artista, data, visualizacao, plataforma, estimativa_de_lucro, diferenca_view,origem,tempo_de_navegacao_seconds,qtde_perfis_navegados
    FROM Auditoria_musicas
    WHERE plataforma = 'TikTok' AND data >= %s AND origem = %s
    """

    cursor.execute(query_youtube, (data_semana_passada, origem))
    dados_youtube = cursor.fetchall()

    cursor.execute(query_spotify, (data_semana_passada, origem))
    dados_spotify = cursor.fetchall()

    cursor.execute(query_deezer, (data_semana_passada, origem))
    dados_deezer = cursor.fetchall()

    cursor.execute(query_tiktok, (data_semana_passada, origem))
    dados_tiktok = cursor.fetchall()

    conexao.close()

    return dados_youtube, dados_spotify, dados_deezer, dados_tiktok


def garantir_cabecalhos(service, SPREADSHEET_ID):
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=SPREADSHEET_ID, range="Sheet1!A1:F1")
        .execute()
    )

    values = result.get("values", [])

    if not values or values[0] != HEADER:
        body = {"values": [HEADER]}
        service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range="Sheet1!A1",
            valueInputOption="RAW",
            body=body,
        ).execute()


def atualizar_google_sheets(dados, SPREADSHEET_ID):
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build("sheets", "v4", credentials=creds)

    garantir_cabecalhos(service, SPREADSHEET_ID)

    # Converta os dados para o formato necessário para o Google Sheets
    values = []
    for plataforma, dados_plataforma in dados:
        for dado in dados_plataforma:
            # Converter datetime para string no formato ISO
            linha = [str(item) if isinstance(item, datetime) else item for item in dado]
            values.append(linha)

    body = {"values": values}

    result = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption="RAW",
            body=body,
        )
        .execute()
    )

    print(f"{result.get('updates').get('updatedCells')} células atualizadas.")


if __name__ == "__main__":
    print("Gerando relatório e atualizando Google Sheets...")

    dados_youtube_api, dados_spotify_api, dados_deezer_api, dados_tiktok_api = (
        buscar_dados_semanal("API")
    )
    dados_youtube_nav, dados_spotify_nav, dados_deezer_nav, dados_tiktok_nav = (
        buscar_dados_semanal("Navegação")
    )

    dados_para_atualizar_api = [
        ("YouTube", dados_youtube_api),
        ("Spotify", dados_spotify_api),
        ("Deezer", dados_deezer_api),
        ("TikTok", dados_tiktok_api),
    ]
    dados_para_atualizar_nav = [
        ("YouTube", dados_youtube_nav),
        ("Spotify", dados_spotify_nav),
        ("Deezer", dados_deezer_nav),
        ("TikTok", dados_tiktok_nav),
    ]

    atualizar_google_sheets(dados_para_atualizar_api, data_select["API"])
    atualizar_google_sheets(dados_para_atualizar_nav, data_select["Navegação"])

    print(
        f"Relatório atualizado no Google Sheets com sucesso ás {datetime.now().strftime('%d-%m-%Y, %H:%M:%S')}"
    )


# Configurações de escopo e credenciais
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = "/content/audit-robot-423614-b59f224e5bd1.json"

# Carregar credenciais da conta de serviço
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Conectar-se ao serviço do Google Sheets
service = build("sheets", "v4", credentials=creds)

# IDs das planilhas (origem e destino)
SPREADSHEET_ID_ORIGEM = {
    "API": "19vyV0n_wwshYQU1Jz_W8LIR6mUE-GrV34-LtDesiQ3Y",
    "Navegação": "1iOeJtnc_TzU67WMP4JdKuUKBVVo7T2G48Gp_3lgxUR8",
}

SPREADSHEET_ID_DESTINO = "1tSl6BW2J14Lg_3xveJ-MqECeCEcUKuFxr2y_iAkwjd0"

# Nome da aba ou intervalo da planilha de origem
RANGE_ORIGEM = "Sheet1"  # Ou 'Sheet1!A1:C100' para um intervalo específico

# Nome da aba ou intervalo da planilha de destino
RANGE_DESTINO = "Sheet1"  # Ou 'Sheet1!A1' para começar a escrever a partir da célula A1


# Função para obter dados de uma planilha
def obter_dados(spreadsheet_id, range_name):
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=range_name)
        .execute()
    )
    return result.get("values", [])


# Passo 1: Obter os dados das duas planilhas de origem
dados_api = obter_dados(SPREADSHEET_ID_ORIGEM["API"], RANGE_ORIGEM)
dados_navegacao = obter_dados(SPREADSHEET_ID_ORIGEM["Navegação"], RANGE_ORIGEM)

# Verificar se há dados para transferir
if not dados_api and not dados_navegacao:
    print("Nenhum dado encontrado nas planilhas de origem.")
else:
    # Combinar os dados de ambas as planilhas
    dados_combinados = dados_api + dados_navegacao

    # Passo 2: Preencher a planilha de destino
    body = {"values": dados_combinados}  # Dados a serem escritos

    # Usando 'append' para adicionar os dados na planilha de destino
    result = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=SPREADSHEET_ID_DESTINO,
            range=RANGE_DESTINO,
            valueInputOption="RAW",  # Ou 'USER_ENTERED' se quiser interpretar fórmulas, por exemplo
            body=body,
        )
        .execute()
    )

    print(
        f"{result.get('updates', {}).get('updatedCells', 0)} células atualizadas na planilha de destino."
    )
