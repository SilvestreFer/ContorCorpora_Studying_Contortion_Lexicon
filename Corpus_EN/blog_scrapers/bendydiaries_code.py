import requests
from bs4 import BeautifulSoup
import time
import os

# Base URL of the WordPress blog
BASE_URL = "https://bendydiaries.wordpress.com"
# Approximate number of posts displayed per blog page
POSTS_PER_PAGE = 10
# Directory to store the downloaded articles
OUTPUT_FOLDER = "bendy_diaries_articles"
# Delay (in seconds) between each HTTP request to avoid overloading the server
DELAY_BETWEEN_REQUESTS = 2

# Create output folder if it doesn't exist
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Function to extract all blog post links from a specific page number
def get_posts_links(page_num):
    url = f"{BASE_URL}/page/{page_num}/"
    print(f"🔎 Fetching post links from page {page_num}: {url}")
    resp = requests.get(url)
    
    # If the request fails, skip this page
    if resp.status_code != 200:
        print(f"⚠️ Could not access page {page_num}")
        return []

    # Parse HTML content
    soup = BeautifulSoup(resp.text, "html.parser")

    # Posts are usually contained within <article> tags
    posts = soup.find_all("article")
    links = []

    # For each post, find the first anchor tag and extract the href
    for post in posts:
        a = post.find("a", href=True)
        if a:
            href = a['href']
            # Ensure the full URL is constructed correctly
            if href.startswith(BASE_URL):
                links.append(href)
            else:
                links.append(BASE_URL + href)
    
    return links

# Function to download the contents of a single blog post
def download_post(url):
    print(f"📄 Downloading article: {url}")
    resp = requests.get(url)

    # If the request fails, return nothing
    if resp.status_code != 200:
        print(f"⚠️ Error accessing the article: {url}")
        return None

    # Parse HTML content
    soup = BeautifulSoup(resp.text, "html.parser")

    # Extract the title from <h1 class="entry-title">
    title_tag = soup.find("h1", class_="entry-title")
    title = title_tag.text.strip() if title_tag else "Untitled"

    # Extract the main content from <div class="entry-content">
    content_div = soup.find("div", class_="entry-content")
    if not content_div:
        print(f"⚠️ Content not found in article: {url}")
        return None

    # Extract text from all paragraphs within the content div
    paragraphs = content_div.find_all("p")
    text = "\n\n".join(p.get_text(strip=True) for p in paragraphs)

    return title, text

# Function to save an article as a .txt file
def save_article(title, text, index):
    # Make a safe filename from the title (alphanumeric + some punctuation)
    safe_title = "".join(c for c in title if c.isalnum() or c in " _-").rstrip()
    filename = os.path.join(OUTPUT_FOLDER, f"{index:03d}_{safe_title}.txt")

    # Write title and content to the file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(title + "\n\n" + text)
    
    print(f"✅ Saved: {filename}")

# Main execution flow
def main():
    all_links = []
    page_num = 1

    # Loop through paginated blog pages until no more posts are found
    while True:
        links = get_posts_links(page_num)
        if not links:
            print("🚫 No more articles found. Stopping.")
            break
        all_links.extend(links)
        page_num += 1
        time.sleep(DELAY_BETWEEN_REQUESTS)  # Wait between requests to be polite to the server

    print(f"\n🔖 Total articles collected: {len(all_links)}")

    # Download and save each article
    for i, link in enumerate(all_links, 1):
        result = download_post(link)
        if result:
            title, text = result
            save_article(title, text, i)
        time.sleep(DELAY_BETWEEN_REQUESTS)  # Wait again to avoid server overload

    print("\n🏁 All articles have been downloaded and saved.")

# Entry point
if __name__ == "__main__":
    main()
