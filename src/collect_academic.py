import requests
import pymupdf

PDF_URL = "https://www.dilbilimdernegi.org/wp-content/uploads/2021/04/30.-Ulusal-Dilbilim-Kurultayi-Bildirileri.pdf"

def download_pdf(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.content

def open_pdf(pdf_bytes):
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    return doc

def extract_page_text(doc, page_number):
    text = doc[page_number].get_text()
    return text

def main():
    pdf_bytes = download_pdf(PDF_URL)
    doc = open_pdf(pdf_bytes)
    page_text = extract_page_text(doc, 19)
    print(f"PDF boyutu: {len(pdf_bytes)} bytes")
    print("Test edilen PDF sayfası: 20")
    print(f"PDF'teki toplam sayfa sayısı: {len(doc)}")
    print(f"Çıkarılan karakter sayısı: {len(page_text)}")

    if page_text.strip():
        print("Text extraction: OK")
    else:
        print("Text extraction: FAILED")

    print("\n--- SAMPLE ---")
    print(page_text[:2000])

if __name__ == "__main__":
    main()
