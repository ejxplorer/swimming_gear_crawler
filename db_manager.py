import psycopg2
from psycopg2.extras import execute_batch
import logging
from datetime import datetime

class DBManager:
    def __init__(self, db_params):
        self.db_params = db_params
        self.conn = None
    
    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.db_params)
            logging.info("데이터베이스 연결 성공")
        except Exception as e:
            logging.error(f"데이터베이스 연결 실패: {str(e)}")
            raise
    
    def disconnect(self):
        if self.conn:
            self.conn.close()
            logging.info("데이터베이스 연결 종료")
    
    def insert_gear_data(self, items):
        if not self.conn:
            raise Exception("데이터베이스 연결이 필요합니다")
            
        insert_query = """
            INSERT INTO gear_data (
                gear_key, name_ko, name_en, site_url, image_url, 
                gear_price, brand_id, created_at, updated_at
            ) 
            VALUES (
                %(gear_key)s, %(name_ko)s, %(name_en)s, %(site_url)s, 
                %(image_url)s, %(gear_price)s, %(brand_id)s, NOW(), NOW()
            )
            ON CONFLICT (gear_key, brand_id) 
            DO UPDATE SET
                name_ko = EXCLUDED.name_ko,
                name_en = EXCLUDED.name_en,
                site_url = EXCLUDED.site_url,
                image_url = EXCLUDED.image_url,
                gear_price = EXCLUDED.gear_price,
                updated_at = NOW()
        """
        
        try:
            with self.conn.cursor() as cur:
                execute_batch(cur, insert_query, items)
            self.conn.commit()
            logging.info(f"{len(items)}개 상품 데이터 저장 완료")
        except Exception as e:
            self.conn.rollback()
            logging.error(f"데이터 저장 중 오류 발생: {str(e)}")
            raise