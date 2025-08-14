import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# ====== Cấu hình ======
base_url = "https://vieclamquangngai.com.vn/"
list_url = "https://vieclamquangngai.com.vn/viec-lam.html"
start_page = 1
end_page = 170  # ví dụ: trang 1 -> 2

# Danh sách kết quả
results = []

# ====== Hàm lấy link chi tiết từ 1 trang ======
def get_job_links(page):
    if page == 1:
        url = list_url
    else:
        url = f"{list_url}&p={page}"

    res = requests.get(url)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "html.parser")
    job_items = soup.find_all("div", class_="item_product")

    links = []
    for item in job_items:
        a_tag = item.find("a", class_="name")
        if a_tag and a_tag.get("href"):
            full_link = base_url + a_tag["href"].lstrip("/")
            links.append(full_link)
    return links

# ====== Lấy dữ liệu từ nhiều trang ======
for page in range(start_page, end_page + 1):
    print(f"📄 Đang lấy trang {page}...")
    job_links = get_job_links(page)

    for link in job_links:
        try:
            job_res = requests.get(link)
            job_res.encoding = "utf-8"
            job_soup = BeautifulSoup(job_res.text, "html.parser")

            # Tên công việc
            title_tag = job_soup.find("h1", class_="title")
            title = title_tag.get_text(strip=True) if title_tag else ""

            # Thông tin liên hệ
            contact_div = job_soup.find("div", class_="bg-white p-3 border")
            contact_info = contact_div.get_text(strip=True, separator="\n") if contact_div else ""

            results.append({
                "Link": link,
                "Tiêu đề": title,
                "Thông tin liên hệ": contact_info
            })

            time.sleep(1)  # tránh gửi request quá nhanh
        except Exception as e:
            print(f"❌ Lỗi khi xử lý {link}: {e}")

# ====== Xuất ra Excel ======
df = pd.DataFrame(results)
df.to_excel(f"vieclamquangngai_p_{start_page}to{end_page}.xlsx", index=False)
print("✅ Đã lưu vào vieclamquangngai.xlsx")
