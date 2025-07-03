import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

class WebDriverManager:
    @staticmethod
    def create_driver(url, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")

        # 현재 파일 기준으로 chromedriver.exe 경로 설정
        base_dir = os.path.dirname(os.path.abspath(__file__))
        driver_path = os.path.join(base_dir, "chromedriver.exe")

        if not os.path.exists(driver_path):
            raise FileNotFoundError(f"❌ 드라이버가 존재하지 않습니다: {driver_path}")

        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        return driver

    @staticmethod
    def safe_quit(driver):
        """안전하게 드라이버 종료"""
        try:
            if driver:
                driver.quit()
        except Exception as e:
            print(f"드라이버 종료 중 오류 발생: {e}")
