import logging
import time
import random
from speedo.speedo_crawler import crawl_speedo_swimsuits
from jolyn.jolyn_crawler import crawl_jolyn_swimsuits
from nike.nike_crawler import crawl_nike_swimsuits
from db_manager import DBManager

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def crawl_brand(crawler_func, base_url, db_manager):
    page = 1
    total_items = []
    
    while True:
        url = f"{base_url}&page={page}"
        result = crawler_func(url)
        
        if not result:  # 결과가 없으면 종료
            break
            
        db_manager.insert_gear_data(result)
        total_items.extend(result)
        
        page += 1
        delay = random.uniform(2, 4)
        time.sleep(delay)
        
        print("-" * 50)
    
    return total_items



def main():
    # 데이터베이스 연결 정보
    db_params = {
        "dbname": "swimming_db",
        "user": "sw_crawler",
        "password": "crawlerrr!",
        "host": "localhost",
        "port": "5432"
    }
    
    db_manager = DBManager(db_params)
    
    try:
        db_manager.connect()
        total_count = 0
        
        # # Speedo 크롤링
        # speedo_url = "https://speedo.co.kr/category/onepiece/29/sort_method=5"
        # speedo_items = crawl_brand(crawl_speedo_swimsuits, speedo_url, db_manager)
        # print(f"\n=== Speedo 최종 {len(speedo_items)}개 상품 수집 및 저장 완료 ===")
        # total_count += len(speedo_items)
        
        # # Jolyn 크롤링
        # jolyn_url = "https://jolynkorea.co.kr/category/onesies/46/sort_method=5"
        # jolyn_items = crawl_brand(crawl_jolyn_swimsuits, jolyn_url, db_manager)
        # print(f"\n=== Jolyn 최종 {len(jolyn_items)}개 상품 수집 및 저장 완료 ===")
        # total_count += len(jolyn_items)

        # Nike 크롤링
        nike_url = "https://www.swimmetro.co.kr/goods/goods_list.php?cateCd=001001"
        nike_items = crawl_brand(crawl_nike_swimsuits, nike_url, db_manager)
        print(f"\n=== Nike 최종 {len(nike_items)}개 상품 수집 및 저장 완료 ===")
        total_count += len(nike_items)
        
        print(f"\n=== 전체 {total_count}개 상품 수집 및 저장 완료 ===")
        
    except Exception as e:
        logging.error(f"에러 발생: {str(e)}")
    
    finally:
        db_manager.disconnect()

if __name__ == "__main__":
    main()