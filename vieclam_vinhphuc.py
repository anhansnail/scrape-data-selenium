import requests
from bs4 import BeautifulSoup
import pandas as pd

def clean(text):
    return text.strip().replace('\n', ' ') if text else ""

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
    boxes = soup.select("div.box")  # mỗi box công ty

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

# 🔁 Lấy nhiều trang nếu cần
all_data = []
for page in range(1, 101):  # 👉 đổi số tại đây nếu muốn nhiều hơn (vd: range(1, 6) để lấy 5 trang)
    print(f"🔍 Đang xử lý trang {page}")
    all_data.extend(crawl_page(page))

# 💾 Xuất ra file Excel
df = pd.DataFrame(all_data)
df.to_excel("vinhphuc_employer_info.xlsx", index=False)

print("✅ Đã lưu xong vào file vinhphuc_employer_info.xlsx")
