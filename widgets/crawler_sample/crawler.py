import os
import requests
import certifi
from requests.exceptions import SSLError
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter

from dotenv import load_dotenv
from utils.logger_adapter import get_logger

log = get_logger()

# Carrega variáveis de ambiente
BASE_DIR = os.path.dirname(__file__)
dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path)

# URL base e API do backend
UOL_URL = "https://www.uol.com.br/"
API_URL = os.getenv("WIDGET_CRAWLER_API_URL")
if not API_URL:
    raise RuntimeError("WIDGET_CRAWLER_API_URL não configurada no .env")


def get_noticias_urls() -> list[str]:
    """Coleta todos os links de notícias do UOL."""
    try:
        response = requests.get(UOL_URL, timeout=10)
        response.raise_for_status()
    except Exception as e:
        log.error(f"Erro ao buscar página principal: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a", href=True)
    noticias = set()

    for link in links:
        href = urljoin(UOL_URL, link["href"])
        if ("/noticias/" in href or "uol.com.br" in href) and href.startswith("http"):
            noticias.add(href.split("?")[0])

    return list(noticias)


def get_conteudo_noticia(url: str) -> str | None:
    """Extrai título e parágrafos de uma notícia."""
    try:
        r = requests.get(url, verify=certifi.where(), timeout=5)
        r.raise_for_status()
    except SSLError:
        log.error(f"Ignorado SSLError para {url}")
        return None
    except Exception as e:
        log.error(f"Erro ao processar {url}: {e}")
        return None

    try:
        soup = BeautifulSoup(r.text, "html.parser")
        titulo = soup.find("h1").text.strip() if soup.find("h1") else ""
        paragrafos = [p.text.strip() for p in soup.find_all("p") if p.text.strip()]
        return f"{titulo}\n\n" + "\n".join(paragrafos)
    except Exception as e:
        log.error(f"Erro ao extrair conteúdo de {url}: {e}")
        return None


def popular_vector_db(noticias: list[str]) -> None:
    """
    Chunka cada notícia e envia ao backend via HTTP.
    Espera que o endpoint /ingest/stream receba:
    { collection_name, content, metadata }
    """
    collection_name = os.getenv("WIDGET_CRAWLER_COLLECTION_NAME", "crawler_sample")

    # Coleta textos e metadados
    chunks = []
    for url in noticias:
        texto = get_conteudo_noticia(url)
        if texto:
            chunks.append((texto, {"url": url}))

    if not chunks:
        log.warning("Nenhum documento para ingerir.")
        return

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.create_documents(
        [t for t, _ in chunks],
        metadatas=[m for _, m in chunks],
    )

    total = len(docs)
    for idx, doc in enumerate(docs, start=1):
        payload = {
            "collection_name": collection_name,
            "content": doc.page_content,
            "metadata": doc.metadata,
        }
        try:
            resp = requests.post(
                API_URL,
                json=payload,
                timeout=10,
                headers={"Content-Type": "application/json", "Accept": "application/json"},
            )
            resp.raise_for_status()
            log.info(f"→ ({idx}/{total}) enviado com sucesso: {doc.metadata.get('url')}")
        except Exception as e:
            log.error(f"→ Erro ao enviar documento ({idx}/{total}): {e}")


def count_items_in_collection(collection_name: str) -> None:
    """Opcional: chamar backend para contar itens (se exposto)."""
    url = os.getenv("WIDGET_CRAWLER_API_URL", "")
    if not url:
        return
    try:
        resp = requests.get(f"{url}?collection_name={collection_name}", timeout=5)
        resp.raise_for_status()
        total = resp.json().get("count", 0)
        log.success(f"🔥 Total de documentos em '{collection_name}': {total}")
    except Exception as e:
        log.error(f"Erro ao contar itens na coleção via API: {e}")


if __name__ == "__main__":
    collection_name = os.getenv("WIDGET_CRAWLER_COLLECTION_NAME", "langchain")
    log.success(f"Inicializando crawler para a coleção '{collection_name}'")

    urls = get_noticias_urls()
    log.info(f"Encontradas {len(urls)} URLs de notícias")
    popular_vector_db(urls)

    log.success("Crawler finalizado com sucesso!")
