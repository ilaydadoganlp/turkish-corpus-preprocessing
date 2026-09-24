import requests
import re
from bs4 import BeautifulSoup

url = "https://tbmm.gov.tr/Yasama/Kanun/16814ed0-898a-4315-8025-019fc7efdcdf"

response = requests.get(url, timeout=30)

soup = BeautifulSoup(response.text, "html.parser")

law_text_element = soup.find(
    string=lambda text: text and "Kanun Metni" in text
)

law_text_url = law_text_element.parent.get("href")
law_response = requests.get(law_text_url, timeout=30)

law_response.encoding = "Windows-1254"
law_soup = BeautifulSoup(law_response.text, "html.parser")

article_candidates = law_soup.find_all(
    string=lambda text: text and text.strip().startswith("MADDE")
)

articles = []

for article in article_candidates:
    paragraph = article.find_parent("p")
    text = paragraph.get_text(separator=" ", strip=True)
    text = " ".join(text.split())

    match = re.match(r"^MADDE (\d+)-\s*(.*)", text)

    article_number = int(match.group(1))
    article_text = match.group(2)

    articles.append({
        "article_number": article_number,
        "text": article_text
    })

print(articles)