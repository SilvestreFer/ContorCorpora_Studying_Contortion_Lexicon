import requests
from bs4 import BeautifulSoup
import html2text
import os

# Function to download and save the text of an article
def save_article(url, destination_folder, filename):
    # Send a GET request to the article's URL
    response = requests.get(url)
    
    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Convert HTML content to plain text using html2text
    converter = html2text.HTML2Text()
    converter.ignore_links = True  # Removes hyperlinks, keeping only text content
    text = converter.handle(str(soup))
    
    # Create the destination folder if it doesn't already exist
    os.makedirs(destination_folder, exist_ok=True)
    
    # Define the full path to save the .txt file
    filepath = os.path.join(destination_folder, filename)
    
    # Save the text content into a UTF-8 encoded file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"✅ Article saved: {filename}")

# Main blog URL to scrape articles from
blog_url = "https://www.ashrexcircus.com/blog"

# Send a request to the blog page
response = requests.get(blog_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all hyperlinks (anchor tags with href attributes)
links = soup.find_all('a', href=True)
article_urls = []

# Filter valid blog post URLs
for link in links:
    href = link['href']
    # Look for internal blog links starting with /blog/
    if '/blog/' in href and href.startswith('/blog/'):
        full_url = "https://www.ashrexcircus.com" + href
        # Avoid duplicates
        if full_url not in article_urls:
            article_urls.append(full_url)

# Download and save all filtered articles
for i, url in enumerate(article_urls):
    save_article(url, 'ashrex_articles', f'ashrexcircus_{i+1}.txt')
