from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re
import openpyxl

# === Cấu hình đường dẫn ChromeDriver ===
chrome_driver_path = "D:/prj_test_1/chromedriver/chromedriver.exe"
service = Service(executable_path=chrome_driver_path)
options = Options()
# options.add_argument("--headless")  # Nếu muốn chạy ẩn

driver = webdriver.Chrome(service=service, options=options)

# === Tạo file Excel ===
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Thông tin tuyển dụng"
ws.append(["Link", "Thông tin công ty", "Email", "Số điện thoại"])

# === Bắt đầu từ trang 22, duyệt nhiều trang ===
start_page = 421
end_page = 480  # Thay số trang bạn muốn quét

for page in range(start_page, end_page + 1):
    url = f"https://vieclambacninhso1.vn/viec-lam-trang-{page}.html?per-page=15"
    print(f"\n📄 Đang xử lý: {url}")
    driver.get(url)
    time.sleep(3)

    job_links = []
    job_elements = driver.find_elements(By.CSS_SELECTOR, ".job-ad-item .item-info .ad-info a")
    for el in job_elements:
        link = el.get_attribute("href")
        if link:
            job_links.append(link)

    print(f"🔗 Tìm thấy {len(job_links)} tin tuyển dụng.")

    # Duyệt từng tin chi tiết
    link1 = ""
    for link in job_links:
        if link != link1:
            driver.get(link)
            time.sleep(2)

            company_links = driver.find_elements(By.CSS_SELECTOR, ".company-info li a")
            try:
                company_name = driver.find_element(By.CSS_SELECTOR, ".job-details-info .company-info h2").text.strip()
            except:
                company_name = "Không rõ"
            company_info = [el.text + " (" + el.get_attribute("href") + ")" for el in company_links]

            page_text = driver.page_source

            # Trích xuất email và điện thoại
            emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", page_text)
            phones = re.findall(r"(0|\+84)[1-9][0-9]{8}", page_text)

            email_str = ', '.join(set(emails)) if emails else "Không có"
            phone_str = ', '.join(set(phones)) if phones else "Không có"
            company_str = ', '.join(company_info) if company_info else "Không có"

            print(f"\n🔗 {link}")
            print(f"Company name: {company_name}")
            print(f"🏢 Company info(s): {company_str}")
            print(f"📧 Email(s): {email_str}")
            # print(f"📞 Phone(s): {phone_str}")

            # Ghi vào Excel
            ws.append([company_name, company_str, email_str, phone_str])

            link1 = link

# === Lưu Excel ===
excel_filename = f"viec_lam_bac_ninh_so_1'{end_page}'.xlsx"
wb.save(excel_filename)
print(f"\n✅ Đã lưu dữ liệu vào '{excel_filename}'")

# Đóng trình duyệt
driver.quit()
