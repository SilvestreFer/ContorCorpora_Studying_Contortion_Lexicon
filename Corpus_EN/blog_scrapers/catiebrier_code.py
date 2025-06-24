import requests
from bs4 import BeautifulSoup
import os
import re

# List of blog post URLs to be scraped
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

# Folder to save the downloaded articles
folder_name = "catiebrier_articles"
os.makedirs(folder_name, exist_ok=True)

# Function to create a safe filename from the article title
def article_name(title):
    # Removes special characters and replaces spaces with underscores
    return re.sub(r'[^\w\s-]', '', title).strip().lower().replace(' ', '_')

# Loop over all URLs to download and save each article
for url in urls:
    # Make the HTTP request to the article page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the article title (usually inside an <h1> tag)
    title_tag = soup.find('h1')
    title = title_tag.get_text(strip=True) if title_tag else "untitled"

    # Find the main content area (typically in a div with class 'sqs-block-content')
    article_body = soup.find('div', class_='sqs-block-content')
    if not article_body:
        # Fallback in case the main div is not found
        article_body = soup.find('article')

    # Extract paragraphs and other relevant tags
    paragraphs = article_body.find_all(['p', 'h2', 'h3', 'ul', 'ol']) if article_body else []
    content = f"# {title}\n\n"
    for p in paragraphs:
        content += p.get_text(strip=True) + "\n\n"

    # Generate a filename and save the content to a .txt file
    filename = f"{article_name(title)}.txt"
    filepath = os.path.join(folder_name, filename)

    f = open(filepath, "w", encoding="utf-8")
    f.write(content)
    f.close()

    print(f"Article saved: {filename}")
