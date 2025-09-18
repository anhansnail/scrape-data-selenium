from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import pandas as pd

# Danh sách URL cần crawl
# urls = [
#     "https://www.tuyendunghaiphong.vn/viec-lam/910383/tuyen-nhan-vien-media-chup-chinh-anh-quay-dung-video-nganh-xay-dung",
#     "https://www.tuyendunghaiphong.vn/viec-lam/910250/tuyen-ky-su-qa-qc-lam-viec-tai-phan-xuong-thanh-pham",
#     "https://www.tuyendunghaiphong.vn/viec-lam/910374/tuyen-dung-nhan-vien-hanh-chinh-nhan-su-uu-tien-biet-tieng-nhat-tuong-duong-n3"
# ]
urls = pd.read_excel("input.xlsx")["url"].tolist()

# Khởi tạo driver
driver = webdriver.Chrome()

results = []

for url in urls:
    driver.get(url)
    time.sleep(1)  # chờ trang load

    try:
        # Lấy nội dung trong class chitiet-content
        content = driver.find_element(By.ID, "thongtintuyendung").text


        if content:
            results.append({"URL": url, "Content": content})
            print(url)
    except Exception as e:
        print(url, "-> Lỗi:", e)
        results.append({"URL": url, "Content": ""})

driver.quit()

# Xuất ra file Excel
df = pd.DataFrame(results)
df.to_excel("emails_tuyendung_22tuyendung_haiphong501to620.xlsx", index=False)

print("✅ Đã lưu kết quả vào emails_tuyendung.xlsx")
