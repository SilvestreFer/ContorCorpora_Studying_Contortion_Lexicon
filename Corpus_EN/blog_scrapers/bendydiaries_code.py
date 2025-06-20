import requests
from bs4 import BeautifulSoup
import time
import os

BASE_URL = "https://bendydiaries.wordpress.com"
POSTS_PER_PAGE = 10  # típico WordPress
OUTPUT_FOLDER = "bendy_diaries_articles"
DELAY_BETWEEN_REQUESTS = 2  # segundos para respeitar o site

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def get_posts_links(page_num):
    url = f"{BASE_URL}/page/{page_num}/"
    print(f"🔎 Pegando links da página {page_num}: {url}")
    resp = requests.get(url)
    if resp.status_code != 200:
        print(f"⚠️ Não foi possível acessar a página {page_num}")
        return []
    soup = BeautifulSoup(resp.text, "html.parser")

    # Os posts ficam dentro de article.post ou similar
    posts = soup.find_all("article")
    links = []
    for post in posts:
        a = post.find("a", href=True)
        if a:
            href = a['href']
            if href.startswith(BASE_URL):
                links.append(href)
            else:
                links.append(BASE_URL + href)
    return links

def download_post(url):
    print(f"📄 Baixando artigo: {url}")
    resp = requests.get(url)
    if resp.status_code != 200:
        print(f"⚠️ Erro ao acessar o artigo: {url}")
        return None
    soup = BeautifulSoup(resp.text, "html.parser")

    # Pega o título
    title_tag = soup.find("h1", class_="entry-title")
    title = title_tag.text.strip() if title_tag else "Sem título"

    # Pega o conteúdo do post (geralmente dentro de div.entry-content)
    content_div = soup.find("div", class_="entry-content")
    if not content_div:
        print(f"⚠️ Conteúdo não encontrado no artigo: {url}")
        return None

    paragraphs = content_div.find_all("p")
    text = "\n\n".join(p.get_text(strip=True) for p in paragraphs)

    return title, text

def save_article(title, text, index):
    safe_title = "".join(c for c in title if c.isalnum() or c in " _-").rstrip()
    filename = os.path.join(OUTPUT_FOLDER, f"{index:03d}_{safe_title}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(title + "\n\n" + text)
    print(f"✅ Salvo: {filename}")

def main():
    all_links = []
    page_num = 1
    while True:
        links = get_posts_links(page_num)
        if not links:
            print("🚫 Nenhum artigo encontrado. Finalizando.")
            break
        all_links.extend(links)
        page_num += 1
        time.sleep(DELAY_BETWEEN_REQUESTS)

    print(f"\n🔖 Total de artigos coletados: {len(all_links)}")

    for i, link in enumerate(all_links, 1):
        result = download_post(link)
        if result:
            title, text = result
            save_article(title, text, i)
        time.sleep(DELAY_BETWEEN_REQUESTS)

    print("\n🏁 Todos os artigos foram baixados e salvos.")

if __name__ == "__main__":
    main()
