from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class WebDriverManager:
    """웹드라이버 생성 및 관리를 담당하는 클래스"""

    @staticmethod
    def create_driver(url, headless=False):
        """웹드라이버 생성 및 초기화"""
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")

        service = Service(ChromeDriverManager().install())
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
