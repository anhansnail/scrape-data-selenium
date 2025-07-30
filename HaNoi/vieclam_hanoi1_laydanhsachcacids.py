import requests
import urllib3
import time
import csv

# Tắt cảnh báo HTTPS không xác thực
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

all_ids = []
page_index = 1
page_size = 100  # Có thể điều chỉnh thành 20, 50...

base_url = "https://getway.vieclamhanoi.net/api/CongBoNguoiSdLaoDong/TatCa"

while True:
    params = {
        "PageIndex": page_index,
        "PageSize": page_size,
        "Code": "",
        "MucLuong": "",
        "KinhNghiem": "",
        "NganhKinhDoanh": "",
        "HuyenId": "",
        "TenCongViec": "",
        "UserId": "",
        "IsSuperAdmin": "false",
        "UnitId": "0",
        "AccountId": "0",
        "DeparmentId": "0",
        "IpAddress": "",
        "Role": ""
    }

    try:
        response = requests.get(base_url, params=params, verify=False)
        if response.status_code != 200:
            print(f"⚠️ Lỗi HTTP {response.status_code} tại trang {page_index}")
            break

        data = response.json().get("data", [])
        if not data:
            print("⛔ Hết dữ liệu.")
            break

        for item in data:
            id_ = item.get("id")
            if id_:
                all_ids.append([id_])  # Mỗi ID là 1 dòng

        print(f"✅ Trang {page_index}: Đã lấy {len(data)} ID")

        page_index += 1
        time.sleep(0.2)

    except Exception as e:
        print(f"❌ Lỗi ở trang {page_index}: {e}")
        break

# 👉 Ghi ra file CSV
file_path = "../ds_id_hanoi.csv"
with open(file_path, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["id"])  # Header
    writer.writerows(all_ids)

print(f"\n✅ Đã lưu {len(all_ids)} ID vào file: {file_path}")
