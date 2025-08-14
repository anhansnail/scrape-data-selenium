import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# ===== Cấu hình =====
page_start = 21   # Trang bắt đầu
page_end = 100     # Trang kết thúc
page_size = 20   # Số bản ghi mỗi trang

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

all_data = []

# ===== Lấy ID từ API =====
for page in range(page_start, page_end + 1):
    api_url = "https://vieclamhaiphong.net/api/submit_ajax/articleListPaging"
    params = {
        "channel_name": "jobs",
        "category_id": 166,
        "nganhnghe": 0,
        "khuvuc": 0,
        "trinhdo": 0,
        "page_size": page_size,
        "page": page,
        "skeyword": ""
    }
    try:
        res = requests.get(api_url, params=params, headers=headers, timeout=10)
        res.raise_for_status()
        data_json = res.json()

        job_ids = [item["id"] for item in data_json.get("data", [])]
        print(f"📄 Trang {page} có {len(job_ids)} ID: {job_ids}")

        # ===== Lấy chi tiết từng ID =====
        for job_id in job_ids:
            detail_url = f"https://vieclamhaiphong.net/viec-lam/show-{job_id}.html"
            try:
                detail_res = requests.get(detail_url, headers=headers, timeout=10)
                detail_res.raise_for_status()
                soup = BeautifulSoup(detail_res.text, "html.parser")

                tab_content = soup.find("div", class_="tab-content")
                html_content = str(tab_content) if tab_content else ""

                all_data.append({
                    "id": job_id,
                    "url": detail_url,
                    "tab_content_html": html_content
                })

                print(f"✅ Lấy xong ID {job_id}")
                time.sleep(1)  # tránh spam server
            except Exception as e:
                print(f"❌ Lỗi lấy chi tiết ID {job_id}: {e}")
    except Exception as e:
        print(f"❌ Lỗi API trang {page}: {e}")

# ===== Xuất file =====
df = pd.DataFrame(all_data)
df.to_excel(f"vieclam_haiphong_pages{page_start}to{page_end}.xlsx", index=False)
print("💾 Đã lưu job_details_by_pages.xlsx")
