import requests
import pandas as pd
import math
import time

BASE_URL = "https://api.vieclamhungyen.gov.vn/api/getListEmployer"

limit = 50  # lấy tối đa để giảm số lần gọi API

# Lấy trang đầu để biết tổng số bản ghi
res = requests.get(BASE_URL, params={"page": 1, "limit": limit})
data = res.json()

total = data.get("total", 0)
total_pages = math.ceil(total / limit)

print(f"Tổng bản ghi: {total} | Số trang: {total_pages}")

result = []

# Crawl toàn bộ trang
for page in range(1, total_pages + 1):
    print(f"Đang lấy trang {page}/{total_pages}")

    res = requests.get(BASE_URL, params={"page": page, "limit": limit})
    json_data = res.json()

    if json_data.get("status"):
        for item in json_data.get("data", []):
            result.append({
                "email": item.get("email", "").strip(),
                "company_name": item.get("company_name", "").strip(),
                "company_contact": item.get("company_contact", "").strip(),
                "company_phone": item.get("company_phone", "").strip()
            })

    time.sleep(0.3)

# Chuyển sang DataFrame
df = pd.DataFrame(result)
#
# # (tuỳ chọn) loại bỏ dòng không có email
# df = df[df["email"] != ""]
#
# # (tuỳ chọn) loại bỏ trùng email
# df = df.drop_duplicates(subset=["email"])

# Xuất Excel
df.to_excel("employers_filtered_260424.xlsx", index=False)

print("✅ Đã lưu file employers_filtered.xlsx")