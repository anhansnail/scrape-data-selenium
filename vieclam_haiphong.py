import requests
import pandas as pd
import time

# Base URL và tham số cố định
base_url = "https://vieclamhaiphong.net/api/submit_ajax/articleListPaging"
params = {
    "channel_name": "jobs",
    "category_id": 166,
    "nganhnghe": 0,
    "khuvuc": 0,
    "trinhdo": 0,
    "page_size": 100,  # Có thể tăng lên đến 3000 nếu API cho phép
    "page": 1,
    "skeyword": ""
}

all_results = []
total_pages = 1  # Khởi tạo tạm, sẽ cập nhật sau trang đầu tiên

for page in range(1, 1000):  # Duyệt đến khi không còn dữ liệu
    print(f"🔄 Đang lấy trang {page}...")
    params["page"] = page
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()

    if page == 1:
        # Lấy số lượng trang từ phản hồi trang đầu
        total_pages = int(data.get("pages", 1))

    # Nếu không có dữ liệu -> dừng
    if not data.get("data"):
        print("✅ Không còn dữ liệu.")
        break

    # Trích thông tin cần thiết
    for item in data["data"]:
        all_results.append({
            "id": item.get("id"),
            "nhatuyendung": item.get("nhatuyendung"),
            "user_name": item.get("user_name"),
            "Contact": item.get("Contact"),
            "DienThoaiNguoiLienHe": item.get("DienThoaiNguoiLienHe"),
            "ReceiveEmail": item.get("ReceiveEmail"),
            "DiaChiNguoiLienHe": item.get("DiaChiNguoiLienHe"),
            "title": item.get("title"),
            "ViTriDuTuyen": item.get("ViTriDuTuyen")
        })

    # Dừng nếu đến trang cuối cùng
    if page >= total_pages:
        break

    time.sleep(0.3)  # Tránh gửi quá nhanh làm server chặn

# Xuất ra file Excel
df = pd.DataFrame(all_results)
df.to_excel("vieclam_haiphong_all_pages.xlsx", index=False)
print(f"✅ Đã lưu {len(df)} dòng dữ liệu vào 'vieclam_haiphong_all_pages.xlsx'")
