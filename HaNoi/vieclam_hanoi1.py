import requests
import urllib3
import csv
import time

# Tắt cảnh báo SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Đọc danh sách ID từ file CSV
id_file = "../ds_id_hanoi.csv"
ids = []

with open(id_file, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        ids.append(row["id"])

print(f"📥 Đã đọc {len(ids)} ID từ file {id_file}")

# Lấy thông tin chi tiết
data_list = []
for index, id_ in enumerate(ids):
    url = f"https://getway.vieclamhanoi.net/api/CongBoNguoiSdLaoDong/GetbyId?id={id_}"

    try:
        res = requests.get(url, verify=False, timeout=10)
        if res.status_code == 200:
            detail = res.json().get("nguoiSdLaoDong", {})
            data_list.append({
                "id": id_,
                "ten": detail.get("ten", ""),
                "sdt": detail.get("sdt", ""),
                "daiDien": detail.get("daiDien", ""),
                "email": detail.get("email", ""),
                "sdtLh": detail.get("sdtLh", ""),
                "emailLh": detail.get("emailLh", ""),
                "noiLamViecKhac": detail.get("noiLamViecKhac", ""),
            })
            print(f"✅ ID {id_} - {detail.get('ten', '')}")
        else:
            print(f"⚠️ Lỗi HTTP {res.status_code} với ID {id_}")

    except Exception as e:
        print(f"❌ Lỗi khi xử lý ID {id_}: {e}")

    # Nghỉ giữa mỗi 20 ID để tránh bị chặn
    if index % 20 == 0:
        time.sleep(1)

# Ghi ra file CSV
output_file = "../thong_tin_chi_tiet_Hanoi.csv"
with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "id", "ten", "sdt", "daiDien", "email", "sdtLh", "emailLh", "noiLamViecKhac"
    ])
    writer.writeheader()
    writer.writerows(data_list)

print(f"\n✅ Đã lưu {len(data_list)} bản ghi vào file: {output_file}")
