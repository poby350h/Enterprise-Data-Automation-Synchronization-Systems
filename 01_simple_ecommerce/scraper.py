import requests
from bs4 import BeautifulSoup
import csv
import datetime
import os
import time
import random

# ==================================================================================
# [Portfolio] High-Volume E-commerce Scraper (대용량 이커머스 스크래핑 봇)
#
# ----------------------------------------------------------------------------------
# 🌍 Developer Profile:
#    - Native Korean Developer based in Canada (한국인 개발자)
#    - Expert in scraping Korean platforms (Olive Young,Naver, Coupang,  etc.)
#
# 🎯 Target Site (타겟 사이트):
#    - Olive Young (Korea's No.1 Health & Beauty Store) / 올리브영
#    - Similar to Sephora or Boots (세포라, 부츠와 유사한 대형 커머스)
#
# 🛡️ Key Features (핵심 기능):
#    - Anti-Bot Bypass (봇 탐지 회피 기술 적용)
#    - Dynamic Tag Parsing (할인, 쿠폰 등 동적 태그 처리)
#    - UTF-8 Encoding Support (한글 데이터 깨짐 방지 완벽 처리)
#
# ⚠️ Privacy Note:
#    - Real URLs and Selectors are masked for security/NDA reasons.
#    - 실제 URL과 CSS 선택자는 보안 및 고객사 보호를 위해 가림 처리되었습니다.
# ==================================================================================

def get_headers():
    """
    Configures User-Agent to mimic a real browser to avoid blocking.
    (서버 차단을 피하기 위해 실제 브라우저처럼 위장하는 헤더 설정)
    """
    return {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.target-commerce-site.com/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
        'Connection': 'keep-alive'
    }

def scrape_ranking_data():
    # 1. Target URL (Masked)
    url = "https://www.target-commerce-site.com/best/ranking"
    
    print("Initializing Scraper... (스크래퍼 시작 중)")
    
    try:
        # 2. Anti-Bot Delay (Random sleep)
        # Random delay simulates human behavior. (사람처럼 보이게 랜덤 대기)
        sleep_time = random.uniform(1.0, 3.0)
        time.sleep(sleep_time)
        print(f"Waiting for {sleep_time:.2f} seconds...")
        
        # 3. Request
        response = requests.get(url, headers=get_headers())
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 4. Parsing Logic (Selectors masked)
        items = soup.select("ul.product_list > li")
        
        # Prepare CSV Header (Korean/English Bilingual Support)
        data_rows = [['Date', 'Rank', 'Brand', 'Product Name', 'Price', 'Tags']]
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"Found {len(items)} items. Extracting data...")

        for idx, item in enumerate(items, 1):
            # Safe Extraction with Error Handling
            try:
                brand = item.select_one(".brand_name").text.strip()
                name = item.select_one(".product_name").text.strip()
                price = item.select_one(".price_value").text.strip()
                
                # Handling dynamic tags (e.g., Sale, Coupon)
                tags = [t.text for t in item.select(".promotion_tags span")]
                tags_str = ", ".join(tags)
                
                data_rows.append([current_time, idx, brand, name, price, tags_str])
            except AttributeError:
                continue # Skip invalid rows

        # 5. Save to CSV (utf-8-sig for Korean characters)
        filename = "result_sample.csv"
        with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data_rows)
            
        print(f"✅ Success! Data saved to {filename}")

    except Exception as e:
        print(f"❌ Error occurred: {e}")

if __name__ == "__main__":
    scrape_ranking_data()