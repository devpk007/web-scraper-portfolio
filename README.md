# Web Scraper de Catálogo de Produtos

Script em Python que extrai título, preço, avaliação e disponibilidade de
produtos de um catálogo online, com paginação automática, e salva tudo em CSV.

## Por que esse projeto pro portfólio

Esse é exatamente o tipo de pedido mais comum em freelas de web scraping no
Workana: "extrai os dados de [X] produtos de um site pra planilha". O script
mostra:

- Paginação automática (percorre o catálogo inteiro sozinho)
- Tratamento de erro de conexão
- Delay entre requisições (não sobrecarrega o servidor — boa prática)
- Saída em CSV pronta pra abrir no Excel
- Código comentado e organizado em funções reutilizáveis

## Como rodar

```bash
pip install -r requirements.txt
python scraper.py                          # todas as páginas
python scraper.py --max-pages 5             # só as 5 primeiras páginas
python scraper.py --output livros.csv       # nome customizado do CSV
```

## Testes

A lógica de extração (`parse_page`) foi validada com HTML de amostra
reproduzindo a estrutura real do site (`sample_page.html`), sem depender
de conexão de rede pra confirmar que o parsing está correto:

```bash
python3 -c "
from scraper import parse_page
html = open('sample_page.html').read()
for p in parse_page(html):
    print(p)
"
```

## Adaptando pra outro site

Pra usar em outro projeto, troca:
1. `BASE_URL` e `CATALOGUE_URL` pela URL do site alvo
2. Os seletores CSS dentro de `parse_page()` pela estrutura HTML do site alvo
   (inspeciona o site com F12 no navegador pra achar as classes certas)

## Stack

Python · requests · BeautifulSoup4
