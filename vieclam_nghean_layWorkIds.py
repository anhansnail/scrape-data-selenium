import requests
import pandas as pd
import re

url = "http://vieclamnghean.vn/phan-trang-viec-tim-nguoi/"

headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0"
}

def clean_excel_string(s):
    if isinstance(s, str):
        return re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f]', '', s)
    return s

def get_work_data(page, page_size=50):
    payload = {
        "draw": 1,
        "start": (page - 1) * page_size,
        "length": page_size,
        "search[value]": "",
        "search[regex]": "false"
    }

    response = requests.post(url, data=payload, headers=headers)

    if response.status_code != 200:
        print(f"❌ HTTP lỗi: {response.status_code}")
        return []

    try:
        json_data = response.json()
    except Exception as e:
        print(f"❌ Lỗi parse JSON: {e}")
        print("🔍 Response:", response.text[:300])
        return []

    work_data = []
    for item in json_data.get("data", []):
        work_data.append({
            "WorkId": item.get("WorkId"),
            "WorkName": item.get("WorkName")
        })

    return work_data

# Lấy dữ liệu
all_work = []
for page in range(1, 50):
    print(f"📄 Đang xử lý trang {page}")
    works = get_work_data(page)
    print(f"✅ Tìm thấy {len(works)} việc")
    all_work.extend(works)

# Tạo DataFrame
df = pd.DataFrame(all_work)

# ✅ Làm sạch cột WorkName (vì WorkId là số, không cần)
if 'WorkName' in df.columns:
    df['WorkName'] = df['WorkName'].map(clean_excel_string)

# Ghi ra Excel
df.to_excel("ds_workid_name_nghean.xlsx", index=False)

print("✅ Đã lưu file: ds_workid_name_nghean.xlsx")
