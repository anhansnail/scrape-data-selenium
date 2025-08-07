# import pywhatkit
# import time
#
# # Danh sách số điện thoại định dạng quốc tế
# phone_numbers = [
#     "+31204204000",
#     "+19179990380",
#     "+31619934503",
#     "+31645070468",
#     "+31202389200",
#     "+31641072763",
#     "+31850163654",
#     "+31207372911",
#     "+31204204000",
#     "+31207529753",
#     "+31642134794",
#     "+31207529753",
#     "+31203989398",
#     "+31203086019",
#     "+31207700486",
#     "+31203202040",
#     "+31207372911",
#     "+31685313406",
#     "+31206262272",
#     "+31616616690"
# ]
#
#
# # Nội dung tin nhắn
# message = ("Hello,I’m Minh Anh from FTC Viet Nam travel, a Vietnam-based travel agency specializing in inbound tourism."
#            "We are looking to partner with travel agencies in your country who are interested in offering unique travel experiences in Vietnam to their customers."
#            "If you’re open to collaboration, I’d love to share more details and explore how we can work together to bring more Dutch travelers to Vietnam."
#             "Thank you, and I look forward to hearing from you!"
#             "Best regards,"
#             "Minh Anh"
#             "Contact: whatsapp/phone: +84 333 409 581. Email: visaftc2024@gmail.com")
#
# for number in phone_numbers:
#     now = time.localtime()
#     hour = now.tm_hour
#     # minute = now.tm_min + 2  # gửi sau 2 phút từ bây giờ
#     minute = now.tm_min + 1
#
#     # second = now.tm_sec + 15
#
#     print(f"Đang gửi tới {number} lúc {hour}:{minute}")
#     pywhatkit.sendwhatmsg(number, message, hour, minute, wait_time=15)  # gửi sau 15s từ bây giờ
#     time.sleep(15)  # đợi để đảm bảo tin nhắn được gửi
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.parse import quote
import os

# === Cấu hình ===
chrome_driver_path = "D:/prj_test_1/chromedriver/chromedriver.exe"
data_file = "C:/Users/Admin/IdeaProjects/scrape_data/contacts.xlsx"
tin_nhan_gui = "Xin chào, tôi muốn liên hệ với bạn qua WhatsApp. Cảm ơn!"
thoi_gian_cho_moi_tin = 5  # giây

# === Hàm đọc danh sách số điện thoại từ Excel hoặc CSV ===
def read_phone_numbers(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Không tìm thấy file: {file_path}")
    if file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
    elif file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        raise ValueError("Chỉ hỗ trợ định dạng .xlsx hoặc .csv")

    print("📌 Các cột trong file:", df.columns)
    # Tìm cột có tên giống "sdt" (không phân biệt hoa thường)
    sdt_col = next((col for col in df.columns if str(col).lower().strip() in ['sdt', 'phone', 'số điện thoại']), None)
    if not sdt_col:
        raise ValueError("❌ Không tìm thấy cột số điện thoại! (cần tên là 'sdt', 'phone', 'số điện thoại')")

    phones = df[sdt_col].dropna().astype(str).tolist()
    print(f"🔢 Đã đọc {len(phones)} số điện thoại từ file `{file_path}`.")
    return phones

# === Hàm gửi tin nhắn WhatsApp ===
def send_whatsapp_message(phone, message, driver):
    try:
        print(f"➡️ Đang gửi tin đến: {phone}")
        url = f"https://wa.me/{phone}?text={quote(message)}"
        driver.execute_script(f"window.open('{url}', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(8)  # Đợi trang WhatsApp load

        try:
            # Tìm nút Gửi (Send) và nhấn
            send_btn = driver.find_element(By.XPATH, "//div[@role='button'][@data-testid='compose-btn-send']")
            send_btn.click()
            print("✅ Đã gửi tin nhắn.")
        except:
            print("⚠️ Không tìm thấy nút gửi (số có thể chưa đăng ký WhatsApp).")

        time.sleep(thoi_gian_cho_moi_tin)  # Chờ giữa các tin nhắn
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except Exception as e:
        print(f"❌ Lỗi khi gửi cho {phone}: {e}")

# === Cấu hình và khởi động trình duyệt ===
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--start-maximized")

try:
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
    driver.get("https://web.whatsapp.com")
    print("⏳ Vui lòng quét mã QR để đăng nhập WhatsApp...")
    input("✅ Sau khi quét xong, nhấn Enter để tiếp tục...")
except Exception as e:
    print(f"❌ Không thể khởi động trình duyệt: {e}")
    exit()

# === Chạy gửi tin nhắn ===
try:
    phone_numbers = read_phone_numbers(data_file)
    for phone in phone_numbers:
        phone = phone.strip().replace(" ", "").replace(".", "").replace("-", "")
        if phone.startswith("+"):
            phone = phone[1:]
        send_whatsapp_message(phone, tin_nhan_gui, driver)
except Exception as e:
    print(f"❌ Lỗi trong quá trình gửi tin: {e}")

driver.quit()
print("🏁 Hoàn tất gửi tin.")
