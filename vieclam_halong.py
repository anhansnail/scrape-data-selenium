import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import quote

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_updated_max(soup):
    articles = soup.find_all("article", class_="blog-post")
    if not articles:
        return None
    last_time_tag = articles[-1].find("time", class_="published")
    if last_time_tag:
        return last_time_tag["datetime"]
    return None

# Khoảng trang cần lấy
START_PAGE = 3
END_PAGE = 60

# Trang đầu tiên
page = 1
next_url = "https://www.vieclamhalong.com/search?max-results=50"
all_posts = []
visited_links = set()

while page <= END_PAGE:
    print(f"📄 Đang xử lý trang {page}: {next_url}")
    res = requests.get(next_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    articles = soup.find_all("article", class_="blog-post")
    if not articles:
        print("⛔ Không tìm thấy bài viết nào. Kết thúc.")
        break

    if page >= START_PAGE:
        for article in articles:
            a_tag = article.find("h2", class_="post-title").find("a")
            title = a_tag.get_text(strip=True)
            url = a_tag["href"]
            if url in visited_links:
                continue
            visited_links.add(url)

            date_tag = article.find("time", class_="published")
            post_date = date_tag["datetime"] if date_tag else "Không rõ ngày"

            try:
                detail_res = requests.get(url, headers=headers, timeout=10)
                detail_soup = BeautifulSoup(detail_res.text, "html.parser")
                body_tag = detail_soup.find("div", class_="post-body post-content")
                content = body_tag.get_text(separator="\n", strip=True) if body_tag else "Không có nội dung"

                all_posts.append({
                    "Tiêu đề": title,
                    "Link": url,
                    "Ngày đăng": post_date,
                    "Nội dung chi tiết": content
                })

                print(f"✅ Trang {page} | {title}")
                time.sleep(1)

            except Exception as e:
                print(f"❌ Lỗi khi xử lý bài: {url}: {e}")

    # Lấy updated-max để truy cập trang tiếp theo
    updated_max = get_updated_max(soup)
    if not updated_max:
        print("❌ Không tìm thấy updated-max, kết thúc.")
        break

    updated_time_encoded = quote(updated_max, safe='')
    next_url = f"https://www.vieclamhalong.com/search?updated-max={updated_time_encoded}&max-results=50"
    page += 1

# Lưu ra file Excel
df = pd.DataFrame(all_posts)
df.to_excel(f"vieclamhalong_page_{START_PAGE}_to_{END_PAGE}.xlsx", index=False)
print(f"🎉 Đã lưu vào vieclamhalong_page_{START_PAGE}_to_{END_PAGE}.xlsx")
