import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# --- Danh sách từ khóa ---
keywords_belgium = [
    # "travel companies in Brussels",
    # "travel companies in Antwerp",
    # "travel companies in Ghent",
    # "travel companies in Bruges",
    # "travel companies in Leuven"
    "travel companies in Liège",
    "travel companies in Namur",
    "travel companies in Mons",
    "travel companies in Mechelen",
    "travel companies in Hasselt"
]
keywords = keywords_belgium
max_results = 1000   # test nhanh

# --- Cài đặt Chrome ---
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--user-agent=Mozilla/5.0")

service = Service("D:/prj_test_1/chromedriver/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 15)

def extract_emails_from_page(source):
    """Dùng regex tìm tất cả email trong page_source"""
    found_emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", source)
    return list(set(found_emails)) if found_emails else []

def get_emails_from_website(url):
    """Mở website và tìm email cả trang chính + trang Contact"""
    emails = []
    try:
        # Mở trang chính
        driver.execute_script("window.open(arguments[0]);", url)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(5)

        page_source = driver.page_source
        emails.extend(extract_emails_from_page(page_source))

        # Tìm link Contact
        links = driver.find_elements(By.TAG_NAME, "a")
        contact_links = []
        for link in links:
            try:
                href = link.get_attribute("href")
                if href and any(word in href.lower() for word in ["contact", "lien-he", "kontact", "kontakt"]):
                    contact_links.append(href)
            except:
                continue

        if contact_links:
            for clink in set(contact_links):
                try:
                    driver.get(clink)
                    time.sleep(4)
                    contact_source = driver.page_source
                    emails.extend(extract_emails_from_page(contact_source))
                except:
                    continue

    except Exception as e:
        print("❌ Không lấy được email website:", e)
    finally:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    return list(set(emails))

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
            time.sleep(1.5)
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
            time.sleep(3)

            name_el = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.DUwDvf")))
            name = name_el.text.strip()

            address = phone = website = ""
            email_list = []
            all_info = []

            # Lấy thông tin cơ bản
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
                    email_list.append(text)  # email có thể có sẵn trong Maps

            # --- Lấy website chính xác từ nút "Website" ---
            try:
                website_btn = driver.find_element(By.XPATH, '//a[contains(@aria-label, "Website")]')
                website_link = website_btn.get_attribute("href")
                if website_link and "http" in website_link:
                    if "/url?q=" in website_link:
                        website_link = website_link.split("/url?q=")[1].split("&")[0]
                    website = website_link

                    # 🔑 Quét email trong website (trang chính + contact)
                    website_emails = get_emails_from_website(website_link)
                    email_list.extend(website_emails)
            except:
                pass

            # Ghép email thành 1 chuỗi
            email = ", ".join(list(set(email_list)))

            results.append({
                "Từ khóa": keyword,
                "Tên": name,
                "Địa chỉ": address,
                "Số điện thoại": phone,
                "Email": email,
                "Website": website,
                "Thông tin khác": " | ".join(all_info)
            })

            print(f"{index+1}. ✅ {name} ({website}) -> Emails: {email}")
        except Exception as e:
            print(f"❌ Lỗi tại kết quả {index+1}: {e}")
            continue

    all_results.extend(results)

# --- Lưu ra Excel ---
df = pd.DataFrame(all_results)
df.to_excel("ket_qua_travel_agent_all_belgium3.xlsx", index=False)
print("🎉 Đã lưu file ket_qua_travel_agent_all_belgium.xlsx")

# --- Thoát trình duyệt ---
driver.quit()
