import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from tenacity import retry, stop_after_attempt, wait_fixed

BASE_URL = "http://vieclamthainguyen.gov.vn"
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Retry khi load trang danh sách
@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
def get_job_links(page_num):
    url = f"{BASE_URL}/viec-lam?p={page_num}"
    print(f"🔍 Đang tải trang {page_num}...")
    res = requests.get(url, headers=headers, timeout=30)
    soup = BeautifulSoup(res.text, "html.parser")

    job_links = []
    for a in soup.select("a.text_grey2"):
        href = a.get("href")
        if href and href.startswith("/viec-lam/"):
            full_url = BASE_URL + href
            job_links.append(full_url)

    return job_links

# Retry khi load trang chi tiết
@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
def get_contact_info(link):
    res = requests.get(link, headers=headers, timeout=30)
    soup = BeautifulSoup(res.text, "html.parser")

    info_block = soup.select_one("#dnn_ctr3605_Main_ctl00_ctl00_divThongTinLH")
    if not info_block:
        return None

    info = {"Link": link}

    for row in info_block.select(".row"):
        cols = row.select("div")
        if len(cols) >= 2:
            label = cols[0].get_text(strip=True).lower()
            value = cols[1].get_text(strip=True)

            if "người liên hệ" in label:
                info["Người liên hệ"] = value
            elif "địa chỉ" in label:
                info["Địa chỉ"] = value
            elif "điện thoại" in label:
                info["Điện thoại"] = value
            elif "email" in label:
                info["Email"] = value

    return info

# =================== CHẠY ===================

all_data = []
start_page = 151
end_page = 160  # <-- có thể tăng khi ổn định

for page in range(start_page, end_page + 1):
    try:
        job_links = get_job_links(page)
    except Exception as e:
        print(f"❌ Lỗi khi tải trang {page}: {type(e).__name__}: {e}")
        continue

    for link in job_links:
        print(f"📄 Đang xử lý: {link}")
        try:
            info = get_contact_info(link)
            if info:
                all_data.append(info)
        except Exception as e:
            print(f"❌ Lỗi khi xử lý {link}: {type(e).__name__}: {e}")
        time.sleep(2)  # nghỉ giữa các lần để tránh chặn

# Ghi ra Excel
df = pd.DataFrame(all_data)
df.to_excel(f"vieclam_thainguyen_p{start_page}_to_p{end_page}.xlsx", index=False)
print("✅ Đã lưu dữ liệu ra Excel.")
