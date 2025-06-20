import requests
from bs4 import BeautifulSoup
import os
import re

urls = [
    "https://www.catiebrier.com/post/what-to-do-with-your-glutes-in-backbends",
    "https://www.catiebrier.com/post/dizziness-in-backbends-causes-and-solutions",
    "https://www.catiebrier.com/post/the-difference-between-training-flexibility-and-training-tricks-and-how-to-reach-your-bendy-goals",
    "https://www.catiebrier.com/post/why-your-shoulders-hurt-when-you-stretch-and-how-to-fix-it",
    "https://www.catiebrier.com/post/3-tips-to-fix-your-middle-split",
    "https://www.catiebrier.com/post/student-case-study-ep-2-david",
    "https://www.catiebrier.com/post/why-the-f-do-i-need-to-square-my-splits-part-deux",
    "https://www.catiebrier.com/post/student-case-study-ep-1-ines",
    "https://www.catiebrier.com/post/painful-stretching-what-is-means-and-why-we-don-t-play-that-game",
    "https://www.catiebrier.com/post/flexing-feet-pike-stretches-and-nerve-tension-oh-my",
    "https://www.catiebrier.com/post/the-difference-between-contortion-and-flexibility",
    "https://www.catiebrier.com/post/low-back-pain-and-how-to-avoid-it",
    "https://www.catiebrier.com/post/why-you-re-not-getting-more-flexible",
    "https://www.catiebrier.com/post/notyoga-explained",
    "https://www.catiebrier.com/post/how-long-will-it-take-to-learn-the-splits",
    "https://www.catiebrier.com/post/why-the-f-do-i-need-to-square-my-splits",
    "https://www.catiebrier.com/post/why-you-should-never-stretch-passively",
    "https://www.catiebrier.com/post/how-often-should-you-stretch"
]

folder_name = "catiebrier_articles"
os.makedirs(folder_name, exist_ok=True)

def article_name(title):
    return re.sub(r'[^\w\s-]', '', title).strip().lower().replace(' ', '_')

for url in urls:
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Título
        title_tag = soup.find('h1')
        title = title_tag.get_text(strip=True) if title_tag else "sem_titulo"

        # Conteúdo principal
        article_body = soup.find('div', class_='sqs-block-content')
        if not article_body:
            article_body = soup.find('article')  # fallback

        paragraphs = article_body.find_all(['p', 'h2', 'h3', 'ul', 'ol']) if article_body else []
        content = f"# {title}\n\n"
        for p in paragraphs:
            content += p.get_text(strip=True) + "\n\n"

        # Salva como .txt
        filename = f"{article_name(title)}.txt"
        filepath = os.path.join(folder_name, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Artigo salvo: {filename}")

    except Exception as e:
        print(f"Erro ao processar {url}: {e}")
