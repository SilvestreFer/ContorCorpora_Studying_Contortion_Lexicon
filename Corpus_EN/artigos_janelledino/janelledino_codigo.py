import requests
from bs4 import BeautifulSoup
import html2text
import os

def salvar_artigo(url, pasta_destino, nome_arquivo):
    resposta = requests.get(url)
    soup = BeautifulSoup(resposta.text, 'html.parser')

    h = html2text.HTML2Text()
    h.ignore_links = True
    texto = h.handle(str(soup))

    os.makedirs(pasta_destino, exist_ok=True)
    caminho = os.path.join(pasta_destino, nome_arquivo)
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(texto)

    print(f"✅ Artigo salvo: {nome_arquivo}")

# Artigo único do site
url = "https://janelledinosaurs.com/blog-1/2018/9/10/notyoga-notstretching-what-contortion-is-and-isnt"
salvar_artigo(url, "artigos_janelledino", "notyoga_notstretching.txt")
