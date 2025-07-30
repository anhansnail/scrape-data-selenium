import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def extract_company_pair(name_block, info_block):
    name_vi = name_block.select_one("div.tendn")
    name_en = name_block.select_one("div.tengiaodich")
    info_items = info_block.select("li.info")

    data = {
        "Tên tiếng Việt": name_vi.text.replace("Tên tiếng Việt:", "").strip() if name_vi else "",
        "Tên tiếng Anh": name_en.text.replace("Tên tiếng Anh:", "").strip() if name_en else "",
        "Địa chỉ": "",
        "Giấy phép": "",
        "Ngày cấp": "",
        "Điện thoại": "",
        "Website": "",
        "Email": "",
        "Phạm vi hoạt động": "",
    }

    for item in info_items:
        text = item.get_text(strip=True)
        if text.startswith("Địa chỉ:"):
            data["Địa chỉ"] = text.replace("Địa chỉ:", "").strip()
        elif text.startswith("Giấy phép"):
            data["Giấy phép"] = text.split(":", 1)[1].strip()
        elif text.startswith("Ngày cấp:"):
            data["Ngày cấp"] = text.replace("Ngày cấp:", "").strip()
        elif text.startswith("Điện thoại:"):
            data["Điện thoại"] = text.replace("Điện thoại:", "").strip()
        elif text.startswith("Website:"):
            data["Website"] = text.replace("Website:", "").strip()
        elif text.startswith("Email:"):
            data["Email"] = text.replace("Email:", "").strip()
        elif text.startswith("Phạm vi hoạt động:"):
            data["Phạm vi hoạt động"] = text.replace("Phạm vi hoạt động:", "").strip()

    return data

def crawl_pages_by_range(base_url, page_start, page_end):
    all_data = []
    for page in range(page_start, page_end + 1):
        url = f"{base_url}/{page}"
        print(f"📄 Đang lấy trang {page}...")
        response = requests.get(url)
        if response.status_code != 200:
            print(f"❌ Lỗi khi tải trang {page}: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        name_blocks = soup.select("div.company-name.mar-bot")
        info_blocks = soup.select("div.thick-border")

        if not name_blocks or not info_blocks:
            print(f"⚠️ Không tìm thấy dữ liệu tại trang {page}.")
            continue

        for name_block, info_block in zip(name_blocks, info_blocks):
            data = extract_company_pair(name_block, info_block)
            all_data.append(data)

        time.sleep(1)

    return all_data

# Gọi hàm chính
if __name__ == "__main__":
    base_url = "https://www.quanlyluhanh.vn/index.php/cat/1001" #quốc tế
    # base_url = "https://www.quanlyluhanh.vn/index.php/cat/1020" #nội địa

    # 👉 Đặt khoảng trang bạn muốn lấy ở đây
    page_start = 1
    page_end = 250

    all_companies = crawl_pages_by_range(base_url, page_start, page_end)

    df = pd.DataFrame(all_companies)
    df.to_excel(f"dulich_quanlyluhanh_page_{page_start}_to_{page_end}.xlsx", index=False)
    print(f"✅ Đã lưu vào file dulich_quanlyluhanh_page_{page_start}_to_{page_end}.xlsx")
