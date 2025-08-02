import requests
import pandas as pd
import time

# Khởi tạo danh sách kết quả
all_jobs = []

# Cấu hình khoảng trang
page_start = 101
page_end = 300  # Lấy đến trang 10

for page in range(page_start, page_end + 1):
    print(f"🔄 Đang tải trang {page}...")

    url = f"https://vieclamhaiphong.net/api/submit_ajax/articleListPaging"
    params = {
        "channel_name": "jobs",
        "category_id": 166,
        "nganhnghe": 0,
        "khuvuc": 0,
        "trinhdo": 0,
        "page_size": 50,
        "page": page,
        "skeyword": ""
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        items = data.get("data", [])
        if not items:
            print(f"✅ Không có dữ liệu tại trang {page}.")
            continue

        for job in items:
            all_jobs.append({
                "id": job.get("id"),
                "nhatuyendung": job.get("nhatuyendung"),
                "user_name": job.get("user_name"),
                "Contact": job.get("Contact"),
                "DienThoaiNguoiLienHe": job.get("DienThoaiNguoiLienHe"),
                "ReceiveEmail": job.get("ReceiveEmail"),
                "DiaChiNguoiLienHe": job.get("DiaChiNguoiLienHe"),
                "title": job.get("title"),
                "ViTriDuTuyen": job.get("ViTriDuTuyen"),
            })

        time.sleep(0.5)

    except Exception as e:
        print(f"❌ Lỗi tại trang {page}: {e}")
        continue

# Xuất ra file
df = pd.DataFrame(all_jobs)
df.to_excel(f"vieclamhaiphong_paging{page_start}.xlsx", index=False)
print("📁 Đã lưu file 'vieclamhaiphong_paging.xlsx'")
