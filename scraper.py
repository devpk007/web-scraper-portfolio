"""
scraper.py — Extrai dados de produtos de um catálogo online e salva em CSV.

Site alvo: http://books.toscrape.com/
(site público, criado especificamente para prática de web scraping — sem
restrição de uso, ideal pra portfólio sem risco de violar termos de serviço)

Uso:
    python scraper.py
    python scraper.py --max-pages 5
    python scraper.py --output meus_dados.csv

O script percorre todas as páginas do catálogo (ou até --max-pages),
extrai título, preço, avaliação (estrelas) e disponibilidade de cada
produto, e salva tudo em um CSV pronto pra abrir no Excel.
"""

import argparse
import csv
import sys
import time

import requests
from bs4 import BeautifulSoup

BASE_URL = "http://books.toscrape.com/"
CATALOGUE_URL = "http://books.toscrape.com/catalogue/page-{}.html"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; PortfolioScraper/1.0)"}

# O site marca a nota em estrelas como uma classe CSS em texto por extenso
STAR_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def parse_page(html: str) -> list[dict]:
    """Extrai os dados de todos os produtos de uma página do catálogo."""
    soup = BeautifulSoup(html, "html.parser")
    products = []

    for item in soup.select("article.product_pod"):
        title = item.h3.a["title"].strip()

        price_text = item.select_one("p.price_color").text
        price = float(price_text.replace("£", "").strip())

        rating_class = item.select_one("p.star-rating")["class"]
        rating_word = [c for c in rating_class if c != "star-rating"][0]
        rating = STAR_MAP.get(rating_word, None)

        availability = item.select_one("p.instock.availability").text.strip()

        products.append(
            {
                "titulo": title,
                "preco_libras": price,
                "avaliacao_estrelas": rating,
                "disponibilidade": availability,
            }
        )

    return products


def scrape(max_pages: int | None = None) -> list[dict]:
    """Percorre as páginas do catálogo e junta todos os produtos."""
    all_products = []
    page = 1

    while True:
        if max_pages and page > max_pages:
            break

        url = CATALOGUE_URL.format(page)
        response = requests.get(url, headers=HEADERS, timeout=10)

        if response.status_code == 404:
            # chegou na última página
            break
        response.raise_for_status()

        page_products = parse_page(response.text)
        if not page_products:
            break

        all_products.extend(page_products)
        print(f"Página {page}: {len(page_products)} produtos coletados")

        page += 1
        time.sleep(0.5)  # educado com o servidor — evita sobrecarregar o site

    return all_products


def save_to_csv(products: list[dict], output_path: str) -> None:
    if not products:
        print("Nenhum produto encontrado, nada foi salvo.")
        return

    fieldnames = list(products[0].keys())
    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)

    print(f"\n{len(products)} produtos salvos em {output_path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-pages", type=int, default=None,
                         help="Número máximo de páginas a percorrer (padrão: todas)")
    parser.add_argument("--output", type=str, default="produtos.csv",
                         help="Nome do arquivo CSV de saída")
    args = parser.parse_args()

    try:
        products = scrape(max_pages=args.max_pages)
        save_to_csv(products, args.output)
    except requests.RequestException as e:
        print(f"Erro de conexão: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
