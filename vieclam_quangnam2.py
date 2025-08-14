import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# ===== Cấu hình =====
page_start = 12   # Trang bắt đầu
page_end = 15     # Trang kết thúc
output_file = f"vieclam_quangnam_{page_start}to{page_end}.xlsx"

# Danh sách kết quả
data = []

# ===== Lấy dữ liệu từ nhiều trang =====
for page in range(page_start, page_end + 1):
    url = f"https://vieclamquangnam.vn/tim-kiem/viec-lam?page={page}&order=1"
    print(f"🔍 Đang lấy danh sách từ trang {page}: {url}")

    res = requests.get(url)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "html.parser")

    job_boxes = soup.find_all("div", class_="box-job-horizontal mb-12")

    for job in job_boxes:
        a_tag = job.find("a", href=True)
        if a_tag and a_tag['href'].startswith("/viec-lam/"):
            full_link = "https://vieclamquangnam.vn" + a_tag['href']

            # Lấy nội dung chi tiết
            try:
                detail_res = requests.get(full_link)
                detail_res.encoding = "utf-8"
                detail_soup = BeautifulSoup(detail_res.text, "html.parser")

                job_detail_div = detail_soup.find("div", class_="card card-job-detail mb-5")
                job_detail_text = job_detail_div.get_text(separator="\n", strip=True) if job_detail_div else ""

                # Lưu vào danh sách
                data.append({
                    "Link": full_link,
                    "ChiTiet": job_detail_text
                })
                print(f"✅ Lấy thành công: {full_link}")

            except Exception as e:
                print(f"❌ Lỗi khi lấy {full_link}: {e}")

            time.sleep(1)  # nghỉ 1s tránh bị chặn

# ===== Xuất ra Excel =====
df = pd.DataFrame(data)
df.to_excel(f"2vieclam_quangnam_p_{page_start}to{page_end}.xlsx", index=False)
print(f"Đã lưu vieclam_quangnamp_{page_start}to{page_end}.xlsx")
