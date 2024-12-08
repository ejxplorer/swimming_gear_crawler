import json
import requests
import logging
import re
import time
import random
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def crawl_nike_swimsuits(url):
    logging.info(f"크롤링 시작: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logging.debug(f"HTTP 상태 코드: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')
        logging.debug("페이지 파싱 완료")
        items = []
        
        products = soup.select('.item_gallery_type li')
        
        for product in products:
            try:
                # 상품 ID
                product_link = product.select_one('.item_photo_box a')['href']
                gear_key = re.search(r'goodsNo=(\d+)', product_link).group(1)

                # 상품명
                korean_name = product.select_one('.item_name').text.strip()
                english_name = product.select_one('.num_model').text.strip()
                
                # 가격 정보
                price_element = product.select_one('.item_price span')
                if price_element:
                    # 숫자만 추출
                    gear_price = re.sub(r'[^\d]', '', price_element.text)
                
                # 이미지 URL
                image = product.select_one('.item_photo_box img')['src']
                if not image.startswith('http'):
                    image = 'https://www.swimmetro.co.kr' + image
                
                item = {
                    'gear_key': gear_key,
                    'name_ko': korean_name,
                    'name_en': english_name,
                    'site_url': f"https://www.swimmetro.co.kr/goods/goods_view.php?goodsNo={gear_key}",
                    'image_url': image,
                    'gear_price': gear_price,
                    'brand_id': 3  # Swimmetro의 brand_id
                }
                items.append(item)
   
            except Exception as e:
                logging.error(f"상품 처리 중 오류 발생: {str(e)}")
                continue
        
        logging.info(f"크롤링 완료. 총 {len(items)}개 상품 수집")
        return items
        
    except Exception as e:
        logging.error(f"크롤링 중 에러 발생: {str(e)}")
        return []



if __name__ == "__main__":
    page = 1
    total_items = []
    
    while page == 1 or len(result) > 0:
        url = f"https://www.swimmetro.co.kr/goods/goods_list.php?cateCd=001001&page={page}"
        result = crawl_nike_swimsuits(url)
        
        for item in result:
            total_items.append(item)
            
        page += 1
        delay = random.uniform(2, 4)  # 2~4초 사이의 랜덤한 시간
        time.sleep(delay)
        
        print("-" * 50)
        

    # 결과 출력
    print(f"\n=== 최종 {len(total_items)}개 상품 수집 ===")

    # 결과를 JSON 파일로 저장
    with open('nike_swimsuits.json', 'w', encoding='utf-8') as f:
        json.dump(total_items, f, ensure_ascii=False, indent=2)
    logging.info("데이터를 'nike_swimsuits.json' 파일로 저장했습니다.\n")