import pyautogui
import time
import pandas as pd

# Cấu hình
csv_file = 'zalocontacts.csv'
delay_between_messages = 2  # giây
message_template = "Chào {name}, đây là tin nhắn tự động."

# Đọc danh sách
df = pd.read_csv(csv_file)

# Nhắc mở Zalo
print("➡️ Mở Zalo App và để ở chế độ hoạt động (không thu nhỏ). Bắt đầu trong 5 giây...")
time.sleep(5)

# Vòng lặp gửi tin
for index, row in df.iterrows():
    name = row['name']
    phone = str(row['phone'])

    try:
        # Tìm người
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(1)
        pyautogui.write(phone)
        time.sleep(2)
        pyautogui.press('enter')  # mở chat
        time.sleep(2)

        # Click vào ô nhập (dán tọa độ bạn đã đo được)
        pyautogui.click(x=500, y=700)  # 🛠 THAY tọa độ đúng với máy bạn
        time.sleep(0.5)

        # Nhập và gửi tin nhắn
        message = message_template.format(name=name)
        pyautogui.write(message)
        time.sleep(0.5)
        pyautogui.press('enter')

        print(f"✅ Đã gửi tin cho {name} ({phone})")
        time.sleep(delay_between_messages)
    except Exception as e:
        print(f"❌ Lỗi khi gửi cho {name} ({phone}): {e}")
