import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import time

def clean_text(text):
    if isinstance(text, str):
        return re.sub(r'[\x00-\x1F]', '', text).strip()
    return ""

def get_contact_info(work_id):
    url = f"http://vieclamnghean.vn/chi-tiet-viec-tim-nguoi/{work_id}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return {"WorkId": work_id, "Notes": "Lỗi tải trang", "URL": url}

        soup = BeautifulSoup(res.text, "html.parser")

        content_wrapper = soup.select_one(".infoDetail-content")
        if not content_wrapper:
            print(f"⚠️ Không tìm thấy .infoDetail-content trong WorkId {work_id}")
            return {"WorkId": work_id, "Notes": "", "URL": url}

        notes = content_wrapper.select(".infoDetail-content-note")
        notes_text = "\n\n".join(clean_text(note.get_text(separator="\n", strip=True)) for note in notes)

        return {
            "WorkId": work_id,
            "Notes": notes_text,
            "URL": url
        }

    except Exception as e:
        print(f"❌ Lỗi WorkId {work_id}: {e}")
        return {"WorkId": work_id, "Notes": "Lỗi xử lý", "URL": url}

# ✅ Đọc toàn bộ danh sách WorkId từ file Excel
df_input = pd.read_excel("ds_workid_name_nghean.xlsx")
work_ids = df_input["WorkId"].dropna().astype(int).tolist()

# ✅ Lặp qua toàn bộ WorkId
results = []
for idx, wid in enumerate(work_ids):
    print(f"🔍 {idx+1}/{len(work_ids)} - Đang lấy nội dung WorkId {wid}")
    info = get_contact_info(wid)
    results.append(info)
    time.sleep(0.5)  # Chờ nhẹ để tránh bị chặn

# ✅ Ghi kết quả ra file Excel
df_result = pd.DataFrame(results)
df_result.to_excel("chi_tiet_mo_ta_tat_ca_nghean.xlsx", index=False)

print("✅ Đã lưu toàn bộ nội dung vào: chi_tiet_mo_ta_tat_ca_nghean.xlsx")
