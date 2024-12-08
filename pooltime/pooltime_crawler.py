import requests
import logging
import json
import time
import random

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def fetch_pooltime_swimsuits(url):
    logging.info(f"API 호출 시작: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logging.debug(f"HTTP 상태 코드: {response.status_code}")
        
        json_data = response.json()
        products = json_data.get('rtn_data', {}).get('data', [])
        
        items = []
        for product in products:
            try:
                item = {
                    'gear_key': product.get('product_no'),
                    'name_ko': product.get('product_name'),
                    'name_en': '',
                    'gear_price': product.get('product_price'),
                    'image_url': 'https:' + product.get('image_medium'),
                    'site_url': f"https://m.pooltime.kr/product/detail.html?product_no={product.get('product_no')}",
                    'brand_id': 5  # Pooltime의 brand_id
                }
                items.append(item)
                
            except Exception as e:
                logging.error(f"상품 처리 중 오류 발생: {str(e)}")
                continue
        
        logging.info(f"데이터 수집 완료. 총 {len(items)}개 상품")
        return items
        
    except Exception as e:
        logging.error(f"API 호출 중 에러 발생: {str(e)}")
        return []
    

if __name__ == "__main__":
    base_url = "https://m.pooltime.kr/exec/front/Product/ApiProductNormal"
    url = f"{base_url}?cate_no=97&supplier_code=S0000000&count=200"
    # url = f"{base_url}?cate_no=97&supplier_code=S0000000&page=0bInitMore=T&count=10"
    results = fetch_pooltime_swimsuits(url)
    
    # 결과를 JSON 파일로 저장
    if results:
        with open('pooltime_swimsuits.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        logging.info(f"데이터가 pooltime_swimsuits.json 파일로 저장되었습니다. 총 {len(results)}개 상품")