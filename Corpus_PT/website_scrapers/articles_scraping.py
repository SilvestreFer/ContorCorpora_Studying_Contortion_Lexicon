import os
import requests
from bs4 import BeautifulSoup

# List of URLs
urls = [
    "https://holoart.com.br/contor-lab/",
    "https://omenorespetaculodaterra.blogspot.com/2010/05/contorcionista-o-contorcionismo-ou.html",
    "https://circodelalunacontagem.blogspot.com/",
    "https://mulher-borracha.blogspot.com/2014/03/mega-post-karine-almeida.html",
    "https://a-arte-que-vem-do-circo.blogspot.com/2014/06/a-vida-de-uma-contorcionista.html",
    "https://dominiquemartins.wordpress.com/"
]

# Directory to store the text files
output_dir = "../articles"
os.makedirs(output_dir, exist_ok=True)

# Function to extract and clean text
def extract_text(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove scripts and styles
        for script_or_style in soup(["script", "style", "noscript"]):
            script_or_style.decompose()

        # Extract visible text
        text = soup.get_text(separator="\n")
        cleaned_lines = [line.strip() for line in text.splitlines() if line.strip()]
        cleaned_text = "\n".join(cleaned_lines)

        return cleaned_text
    except Exception as e:
        print(f"Error extracting {url}: {e}")
        return ""

# Process each URL
for idx, url in enumerate(urls, start=1):
    text = extract_text(url)
    if text:
        file_name = f"text_{idx}.txt"
        with open(os.path.join(output_dir, file_name), "w", encoding="utf-8") as f:
            f.write(f"URL: {url}\n\n")
            f.write(text)

print("Text extraction complete. Files saved in the 'articles/' folder.")
