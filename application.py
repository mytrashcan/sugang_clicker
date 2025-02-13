import os
import time
from datetime import datetime
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import Config
from web_driver_manager import WebDriverManager
from time_manager import TimeManager
from sugang_handler import SugangHandler


class SugangApplication:
    """수강신청 애플리케이션의 메인 클래스"""

    def __init__(self):
        load_dotenv()
        self.user_id = os.getenv("user_id")
        self.user_pw = os.getenv("user_pw")
        self.sugang_url = os.getenv("url")
        self.time_url = os.getenv("time_url")

        self.time_driver = None
        self.sugang_driver = None
        self.sugang_handler = None

    def initialize_drivers(self):
        """드라이버 초기화"""
        self.time_driver = WebDriverManager.create_driver(
            self.time_url, headless=True)
        self.sugang_driver = WebDriverManager.create_driver(
            self.sugang_url)
        self.sugang_handler = SugangHandler(self.sugang_driver)

    def prepare_login(self):
        """로그인 준비"""
        id_field = WebDriverWait(self.sugang_driver, Config.DEFAULT_TIMEOUT).until(
            EC.presence_of_element_located((By.ID, Config.SELECTORS['login_id'])))
        pw_field = WebDriverWait(self.sugang_driver, Config.DEFAULT_TIMEOUT).until(
            EC.presence_of_element_located((By.ID, Config.SELECTORS['login_pw'])))

        id_field.send_keys(self.user_id)
        pw_field.send_keys(self.user_pw)
        return WebDriverWait(self.sugang_driver, Config.DEFAULT_TIMEOUT).until(
            EC.presence_of_element_located((By.ID, Config.SELECTORS['login_btn'])))

    def get_current_time(self):
        """현재 시간을 가져오는 메서드"""
        try:
            time_element = WebDriverWait(self.time_driver, Config.DEFAULT_TIMEOUT).until(
                EC.presence_of_element_located((By.ID, Config.SELECTORS['time_area']))
            )
            korean_time = time_element.text.strip()
            return TimeManager.convert_korean_time_to_hms(korean_time)
        except Exception as e:
            print(f"현재 시간 가져오기 실패: {e}")
            return None

    def run(self, target_time, interval=Config.DEFAULT_INTERVAL):
        """메인 실행 함수"""
        try:
            self.initialize_drivers()
            login_btn = self.prepare_login()
            print("로그인 정보 입력 완료, 대기 중...")

            while True:
                current_time = self.get_current_time()
                if current_time and TimeManager.is_target_time_reached(current_time, target_time):
                    print("\n목표 시간 도달! 로그인 시도...")
                    WebDriverManager.safe_quit(self.time_driver)

                    login_btn.click()
                    self.sugang_handler.process_sugang(Config.PRIORITIES)
                    break

                time.sleep(interval)

        except Exception as e:
            print(f"프로그램 실행 중 오류: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        """리소스 정리"""
        WebDriverManager.safe_quit(self.time_driver)
        WebDriverManager.safe_quit(self.sugang_driver)
