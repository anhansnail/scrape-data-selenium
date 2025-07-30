import requests
from bs4 import BeautifulSoup
import pandas as pd

def clean(text):
    return text.strip().replace('\n', ' ') if text else ""

# 🔎 Hàm crawl từng trang
def crawl_page(page_num):
    url = f"https://vieclamvinhphuc.gov.vn/nha-tuyen-dung/{page_num}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"❌ Lỗi truy cập trang {url}")
        return []

    soup = BeautifulSoup(res.text, "html.parser")
    boxes = soup.select("div.box")

    data = []
    for box in boxes:
        name = box.select_one(".box-name a")
        address = box.select_one(".item-text p")
        phone_tag = box.select_one(".des p:nth-of-type(2)")
        positions = box.select("div.tin-dang a")

        item = {
            "box-name": clean(name.text if name else ""),
            "address": clean(address.text if address else ""),
            "phone": clean(phone_tag.text.replace("- Số điện thoại:", "") if phone_tag else ""),
            "positions": "; ".join([clean(p.text) for p in positions])
        }

        data.append(item)

    return data

# 👉 CHỌN KHOẢNG TRANG TẠI ĐÂY
start_page = 5
end_page = 10  # bao gồm cả trang này

# ▶️ Lặp crawl
all_data = []
print(f"📥 Bắt đầu lấy dữ liệu từ trang {start_page} đến {end_page}")

for page in range(start_page, end_page + 1):
    print(f"🔍 Đang xử lý trang {page}")
    all_data.extend(crawl_page(page))

# 💾 Xuất file
df = pd.DataFrame(all_data)
df.to_excel(f"vinhphuc_employers_p{start_page}_to_p{end_page}.xlsx", index=False)

print(f"✅ Đã lưu xong vào file vinhphuc_employers_p{start_page}_to_p{end_page}.xlsx")
