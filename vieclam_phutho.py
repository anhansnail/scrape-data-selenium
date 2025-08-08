import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# ========== ⚙️ CẤU HÌNH ========== #
start_page = 3  # Trang bắt đầu
end_page = 40    # Trang kết thúc

# ========== 🧩 LẤY LINK BÀI CHI TIẾT ========== #
def get_detail_links(page_index):
    url = f"http://vieclamphutho.gov.vn/ViecTimNguoi/ListViecTimNguoiPartial?p={page_index}&IdChuyenMucFilter=&elementItem=load-viec-tim-nguoi&pageSize=0&pageIndex={page_index}"

    try:
        response = requests.get(url, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")
        links = []

        for a_tag in soup.select("a[href^='/Viec-tim-nguoi/']"):
            href = a_tag.get("href")
            if href:
                full_url = f"http://vieclamphutho.gov.vn{href}"
                links.append(full_url)

        return list(set(links))  # loại bỏ trùng lặp

    except Exception as e:
        print(f"❌ Lỗi khi tải trang {page_index}: {e}")
        return []

# ========== 🧩 LẤY THÔNG TIN LIÊN HỆ ========== #
def get_contact_info(detail_url):
    try:
        res = requests.get(detail_url, timeout=10)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, "html.parser")

        # Tìm <ul> chứa thông tin liên hệ (có thẻ <i> class 'bi-person-vcard' chẳng hạn)
        ul_tags = soup.find_all("ul")

        contact = {
            "URL": detail_url,
            "Tên người liên hệ": "",
            "Email": "",
            "Điện thoại": ""
        }

        for ul in ul_tags:
            if ul.find("i", class_="bi-person-vcard") or ul.find("h5", string="Tên người liên hệ"):
                for li in ul.find_all("li"):
                    h5 = li.find("h5")
                    span = li.find("span")
                    if h5 and span:
                        label = h5.get_text(strip=True)
                        value = span.get_text(strip=True)
                        if label in contact:
                            contact[label] = value
                break  # Dừng sau khi đã lấy đúng khối <ul>

        return contact

    except Exception as e:
        print(f"❌ Lỗi khi xử lý {detail_url}: {e}")
        return None

# ========== 🔁 DUYỆT TỪNG TRANG ========== #
all_contacts = []

for page_index in range(start_page, end_page + 1):
    print(f"\n📄 Đang xử lý trang {page_index}...")
    detail_links = get_detail_links(page_index)
    print(f"🔗 Tìm thấy {len(detail_links)} bài tuyển dụng.")

    for link in detail_links:
        print(f"➡️ Đang lấy: {link}")
        info = get_contact_info(link)
        if info:
            all_contacts.append(info)
        time.sleep(1)  # nghỉ 1s tránh bị chặn

# ========== 💾 XUẤT RA EXCEL ========== #
if all_contacts:
    df = pd.DataFrame(all_contacts)
    output_file = f"thong_tin_lien_he_phutho_{start_page}_{end_page}.xlsx"
    df.to_excel(output_file, index=False)
    print(f"\n✅ Đã lưu {len(df)} liên hệ vào: {output_file}")
else:
    print("⚠️ Không có dữ liệu nào được thu thập.")
