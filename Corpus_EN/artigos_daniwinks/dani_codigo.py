from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

BASE_URL = "https://www.daniwinksflexibility.com"
BLOG_URL = BASE_URL + "/bendy-blog"

# Configurações para rodar o Chrome sem abrir janela (headless)
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)

def pegar_links_artigos():
    driver.get(BLOG_URL)
    time.sleep(3)  # espera carregar o conteúdo JS

    # Scroll para baixo para carregar todos os posts (se tiver lazy load)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    links = set()
    # Pega todos os links que têm a classe 'blog-more-link' (botão Read More)
    elementos = driver.find_elements(By.CSS_SELECTOR, "a.blog-more-link")
    for elem in elementos:
        href = elem.get_attribute('href')
        if href and "/bendy-blog/" in href and "/category/" not in href:
            links.add(href)

    print(f"➡️ {len(links)} links de artigos encontrados.")
    return list(links)

def baixar_texto_artigo(url):
    driver.get(url)
    time.sleep(3)  # espera carregar o artigo

    try:
        content = driver.find_element(By.CSS_SELECTOR, "div.blog-post-content")
        texto = content.text
        return texto
    except:
        print(f"⚠️ Conteúdo não encontrado no artigo: {url}")
        return None

def salvar_artigo(texto, url):
    slug = url.rstrip('/').split('/')[-1]
    nome_arquivo = f"{slug}.txt"
    os.makedirs("artigos_daniwinks", exist_ok=True)
    caminho = os.path.join("artigos_daniwinks", nome_arquivo)
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(texto)
    print(f"✅ Artigo salvo em: {caminho}")

def main():
    try:
        links = pegar_links_artigos()

        print("\n=== Iniciando download dos artigos ===\n")
        for i, link in enumerate(links, 1):
            print(f"🔄 [{i}/{len(links)}] Processando {link}")
            texto = baixar_texto_artigo(link)
            if texto:
                salvar_artigo(texto, link)
            time.sleep(1)

        print("\n🏁 Todos os artigos foram baixados e salvos.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
