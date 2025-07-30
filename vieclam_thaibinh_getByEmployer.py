import requests
import json

import pandas as pd


# ✅ 1. Gọi API và phân tích dữ liệu


url = "https://api-dev.vieclamthaibinh.vn/api/getListEmployer?is_urgent=1&limit=10000"
response = requests.get(url)
data = response.json()

# In ra để kiểm tra cấu trúc
print(json.dumps(data, indent=2, ensure_ascii=False))

# ✅ 2. Trích xuất thông tin mong muốn
for emp in data.get('data', []):
    print("ID:", emp.get("id"))
    print("Email:", emp.get("email"))
    print("Tên công ty:", emp.get("company_name"))
    print("Địa chỉ:", emp.get("company_address"))
    print("Người liên hệ:", emp.get("company_contact"))
    print("Số điện thoại:", emp.get("company_phone"))
    print("Mã số thuế:", emp.get("company_mst"))
    print("-" * 50)

# ✅ 3. (Tùy chọn) Lưu ra Excel
results = []
for emp in data.get('data', []):
    results.append({
        "id": emp.get("id"),
        "email": emp.get("email"),
        "company_name": emp.get("company_name"),
        "company_address": emp.get("company_address"),
        "company_contact": emp.get("company_contact"),
        "company_phone": emp.get("company_phone"),
        "company_mst": emp.get("company_mst"),
    })

df = pd.DataFrame(results)
df.to_excel("employer_info.xlsx", index=False)
print("Đã lưu vào employer_info.xlsx")
