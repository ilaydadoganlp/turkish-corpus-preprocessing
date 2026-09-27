import requests
import re
import json
from bs4 import BeautifulSoup

def is_heading(paragraph):
    paragraph_text = paragraph.get_text(" ", strip=True)

    bold_text = " ".join(
        bold.get_text(" ", strip=True)
        for bold in paragraph.find_all("b")
    )

    return bool(paragraph_text) and paragraph_text == bold_text

laws = [
    {
        "url": "https://tbmm.gov.tr/Yasama/Kanun/f72877c0-958d-037b-e050-007f01005610",
        "domain": "mixed"
    },
    {
        "url": "https://www.tbmm.gov.tr/Yasama/Kanun/af1dfbdb-e3e3-4820-a493-0194504c63b4",
        "domain": "cybersecurity"
    }
    ]

articles = []

for law in laws:
    url = law["url"]
    domain = law["domain"]

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    label = soup.find(string=lambda text: text and text.strip() == "Kanun Numarası")
    row = label.find_parent("tr")
    cells = row.find_all("td")

    law_number = int(cells[1].get_text(strip=True))

    title_label = soup.find(string=lambda text: text and text.strip() == "Başlığı")
    title_row = title_label.find_parent("tr")
    title_cells = title_row.find_all("td")

    law_title = title_cells[1].get_text(strip=True)

    date_label = soup.find(
        string=lambda text: text and text.strip() == "Resmi Gazete Tarihi"
    )
    date_row = date_label.find_parent("tr")
    date_cells = date_row.find_all("td")
    publication_date = date_cells[1].get_text(strip=True)

    law_text_element = soup.find(
        string=lambda text: text and "Kanun Metni" in text
    )

    if law_text_element is None:
        raise ValueError("Kanun metni bağlantısı bulunamadı.")

    law_text_url = law_text_element.parent.get("href")
    if not law_text_url:
        raise ValueError("Kanun metni URL'i bulunamadı.")

    law_response = requests.get(law_text_url, timeout=30)
    law_response.raise_for_status()

    law_response.encoding = "Windows-1254"
    law_soup = BeautifulSoup(law_response.text, "html.parser")

    article_candidates = law_soup.find_all(
        string=lambda text: text and text.strip().startswith("MADDE")
    )
    if not article_candidates:
        raise ValueError("Kanun metninde madde başlangıcı bulunamadı.")

    for article in article_candidates:
        paragraph = article.find_parent("p")
        text = paragraph.get_text(separator=" ", strip=True)
        text = " ".join(text.split())
        next_paragraph = paragraph.find_next_sibling("p")

        while next_paragraph:
            next_text = next_paragraph.get_text(separator=" ", strip=True)
            next_text = " ".join(next_text.split())

            if next_text.startswith("MADDE"):
                break

            if is_heading(next_paragraph):
                next_paragraph = next_paragraph.find_next_sibling("p")
                continue

            if next_text:
                text += " " + next_text

            next_paragraph = next_paragraph.find_next_sibling("p")

        match = re.match(r"^MADDE (\d+)-\s*(.*)", text)

        if match is None:
            raise ValueError(f"Madde yapısı çözümlenemedi: {text[:100]}")

        article_number = int(match.group(1))
        article_text = match.group(2)

        articles.append({
            "corpus_type": "legal",
            "source": "TBMM",
            "law_number": law_number,
            "law_title": law_title,
            "publication_date": publication_date,
            "domain": domain,
            "article_number": article_number,
            "text": article_text
        })

with open("data/raw/legal.jsonl", "w", encoding="utf-8") as file:
    for article in articles:
        file.write(json.dumps(article, ensure_ascii=False) + "\n")