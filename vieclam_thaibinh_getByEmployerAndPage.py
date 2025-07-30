import requests
import pandas as pd
import time
import re

def clean_text(text):
    """Xóa các ký tự không hợp lệ để ghi Excel"""
    if isinstance(text, str):
        # Xóa ký tự điều khiển ASCII (0-31), ngoại trừ xuống dòng (\n) và tab (\t)
        return re.sub(r"[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]", "", text)
    return text

def fetch_all_employers():
    all_data = []
    page = 1
    limit = 50

    while True:
        url = f"https://api-dev.vieclamthaibinh.vn/api/getListEmployer?page={page}&limit={limit}"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Lỗi khi gọi trang {page}.")
            break

        data = response.json().get("data", [])
        if not data:
            break

        for emp in data:
            all_data.append({
                "id": emp.get("id"),
                "email": clean_text(emp.get("email")),
                "company_name": clean_text(emp.get("company_name")),
                "company_address": clean_text(emp.get("company_address")),
                "company_contact": clean_text(emp.get("company_contact")),
                "company_phone": clean_text(emp.get("company_phone")),
                "company_mst": clean_text(emp.get("company_mst")),
            })

        print(f"Đã lấy trang {page}")
        page += 1
        time.sleep(0.3)

    return all_data

# Gọi và xuất Excel
data = fetch_all_employers()
df = pd.DataFrame(data)

# Ghi file Excel an toàn
df.to_excel("tat_ca_employer_thaiBinh.xlsx", index=False)
print("✅ Đã lưu tat_ca_employer_thaiBinh.xlsx thành công.")
