import requests
from bs4 import BeautifulSoup
import html2text
import os

# Função para baixar e salvar texto de um artigo
def salvar_artigo(url, pasta_destino, nome_arquivo):
    resposta = requests.get(url)
    soup = BeautifulSoup(resposta.text, 'html.parser')

    # Converte o HTML para texto
    h = html2text.HTML2Text()
    h.ignore_links = True
    texto = h.handle(str(soup))

    # Cria a pasta se não existir
    os.makedirs(pasta_destino, exist_ok=True)

    # Salva o texto num arquivo .txt
    caminho = os.path.join(pasta_destino, nome_arquivo)
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(texto)

    print(f"✅ Artigo salvo: {nome_arquivo}")

# URL principal do blog
url_blog = "https://www.ashrexcircus.com/blog"
resposta = requests.get(url_blog)
soup = BeautifulSoup(resposta.text, 'html.parser')

# Encontra os links dos artigos
links = soup.find_all('a', href=True)
urls_artigos = []

for link in links:
    href = link['href']
    if '/blog/' in href and href.startswith('/blog/'):
        url_completa = "https://www.ashrexcircus.com" + href
        if url_completa not in urls_artigos:
            urls_artigos.append(url_completa)

# Baixa e salva os artigos
for i, url in enumerate(urls_artigos):
    salvar_artigo(url, 'artigos_ashrex', f'ashrexcircus_{i+1}.txt')
