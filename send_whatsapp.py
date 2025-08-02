import pywhatkit
import time

# Danh sách số điện thoại định dạng quốc tế
phone_numbers = [
    "+31615467640",
    "+31643413799",
    "+31689937548"
]

# Nội dung tin nhắn
message = ("Hello,I’m Minh Anh from FTC Viet Nam travel, a Vietnam-based travel agency specializing in inbound tourism."
           "We are looking to partner with travel agencies in the Netherlands who are interested in offering unique travel experiences in Vietnam to their customers."
           "If you’re open to collaboration, I’d love to share more details and explore how we can work together to bring more Dutch travelers to Vietnam."
            "Thank you, and I look forward to hearing from you!"
            "Best regards,"
            "Minh Anh"
            "Contact: whatsapp/phone: +84 333 409 581. Email: visaftc2024@gmail.com")

for number in phone_numbers:
    now = time.localtime()
    hour = now.tm_hour
    minute = now.tm_min + 2  # gửi sau 2 phút từ bây giờ

    print(f"Đang gửi tới {number} lúc {hour}:{minute}")
    pywhatkit.sendwhatmsg(number, message, hour, minute, wait_time=10)
    time.sleep(30)  # đợi để đảm bảo tin nhắn được gửi
