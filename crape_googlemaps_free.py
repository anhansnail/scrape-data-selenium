from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# --- Cấu hình ---
# keyword = "spa Da Nang"
# keyword = "ha noi hotel"
# keyword = "khách sạn ở phố cổ"
keyword = "travel companies in holland"
max_results = 600
results = []

# --- Cài đặt Chrome ---
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--user-agent=Mozilla/5.0")

service = Service("D:/prj_test_1/chromedriver/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 15)

# --- Mở Google Maps ---
driver.get(f"https://www.google.com/maps/search/{keyword}")
time.sleep(5)

# --- Cuộn để tải thêm kết quả ---
try:
    scrollable_div = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="feed"]')))
    for _ in range(5):
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
        time.sleep(2)
except:
    print("❌ Không tìm thấy danh sách kết quả.")

# --- Lấy danh sách các địa điểm ---
items = driver.find_elements(By.XPATH, '//a[contains(@href, "/place/")]')
print(f"🔍 Tìm thấy {len(items)} kết quả.")

# --- Lặp qua các kết quả ---
for index, item in enumerate(items):
    if index >= max_results:
        break

    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", item)
        time.sleep(1)
        item.click()
        time.sleep(4)

        name_el = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.DUwDvf")))
        name = name_el.text.strip()

        address = phone = website = email = ""
        all_info = []

        info_blocks = driver.find_elements(By.CSS_SELECTOR, '.Io6YTe.fontBodyMedium.kR99db')
        for block in info_blocks:
            text = block.text.strip()
            all_info.append(text)
            if "http" in text or "www." in text:
                website = text
            elif text.startswith("0") or text.startswith("+"):
                phone = text
            elif "," in text and len(text) > 10:
                address = text
            # Tìm email (dùng ký tự @ để phát hiện)
            elif "@" in text and "." in text:
                email = text

        results.append({
            "Tên": name,
            "Địa chỉ": address,
            "Số điện thoại": phone,
            "Email": email,
            "Website": website,
            "Thông tin khác": " | ".join(all_info)
        })

        print(f"{index+1}. ✅ {name}")
    except Exception as e:
        print(f"❌ Lỗi tại kết quả {index+1}: {e}")
        continue

# --- Lưu ra Excel ---
df = pd.DataFrame(results)
df.to_excel(f"{keyword}_ket_qua_google_maps.xlsx", index=False)  # Không dùng encoding hay engine
print(f"🎉 Đã lưu file {keyword}_ket_qua_google_maps.xlsx")

# --- Thoát trình duyệt ---
driver.quit()
