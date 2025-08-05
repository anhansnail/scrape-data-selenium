import pywhatkit
import time

# Danh sách số điện thoại định dạng quốc tế
phone_numbers = [
    "+31204204000",
    "+19179990380",
    "+31619934503",
    "+31645070468",
    "+31202389200",
    "+31641072763",
    "+31850163654",
    "+31207372911",
    "+31204204000",
    "+31207529753",
    "+31642134794",
    "+31207529753",
    "+31203989398",
    "+31203086019",
    "+31207700486",
    "+31203202040",
    "+31207372911",
    "+31685313406",
    "+31206262272",
    "+31616616690"
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
    # minute = now.tm_min + 2  # gửi sau 2 phút từ bây giờ
    minute = now.tm_min + 1

    # second = now.tm_sec + 15

    print(f"Đang gửi tới {number} lúc {hour}:{minute}")
    pywhatkit.sendwhatmsg(number, message, hour, minute, wait_time=15)  # gửi sau 15s từ bây giờ
    time.sleep(15)  # đợi để đảm bảo tin nhắn được gửi
