import requests
import pymupdf
import json

PDF_URL = "https://www.dilbilimdernegi.org/wp-content/uploads/2021/04/30.-Ulusal-Dilbilim-Kurultayi-Bildirileri.pdf"
ACADEMIC_CONTENT_END_PAGE = 352
PAPERS = [
    {
        "title": "Korku Kültürü İle İlgili Türkçe Sözcüklerin Derlem Temelli İncelenmesi",
        "authors": ["Özlem Kurtoğlu Zorlu"],
        "start_page": 53,
    },
    {
        "title": "Türkçede Yer, Yönelim ve Hareket Tarzının Kodlanması",
        "authors": ["Engin Arık"],
        "start_page": 61,
    },
    {
        "title": "Türkçe Deyimlerde Göz Sözcüğünün Kavramsallaştırılması",
        "authors": ["Melike Baş"],
        "start_page": 69,
    },
    {
        "title": "Türkçe Sosyal Bilimler Metinlerindeki Savlarda Kullanılan Kavramsal Metaforlar",
        "authors": ["Elif Arıca-Akkök", "Gülsün Leyla Uzun"],
        "start_page": 77,
    },
    {
        "title": "Fonolojik Farkındalık ve Sözcük Bilgisinin Yazma Becerisi Üzerindeki Etkisi",
        "authors": ["Ecehan Sönmez", "Belma Haznedar", "Nalan Babür"],
        "start_page": 85,
    },
    {
        "title": "Seçim Propaganda Konuşmalarının Söylemsel Stratejiler Çerçevesinde İncelenmesi",
        "authors": ["Kübra Karaca"],
        "start_page": 93,
    },
    {
        "title": "Siyasi Söylemlerde Canlı Bir Varlık Olarak Türkiye",
        "authors": ["Esranur Efeoğlu", "Hale Işık-Güler"],
        "start_page": 103,
    },
    {
        "title": "Tek Heceli Türkçe Sözcüklerin Üç Boyutlu Analizi: “Ses-görselleri” ya da “Sesin haritası”",
        "authors": ["Yusuf Kemal Kemaloğlu", "Güven Mengü"],
        "start_page": 111,
    },
    {
        "title": "Kaçınsama ve Vurgulayıcı Dilsel Öğeler",
        "authors": ["Elçin Esmer"],
        "start_page": 119,
    },
    {
        "title": "Türkçe Söylem Yapısında Boş Nesne",
        "authors": ["Aytaç Çeltek", "Lütfiye Oktar"],
        "start_page": 125,
    },
    {
        "title": "Türkçede Olumsuz Zayıf Bilgisel Kiplik Yapılarının Edinimi",
        "authors": ["Melike Hendek"],
        "start_page": 133,
    },
    {
        "title": "Türkçe Bileşik Sözcüklerin Biçimbirimsel Olarak İşlemlenmesi",
        "authors": ["Serkan Uygun", "Ayşe Gürel"],
        "start_page": 139,
    },
    {
        "title": "Türkçede [gibi + Öznesiz Yüklem] Yapıları",
        "authors": ["Halil İskender", "Tacettin Turgay"],
        "start_page": 147,
    },
    {
        "title": "Değerlendirme Kuramı Açısından Yaş Kimliği",
        "authors": ["Nazlı Baykal"],
        "start_page": 155,
    },
    {
        "title": "Yabancı Dil Öğretimi Kitaplarında Eşdizimli Sözcüklerin Sunumu",
        "authors": ["Meltem Ayabakan", "Nursel Tan Elmas"],
        "start_page": 163,
    },
    {
        "title": "Ortaokul Öğrencilerinin Ürettikleri Tartışmacı Metinlerde Bağdaşıklık, Tutarlılık",
        "authors": ["Seda Gülsüm Gökmen", "Nilay Çağlayan Dilber"],
        "start_page": 169,
    },
    {
        "title": "İkinci Dil Olarak İngilizcede İlgi Tümceciklerini İliştirme Tercihleri",
        "authors": ["Tuğba Aydın Yıldız", "Filiz Çele"],
        "start_page": 179,
    },
    {
        "title": "Eşdizimliliklerde Seçim Sınırlamaları",
        "authors": ["Selma Elyıldırım"],
        "start_page": 187,
    },
    {
        "title": "Deneyimin Soyut ve Somut Kelimelerin İşlemlenmesindeki Etkisinin Araştırılması",
        "authors": ["Selgün Yüceil", "Didem Gökçay"],
        "start_page": 195,
    },
    {
        "title": "Çanakkale Savaş Cephesinden Gönderilen Türk Asker Mektupları",
        "authors": ["Nalan Kızıltan"],
        "start_page": 203,
    },
    {
        "title": "Türkçede Üye Yapısı ve Durum Eklerinin Edinimi",
        "authors": ["Mine Nakipoğlu", "Begüm Avar", "Melike Hendek"],
        "start_page": 211,
    },
    {
        "title": "Türkçede Ad-Eylem Eşdizimliği İçin İstatistiksel ve Anlamsal Ölçütler",
        "authors": ["Özlem Aksu Kurtoğlu"],
        "start_page": 219,
    },
    {
        "title": "Türkçede Özne ve Nesne Ortaçlarının İşlenmesinde Bağlamın Etkisi",
        "authors": ["Emine Yarar", "Burcu Karaduman"],
        "start_page": 227,
    },
    {
        "title": "Türkçede Eylem-Sonu Konumunda Odağın OİP Açısından İncelenmesi",
        "authors": ["İpek Pınar Bekâr"],
        "start_page": 233,
    },
    {
        "title": "Bebeklere Yöneltilen Dil Kullanımlarında Çift-Biçimli (Dimorphous) İfadeler",
        "authors": ["Filiz Çetintaş Yıldırım"],
        "start_page": 241,
    },
    {
        "title": "Türkçe Tümce Vurgusuna İlişkin Gözlemler: Bir Çekirdek Vurgusu Kuralı İncelemesi",
        "authors": ["Fatoş Eren-Özdemir", "Ahmet Bilal Özdemir"],
        "start_page": 249,
    },
    {
        "title": "Türkiye’de Tehlikedeki Dilleri Yaşatma/Canlandırma Çalışmaları: Nogayca Örneği",
        "authors": ["Ülkü Çelik Şavk"],
        "start_page": 257,
    },
    {
        "title": "Down Sendromlu Çocuklarda Sözcük Türlerine İlişkin Bir İnceleme",
        "authors": ["Hazel Zeynep Kurada", "Seda Gökmen", "Semra Şahin", "Esra Özcebe"],
        "start_page": 265,
    },
    {
        "title": "Türkiye Türkçesi ve Tebriz Azericesi Arasındaki Sesbilimsel Değişimler",
        "authors": ["Seyed Hamrad Eshaghi"],
        "start_page": 273,
    },
    {
        "title": "Görsel Destekli Dil Girdileri Olarak Reklamlar ve Çizgi Filmler Projesi",
        "authors": ["Pınar İbe Akcan", "Umut Ufuk Demirhan"],
        "start_page": 281,
    },
    {
        "title": "Eş Kullanım Varsayımına Göre Türkçede Kurallı Karşıt Anlamlılık",
        "authors": ["Soner Akşehirli"],
        "start_page": 289,
    },
    {
        "title": "Yazar Cinsiyeti Değişkeninde Türkçede Toplumsal Cinsiyet",
        "authors": ["Gülcan Çolak"],
        "start_page": 297,
    },
    {
        "title": "Sözcük-Dilbilgisi Süreminde Yakın-Anlamlılık",
        "authors": ["Fırat Öter", "Ayda Sevin"],
        "start_page": 307,
    },
    {
        "title": "Türkçe ve Çağdaş Yunancada Hayvan İsmi İçeren Deyimsel İfadelerde Kültürel Metafor",
        "authors": ["Merve Koldamca Yılmaz"],
        "start_page": 315,
    },
    {
        "title": "Çağdaş Standart Türkiye Türkçesinde Yararlananı İşaretleyen Verme Durumu",
        "authors": ["F. Yelda Şahin"],
        "start_page": 323,
    },
    {
        "title": "Star Dust (Yıldız Tozu) Filminin Propp’un Yaklaşımı Çerçevesinde İncelenmesi",
        "authors": ["Meltem Merve Konu"],
        "start_page": 331,
    },
    {
        "title": "Türkçede Sessiz Okuma Sırasında Bürün: Göz Hareketleri Temelli Bir İnceleme",
        "authors": ["İpek Pınar Bekâr", "Özgür Aydın", "İclâl Ergenç", "Canan Kalaycıoğlu"],
        "start_page": 337,
    },
    {
        "title": "Eski Türkçede Çok Anlamlılık ve Bağlam: İşitme Alanı Algı Eylemleri",
        "authors": ["Zeynep Erk Emeksiz"],
        "start_page": 345,
    },
]

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

