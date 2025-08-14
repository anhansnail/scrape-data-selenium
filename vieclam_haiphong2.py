import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

# ================== ⚙️ CẤU HÌNH ==================
BASE_URL = "https://www.tuyendunghaiphong.vn"
page_start = 501   # Trang bắt đầu
page_end = 620     # Trang kết thúc
delay = 1         # Giãn cách giữa các request (giây)

# ================== 📦 LƯU KẾT QUẢ ==================
all_jobs = []

# ================== 🔄 LẶP QUA CÁC TRANG ==================
for page in range(page_start, page_end + 1):
    url = f"{BASE_URL}/viec-lam/trang-{page}?tukhoa=&nganhnghe=&diadiem=0"
    print(f"📄 Đang lấy danh sách: {url}")

    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    # Lấy các khối bài đăng tuyển
    job_blocks = soup.find_all("div", class_="border-bootom-10 viec-lam")

    for job in job_blocks:
        a_tag = job.find("a", href=True)
        if a_tag:
            detail_link = BASE_URL + a_tag["href"]

            try:
                detail_res = requests.get(detail_link)
                detail_soup = BeautifulSoup(detail_res.text, "html.parser")

                # Lấy tiêu đề
                title_tag = detail_soup.find("h1")
                title = title_tag.get_text(strip=True) if title_tag else ""

                # Lấy thông tin liên hệ (id="thongtintuyendung")
                contact_div = detail_soup.find("div", id="thongtintuyendung")
                contact_info = contact_div.get_text("\n", strip=True) if contact_div else ""

                all_jobs.append({
                    "url": detail_link,
                    "title": title,
                    "contact_info": contact_info
                })

                print(f"✅ Lấy thành công: {title}")

            except Exception as e:
                print(f"❌ Lỗi khi lấy {detail_link}: {e}")

            time.sleep(delay)

# ================== 💾 LƯU RA EXCEL ==================
df = pd.DataFrame(all_jobs)
df.to_excel(f"2tuyendung_haiphong{page_start}to{page_end}.xlsx", index=False)
print(f"📊 Tổng số bài lấy được: {len(all_jobs)}")
print(f"2tuyendung_haiphong{page_start}to{page_end}.xlsx")
