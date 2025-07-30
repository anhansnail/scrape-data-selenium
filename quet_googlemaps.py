import requests
import pandas as pd
import time

# 👉 CẤU HÌNH
API_KEY = 'AIzaSyAvfy-RlboJjc2405Q99uzXxb410Mf3Hjk'  # Thay bằng API Key Google Maps của bạn
query = 'spa Da Nang'           # Từ khóa tìm kiếm (có thể đổi thành cafe, travel agency, v.v.)
location = '16.0471,108.2068'   # Vị trí trung tâm tìm kiếm (ví dụ Đà Nẵng)
radius = 5000                   # Bán kính tìm kiếm (mét)
max_results = 50               # Giới hạn số kết quả bạn muốn thu thập

# 👉 HÀM LẤY DANH SÁCH PLACE_ID
def get_places(query, location, radius):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "location": location,
        "radius": radius,
        "key": API_KEY
    }
    results = []
    while url and len(results) < max_results:
        res = requests.get(url, params=params)
        data = res.json()
        results.extend(data.get("results", []))
        next_page_token = data.get("next_page_token")
        if next_page_token:
            time.sleep(2)
            url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?pagetoken={next_page_token}&key={API_KEY}"
            params = {}
        else:
            break
    return results[:max_results]

# 👉 HÀM LẤY CHI TIẾT
def get_details(place_id):
    url = f"https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,formatted_address,formatted_phone_number,website",
        "key": API_KEY
    }
    res = requests.get(url, params=params)
    return res.json().get("result", {})

# 👉 BẮT ĐẦU CHẠY
def main():
    raw_places = get_places(query, location, radius)
    final_data = []

    for place in raw_places:
        place_id = place.get("place_id")
        details = get_details(place_id)

        final_data.append({
            "Tên": details.get("name"),
            "Địa chỉ": details.get("formatted_address"),
            "Số điện thoại": details.get("formatted_phone_number"),
            "Website": details.get("website"),
        })

        print(f"✅ Đã lấy: {details.get('name')}")

    # 👉 LƯU FILE
    df = pd.DataFrame(final_data)
    df.to_excel("doanh_nghiep_google_maps.xlsx", index=False)
    print("🎉 Đã lưu file doanh_nghiep_google_maps.xlsx")

if __name__ == "__main__":
    main()
