from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import openpyxl
import time
import re

# Đường dẫn tới ChromeDriver
driver_path = "D:/prj_test_1/chromedriver/chromedriver.exe"

# Mở Chrome đã đăng nhập Facebook sẵn: profile path:  C:\Users\Admin\AppData\Local\Temp\scoped_dir7660_1506002762\Default
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:/Users/Admin/AppData/Local/Temp/Chrome/scoped_dir7660_1506002762")  # Đường dẫn thư mục Chrome của bạn
options.add_argument("profile-directory=Default")  # Hoặc Profile 1, Profile 2 tùy theo Chrome bạn dùng
# options.add_argument("profile-directory=Profile 7")  # Hoặc Profile 1, Profile 2 tùy theo Chrome bạn dùng
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(driver_path), options=options)

# Mở nhóm Facebook
group_url = "https://www.facebook.com/groups/266467520786789"
driver.get(group_url)
time.sleep(20)

# Cuộn trang để tải thêm bài viết
for _ in range(3):  # tăng nếu muốn crawl nhiều hơn
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

# Parse nội dung
soup = BeautifulSoup(driver.page_source, "html.parser")
all_spans = soup.find_all("span")

# Tạo file Excel
wb = openpyxl.Workbook()
ws = wb.active
ws.append(["Nội dung", "Email", "SĐT"])

# Hàm trích xuất email và SĐT
def extract_email_phone(text):
    emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    phones = re.findall(r'0\d{9,10}', text)
    return ", ".join(emails), ", ".join(phones)

# Quét dữ liệu
for span in all_spans:
    try:
        text = span.get_text(strip=True)
        if "@" in text or re.search(r"0\d{9,10}", text):
            email, phone = extract_email_phone(text)
            if email or phone:
                ws.append([text, email, phone])
    except:
        continue

# Lưu Excel
wb.save("facebook_tuyendung.xlsx")
driver.quit()
print("✅ Đã lưu xong file facebook_tuyendung.xlsx")
