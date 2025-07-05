import time
from playwright.sync_api import sync_playwright

from salvar_dados import carregar_dados_sessao

artists = {"gino e geno": "@ginoegenooficial"}
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"


def fetch_artist(artist, target_videos_count=10):
    """Busca pela quantidade de views em determinado perfil(`artist`), com `target_videos_count` sendo seu limite de videos procurados

    Args:
        artist (str): @nome_do_perfil para encontra-lo no tiktok
        target_videos_count (int, optional): quantidade de videos alvos para procurar no perfil. Defaults to 10.

    Returns:
        views (list): lista com a quantidade de views
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        contexto = browser.new_context()

        # Carrega os dados da sessão
        carregar_dados_sessao(contexto, "sessao.json")

        # Abre uma nova página com os dados da sessão carregados
        pg = contexto.new_page()
        # pg = browser.new_page()
        pg.goto(f"https://www.tiktok.com/{artist}")
        time.sleep(30)
        tag_videos = ".css-1uqux2o-DivItemContainerV2.e19c29qe8"
        lista_de_videos = pg.query_selector_all(tag_videos)
        print("videos encontrados", len(lista_de_videos))
        if len(lista_de_videos) > 0:
            views = []
            for i, video in enumerate(lista_de_videos):
                x = f"#main-content-others_homepage > div > div.css-833rgq-DivShareLayoutMain.ee7zj8d4 > div.css-1qb12g8-DivThreeColumnContainer.eegew6e2 > div > div:nth-child({i + 1}) > div > div > div > a > div > div.css-11u47i-DivCardFooter.e148ts220 > strong"

                text = pg.locator(
                    x,
                ).inner_text()
                views.append(text)
                if i >= target_videos_count:
                    break

            return views


fetch_artist(artists.get("gino e geno"))
