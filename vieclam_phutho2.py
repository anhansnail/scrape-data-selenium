import requests
from bs4 import BeautifulSoup
import csv
import re

BASE_URL = "https://phutho.work"

def crawl_jobs_in_page(page):
    print(f"🔄 Đang xử lý trang {page}...")
    url = f"{BASE_URL}/tin-tuyen-dung/page/{page}"
    resp = requests.get(url)
    if resp.status_code != 200:
        print(f"❌ Không thể tải trang {page}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    job_items = soup.select("div.item.p-2.rounded")

    results = []
    for item in job_items:
        # Lấy link chi tiết và tiêu đề
        title_tag = item.select_one("a.title")
        if not title_tag:
            continue
        detail_url = title_tag["href"]
        title = title_tag.get_text(strip=True)

        # Tên công ty
        company_tag = item.select_one("strong a")
        company = company_tag.get_text(strip=True) if company_tag else ""

        # Mức lương, hạn nộp, địa điểm
        info_spans = item.select("div.row-cols-3 span.form-text")
        salary = info_spans[0].get_text(strip=True) if len(info_spans) > 0 else ""
        deadline = info_spans[1].get_text(strip=True) if len(info_spans) > 1 else ""
        location = info_spans[2].get_text(strip=True) if len(info_spans) > 2 else ""

        # Truy cập trang chi tiết để lấy phần Liên hệ
        r2 = requests.get(detail_url)
        if r2.status_code != 200:
            lien_he_text = "(Không tải được chi tiết)"
        else:
            s2 = BeautifulSoup(r2.text, "html.parser")
            header = s2.find("h3", id="lien-he")
            lien_he_text = ""
            if header:
                for sib in header.find_next_siblings():
                    if sib.name and re.match(r"h[1-3]", sib.name):
                        break
                    lien_he_text += sib.get_text(" ", strip=True) + "\n"
            lien_he_text = lien_he_text.strip()

        results.append({
            "title": title,
            "url": detail_url,
            "company": company,
            "salary": salary,
            "deadline": deadline,
            "location": location,
            "lien_he": lien_he_text
        })

    return results


# ==== ⚙️ Thiết lập khoảng trang ====
start_page = 1
end_page = 14   # 👉 Thay đổi tại đây nếu cần

all_jobs = []

for page in range(start_page, end_page + 1):
    jobs = crawl_jobs_in_page(page)
    all_jobs.extend(jobs)

# ==== 📦 Ghi ra file CSV ====
with open(f"260205tuyen_dung_phutho_pages{end_page}.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "url", "company", "salary", "deadline", "location", "lien_he"])
    writer.writeheader()
    writer.writerows(all_jobs)

print(f"\n✅ Hoàn tất! Đã lưu {len(all_jobs)} bài đăng vào 'tuyen_dung_vinhphuc_pages.csv'")
