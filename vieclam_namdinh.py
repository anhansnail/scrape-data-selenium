from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re

# Cấu hình trình duyệt
chrome_options = Options()
chrome_options.add_argument("--headless")
service = Service("D:/prj_test_1/chromedriver/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

base_url = "https://vieclamnamdinh.gov.vn"
all_links = set()

# ✅ BƯỚC 1: Duyệt qua 5 trang đầu tiên
for page in range(131, 181):  # 131 đến 180
    url = f"{base_url}/viec-lam?page=15/p/{page}"
    driver.get(url)
    time.sleep(1)

    elements = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/viec-lam/"]')
    for e in elements:
        href = e.get_attribute("href")
        if href and href.startswith(base_url) and "/viec-lam/" in href and "?" not in href:
            all_links.add(href)

    print(f"✅ Đã lấy trang {page}: tổng cộng {len(all_links)} link")

print(f"📌 Tổng số bài tuyển dụng: {len(all_links)}")

# ✅ BƯỚC 2: Lấy thông tin liên hệ từ từng bài
results = []
wait = WebDriverWait(driver, 5)

for link in all_links:
    driver.get(link)
    time.sleep(1)

    title = driver.title
    email = ""
    phone = ""

    try:
        info_div = wait.until(EC.presence_of_element_located(
            (By.ID, "dnn_ctr3605_Main_ctl00_ctl00_divThongTinLH")
        ))
        text = info_div.text

        email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
        phone_match = re.search(r"0\d{8,10}", text)

        if email_match:
            email = email_match.group()
        if phone_match:
            phone = phone_match.group()

    except:
        print(f"⚠️ Không tìm thấy div liên hệ: {link}")

    results.append({
        "title": title,
        "link": link,
        "email": email,
        "phone": phone
    })

    print(f"🔎 {title} | 📧 {email or '-'} | ☎️ {phone or '-'}")

# ✅ BƯỚC 3: Xuất Excel
df = pd.DataFrame(results)
df.to_excel(f"vieclam_namdinh_page{page}.xlsx", index=False)
driver.quit()

print(f"🎉 Đã lưu file: vieclam_namdinh_page{page}.xlsx")
