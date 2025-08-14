import requests
from bs4 import BeautifulSoup
import pdfplumber
import io
from pdf2image import convert_from_bytes
import pytesseract
import pandas as pd
import time


# Hàm đọc PDF, nếu không có text thì OCR
def pdf_to_text(pdf_url):
    try:
        pdf_response = requests.get(pdf_url, timeout=20)
        pdf_response.raise_for_status()
        content = pdf_response.content

        # 1. Thử đọc bằng pdfplumber
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)

        # 2. Nếu không có text -> OCR
        if not text.strip():
            print(f" -> PDF {pdf_url} có thể là ảnh, đang OCR...")
            images = convert_from_bytes(content)
            ocr_text = []
            for img in images:
                ocr_text.append(pytesseract.image_to_string(img, lang="vie"))
            text = "\n".join(ocr_text)

        return text.strip()
    except Exception as e:
        print(f"Lỗi khi đọc PDF {pdf_url}: {e}")
        return ""


# Crawl nhiều trang
page_start = 1
page_end = 2  # chỉnh số trang tùy ý

results = []

for page in range(page_start, page_end + 1):
    list_url = f"https://vieclamquangnam.gov.vn/vieclam/tin-tuc-nd70?p={page}"
    print(f"Đang xử lý trang {page} -> {list_url}")

    try:
        res = requests.get(list_url, timeout=20)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, "html.parser")

        items = soup.find_all("div", class_="item-6")
        for item in items:
            a_tag = item.find("a", href=True)
            if not a_tag:
                continue
            detail_link = a_tag["href"]
            if not detail_link.startswith("http"):
                detail_link = "https://vieclamquangnam.gov.vn" + detail_link

            print(f" -> Vào bài: {detail_link}")
            detail_res = requests.get(detail_link, timeout=20)
            detail_res.encoding = "utf-8"
            detail_soup = BeautifulSoup(detail_res.text, "html.parser")

            pdf_div = detail_soup.find("div", class_="pdf")
            if pdf_div:
                iframe = pdf_div.find("iframe", src=True)
                if iframe:
                    pdf_link = iframe["src"]
                    if not pdf_link.startswith("http"):
                        pdf_link = "https://vieclamquangnam.gov.vn" + pdf_link

                    pdf_text = pdf_to_text(pdf_link)

                    results.append({
                        "Bài đăng": detail_link,
                        "Link PDF": pdf_link,
                        "Nội dung PDF": pdf_text
                    })

            time.sleep(1)  # nghỉ 1s tránh bị chặn
    except Exception as e:
        print(f"Lỗi trang {list_url}: {e}")


# Xuất ra Excel
df = pd.DataFrame(results)
df.to_excel("vieclam_quangnam_pdf_OCR.xlsx", index=False)
print(f"Đã lưu {len(results)} kết quả vào vieclam_quangnam_pdf_OCR.xlsx")
