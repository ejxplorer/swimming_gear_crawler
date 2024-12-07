import requests, logging, json, re, time, random
from bs4 import BeautifulSoup


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


# 한글/영문 이름 분리 메서드
def split_product_name(full_name):
    pattern = r'(.*?)\s*\((.*?)\)'  # 괄호 앞의 모든 텍스트와 괄호 안의 텍스트를 그룹으로 캡처
    match = re.match(pattern, full_name)
    
    if match:
        korean_name = match.group(1).strip()
        english_name = match.group(2).strip()
        if bool(re.search('[가-힣]', english_name)):
            return full_name, ''
        return korean_name, english_name
    else:
        return full_name, ''  # 괄호가 없는 경우 전체를 한글 이름으로 처리
    
    
def crawl_speedo_swimsuits(url):
    logging.info(f"크롤링 시작: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logging.debug(f"HTTP 상태 코드: {response.status_code}")

        
        # # HTML 파일로 저장
        # with open('speedo_page.html', 'w', encoding='utf-8') as f:
        #     f.write(response.text)
        # logging.info("HTML을 'speedo_page.html' 파일로 저장했습니다.")

        
        soup = BeautifulSoup(response.text, 'html.parser')
        logging.debug("페이지 파싱 완료")
        
        items = []
        products = soup.select('.prdList .prdList__item')
        
        for product in products:
            try:
                # 상품 ID
                product_link = product.select_one('.thumbnail a')['href']
                gear_key = product_link.split('/')[3]

                # 상품명
                name_element = product.select_one('.name a > span:not(.title)')
                if name_element:
                    full_name = name_element.text.strip()
                    korean_name, english_name = split_product_name(full_name)
                else:
                    print("상품명을 찾을 수 없습니다.")
                
                # 가격 정보
                price_element = product.select_one('.description')
                if price_element:
                    gear_price = price_element.get('ec-data-price', 0)
                
                # 이미지 URL
                image = product.select_one('.thumbnail img')['src']
                if not image.startswith('http'):
                    image = 'https:' + image
                
                item = {
                    'gear_key': gear_key,
                    'name_ko': korean_name,
                    'name_en': english_name,
                    'site_url': f"https://speedo.co.kr/product/detail/{gear_key}",
                    'image_url': image,
                    'gear_price': gear_price,
                    'brand_id': 1
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

# # 실행
# if __name__ == "__main__":
#     page = 1
#     total_items = []
    
#     while page == 1 or len(result) > 0:
#         url = f"https://speedo.co.kr/category/onepiece/29/sort_method=5&page={page}"
#         result = crawl_speedo_swimsuits(url)
        
#         for item in result:
#             total_items.append(item)
            
#         page += 1
#         delay = random.uniform(2, 4)  # 2~4초 사이의 랜덤한 시간
#         time.sleep(delay)
        
#         print("-" * 50)
        

#     # 결과 출력
#     print(f"\n=== 최종 {len(total_items)}개 상품 수집 ===")

#     # 결과를 JSON 파일로 저장
#     with open('speedo_swimsuits.json', 'w', encoding='utf-8') as f:
#         json.dump(total_items, f, ensure_ascii=False, indent=2)
#     logging.info("데이터를 'speedo_swimsuits.json' 파일로 저장했습니다.\n")