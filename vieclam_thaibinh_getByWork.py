import requests
import json
import pandas as pd

url = "https://api-dev.vieclamthaibinh.vn/api/getListWorks?is_urgent=1&limit=3"
response = requests.get(url)
data = response.json()

# In ra cấu trúc thô để kiểm tra
print(json.dumps(data, indent=2, ensure_ascii=False))



for work in data['data']:
    work_id = work.get('id')
    employer = work.get('employer', {})

    print("ID:", work_id)
    print("Tên công ty:", employer.get('company_name'))
    print("company_contact:", employer.get('company_contact'))
    print("SĐT:", employer.get('company_phone'))
    print("Địa chỉ:", employer.get('company_address'))
    print("employer_id:", employer.get('employer_id'))
    print("-" * 40)

results = []
for work in data['data']:
    employer = work.get('employer', {})
    results.append({
        "id": work.get('id'),
        "company_name": employer.get('company_name'),
        "company_contact": employer.get('company_contact'),
        "company_phone": employer.get('company_phone'),
        "company_address": employer.get('company_address'),
        "employer_id": employer.get('employer_id'),
    })

df = pd.DataFrame(results)
df.to_excel("thong_tin_employer_thaibinh.xlsx", index=False)
print("Đã xuất file Excel.")
