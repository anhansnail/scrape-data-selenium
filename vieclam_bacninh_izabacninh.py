import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

def extract_company_info(brief_text):
    # Trích xuất địa chỉ, số điện thoại, email
    email = re.search(r'[\w\.-]+@[\w\.-]+', brief_text)
    phone = re.search(r'(?:(?:\+84|0)[1-9]\d{8,9})|(?:\d{5,}\d*)', brief_text)
    address_match = re.search(r'Địa chỉ:\s*(.*?)(?:, Điện thoại|, Email|$)', brief_text)

    return {
        "Địa chỉ": address_match.group(1).strip() if address_match else "",
        "Điện thoại": phone.group(0) if phone else "",
        "Email": email.group(0) if email else ""
    }

def crawl_izabacninh(start_page=1, end_page=5):
    base_url = "http://www.izabacninh.gov.vn/tin-tuc/viec-tim-nguoi-38/trang-{}.html"
    headers = {"User-Agent": "Mozilla/5.0"}
    all_data = []

    for page in range(start_page, end_page + 1):
        print(f"Đang crawl trang {page}...")
        url = base_url.format(page)
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"Trang {page} không truy cập được.")
                continue

            soup = BeautifulSoup(response.content, "html.parser")
            items = soup.select("div.newslist-bound-content")

            for item in items:
                name_tag = item.select_one("div.newslist-name a")
                time_tag = item.select_one("div.newslist-time")
                brief = item.select_one("div.newslist-brief")

                if not name_tag or not brief:
                    continue

                name = name_tag.text.strip()
                link = name_tag['href']
                date = time_tag.text.strip() if time_tag else ""
                brief_text = brief.text.strip()

                info = extract_company_info(brief_text)

                all_data.append({
                    "Tên công ty": name,
                    "Link chi tiết": link,
                    "Ngày đăng": date,
                    "Địa chỉ": info["Địa chỉ"],
                    "Điện thoại": info["Điện thoại"],
                    "Email": info["Email"]
                })
        except Exception as e:
            print(f"Lỗi ở trang {page}: {e}")

        time.sleep(1)  # Tạm dừng để tránh bị chặn

    return all_data

# --- Cấu hình số trang ---
start = 11
end = 45  # Ví dụ: lấy từ trang 1 đến 10

results = crawl_izabacninh(start, end)

# --- Xuất ra Excel ---
df = pd.DataFrame(results)
df.to_excel(f"izabacninh_trang_{start}_den_{end}.xlsx", index=False)
print(f"Đã lưu {len(results)} dòng vào file 'izabacninh_trang_{start}_den_{end}.xlsx'")