def extract_document_text(doc, start_page, end_page):
    pages = []

    for page_number in range(start_page, end_page):
        page_text = extract_page_text(doc, page_number)
        pages.append(page_text)

    return "\n".join(pages)

def printed_page_to_index(printed_page):
    return printed_page + 5

def main():
    pdf_bytes = download_pdf(PDF_URL)
    doc = open_pdf(pdf_bytes)

    print(f"Metadata'daki bildiri sayısı: {len(PAPERS)}")

    records = []

    for i in range(len(PAPERS)):
        paper = PAPERS[i]

        start_index = printed_page_to_index(paper["start_page"])

        if i < len(PAPERS) - 1:
            end_page = PAPERS[i + 1]["start_page"]
        else:
            end_page = ACADEMIC_CONTENT_END_PAGE

        end_index = printed_page_to_index(end_page)

        document_text = extract_document_text(doc, start_index, end_index)

        record = {
            "corpus_type": "academic",
            "source": "Dilbilim Derneği",
            "proceedings_title": "30. Ulusal Dilbilim Kurultayı Bildirileri",
            "publication_year": 2017,
            "title": paper["title"],
            "authors": paper["authors"],
            "start_page": paper["start_page"],
            "end_page": end_page - 1,
            "url": PDF_URL,
            "text": document_text,
        }

        records.append(record)

    with open("data/raw/academic.jsonl", "w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Akademik derlem kaydedildi: {len(records)} bildiri")

if __name__ == "__main__":
    main()
