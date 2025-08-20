from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# --- Danh sách từ khóa ---
# keywords_netherlands  = [
#     "school in Amsterdam",
#     "school in Rotterdam",
#     "school in The Hague",
#     "school in Utrecht",
#     "school in Eindhoven",
#     "school in Groningen",
#     "school in Maastricht",
#     "school in Tilburg",
#     "school in Breda",
#     "school in Haarlem"
# ]
keywords_usa = [
    "school in New York",
    "school in Los Angeles",
    "school in Chicago",
    "school in Houston",
    "school in Phoenix",
    "school in Philadelphia",
    "school in San Antonio",
    "school in San Diego",
    "school in Dallas",
    "school in San Jose"
]


keywords = keywords_usa
max_results = 600

# --- Cài đặt Chrome ---
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--user-agent=Mozilla/5.0")

service = Service("D:/prj_test_1/chromedriver/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 15)

# --- Vòng lặp qua từng từ khóa ---
all_results = []

for keyword in keywords:
    print(f"\n🔎 Bắt đầu tìm kiếm: {keyword}")
    results = []

    # Mở Google Maps
    driver.get(f"https://www.google.com/maps/search/{keyword}")
    time.sleep(5)

    # Cuộn để tải thêm kết quả
    try:
        scrollable_div = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="feed"]')))
        for _ in range(100):
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
            time.sleep(2)
    except:
        print("❌ Không tìm thấy danh sách kết quả.")
        continue

    # Lấy danh sách các địa điểm
    items = driver.find_elements(By.XPATH, '//a[contains(@href, "/place/")]')
    print(f"🔍 Tìm thấy {len(items)} kết quả.")

    # Lặp qua các kết quả
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
                elif "@" in text and "." in text:
                    email = text

            results.append({
                "Từ khóa": keyword,
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

    # Gộp vào kết quả chung
    all_results.extend(results)

# --- Lưu ra Excel ---
df = pd.DataFrame(all_results)
df.to_excel(f"ket_qua_school_all_usa.xlsx", index=False)
print("🎉 Đã lưu file ket_qua_google_maps_all_keywords.xlsx")

# --- Thoát trình duyệt ---
driver.quit()
