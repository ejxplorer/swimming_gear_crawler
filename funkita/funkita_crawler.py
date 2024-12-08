import requests
import logging
import re
import time
import random
import json
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def crawl_funkita_swimsuits(url):
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
        products = soup.select('.xans-product-listnormal li')
        
        for product in products:
            try:
                # 상품 ID
                product_link = product.select_one('.item_img a')['href']
                gear_key = re.search(r'product_no=(\d+)', product_link).group(1)
                # print(f'111 {product_link}')
                product_link = f"https://funkytrunks-korea.com/product/detail.html?product_no={gear_key}"

                # 상품명
                name_element = product.select_one('.item_info .name')
                if name_element:
                    full_name = name_element.text.strip()
                    pattern = r'펑키타 코리아\s+(.*?)\s*\(([\w_\s]+)\)'
                    match = re.search(pattern, full_name)
                    name_en = f"{match.group(1)} ({match.group(2)})"
                else:
                    continue
                
                # 가격 정보
                price_element = product.select_one('.price')
                if price_element:
                    # span 태그를 제거하고 남은 텍스트만 추출
                    for span in price_element.select('span'):
                        span.decompose()
                    # 숫자만 추출
                    gear_price = re.sub(r'[^\d]', '', price_element.text)
                else:
                    gear_price = "0"
                
                # 이미지 URL
                image = product.select_one('.item_img a img')['src']
                if not image.startswith('http'):
                    image = 'https:' + image
                
                item = {
                    'gear_key': gear_key,
                    'name_ko': '',
                    'name_en': name_en,
                    'site_url': f"https://funkytrunks-korea.com/product/detail.html?product_no={gear_key}",
                    'image_url': image,
                    'gear_price': gear_price,
                    'brand_id': 4 
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
    base_url = "https://funkytrunks-korea.com/product/list2-women-col3.html"
    results = []

    page = 1
    
    while page<4:
        url = f"{base_url}?cate_no=37&page={page}"
        items = crawl_funkita_swimsuits(url)
        
        if not items:  # 더 이상 상품이 없으면 종료
            break
            
        results.extend(items)
        logging.info(f"페이지 {page} 완료")
        page += 1
        
        # 페이지 간 딜레이
        time.sleep(random.uniform(1, 4))

    # 결과를 JSON 파일로 저장
    if results:
        with open('funkita_swimsuits.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        logging.info(f"데이터가 funkita_swimsuits.json 파일로 저장되었습니다. 총 {len(results)}개 상품")