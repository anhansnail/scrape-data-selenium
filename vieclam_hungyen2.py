import requests
import pandas as pd
import time

BASE_URL = "https://api.vieclamhungyen.gov.vn/api/getSingleWork/{}"

results = []

# START_ID = 3999
# END_ID = 1
START_ID = 5631
END_ID = 3999

for work_id in range(START_ID, END_ID - 1, -1):
    record = {
        "work_id": work_id,
        "company_name": "",
        "company_contact": "",
        "company_phone": "",
        "company_address": "",
        "fetch_status": ""
    }

    try:
        url = BASE_URL.format(work_id)
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            record["fetch_status"] = "HTTP_ERROR"
            results.append(record)
            print(f"❌ ID {work_id} - HTTP {response.status_code}")
            continue

        json_data = response.json()

        if not json_data.get("status"):
            record["fetch_status"] = "NO_DATA"
            results.append(record)
            print(f"⚠️ ID {work_id} - status=false")
            continue

        data = json_data.get("data", {})
        employer = data.get("employer")

        if not employer:
            record["fetch_status"] = "NO_DATA"
            results.append(record)
            print(f"⚠️ ID {work_id} - Không có employer")
            continue

        # Có dữ liệu
        record.update({
            "company_name": employer.get("company_name", ""),
            "company_contact": employer.get("company_contact", ""),
            "company_phone": employer.get("company_phone", ""),
            "company_address": employer.get("company_address", ""),
            "fetch_status": "OK"
        })

        results.append(record)
        print(f"✅ ID {work_id} - OK")

        time.sleep(0.2)

    except Exception as e:
        record["fetch_status"] = "EXCEPTION"
        results.append(record)
        print(f"❌ ID {work_id} - Exception: {e}")

# Xuất Excel
df = pd.DataFrame(results)
df.to_excel("employer_vieclamhungyen260420.xlsx", index=False)

print(f"\n🎉 Hoàn thành! Tổng bản ghi: {len(df)}")
