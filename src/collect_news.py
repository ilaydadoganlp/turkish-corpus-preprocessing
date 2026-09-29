import json
import requests
import time
from bs4 import BeautifulSoup

def extract_article_text(url):
    response = requests.get(url, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    article = soup.find("article")
    if article is None:
        raise ValueError("Article elementi bulunamadı.")

    cms = article.find("div", class_="cms-container")
    if cms is None:
        raise ValueError("cms-container bulunamadı.")

    for ad in cms.find_all(class_="adv-news"):
        ad.decompose()

    for reklam in cms.find_all(string=lambda text: text and text.strip() == "REKLAM"):
        wrapper = reklam.parent.parent.parent

        if wrapper.find(attrs={"data-adv": "hbrtrk"}):
            wrapper.decompose()

    return cms.get_text(" ", strip=True)

def extract_rss_items(rss_url, source_category):
    response = requests.get(rss_url, timeout=15)
    response.raise_for_status()

    rss_soup = BeautifulSoup(response.content, "xml")
    items = rss_soup.find_all("item")

    records = []
    failed_count = 0

    for index, item in enumerate(items, start=1):
        record = {
            "corpus_type": "news",
            "source": "Habertürk",
            "source_category": source_category,
            "title": item.find("title").get_text(strip=True),
            "description": item.find("description").get_text(strip=True),
            "publication_date": item.find("pubDate").get_text(strip=True),
            "url": item.find("link").get_text(strip=True),
        }

        try:
            record["text"] = extract_article_text(record["url"])
            records.append(record)
            print(f"[{source_category}] {index}/{len(items)} işlendi")
            time.sleep(1)
        except (requests.RequestException, ValueError) as error:
            failed_count += 1
            print(f"Haber atlandı: {record['url']}")
            print(f"Sebebi: {error}")

    print(
        f"[{source_category}] RSS item: {len(items)} | "
        f"başarılı: {len(records)} | "
        f"atlanan: {failed_count}"
    )

    return records

feeds = [
    {
        "url": "https://www.haberturk.com/rss/kategori/teknoloji.xml",
        "source_category": "teknoloji",
    },
    {
        "url": "https://www.haberturk.com/rss/kategori/gundem.xml",
        "source_category": "gundem",
    },
    {
        "url": "https://www.haberturk.com/rss/ekonomi.xml",
        "source_category": "ekonomi",
    },
]

def main():
    total_successful_records = 0
    records_by_url = {}

    for feed in feeds:
        records = extract_rss_items(
            feed["url"],
            feed["source_category"]
        )

        total_successful_records += len(records)

        for record in records:
            url = record["url"]

            if url not in records_by_url:
                record["source_category"] = [record["source_category"]]
                records_by_url[url] = record
            else:
                category = record["source_category"]

                if category not in records_by_url[url]["source_category"]:
                    records_by_url[url]["source_category"].append(category)

    all_records = list(records_by_url.values())

    duplicate_count = total_successful_records - len(all_records)

    print(f"Toplam başarılı RSS kaydı: {total_successful_records}")
    print(f"Benzersiz haber: {len(all_records)}")
    print(f"Birleştirilen çift kayıt: {duplicate_count}")

    with open("data/raw/news.jsonl", "w", encoding="utf-8") as file:
        for record in all_records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()
