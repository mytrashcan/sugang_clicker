import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# .env 파일에서 사용자 정보 및 URL 로드
load_dotenv()
user_id = os.getenv("user_id")
user_pw = os.getenv("user_pw")
url = os.getenv("url")


# STEP 1: 환경 설정
def setup_driver():
    from selenium.webdriver.chrome.options import Options
    options = Options()
    # 필요 시 headless 모드 비활성화
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)  # .env 파일의 URL 로드
    return driver


# STEP 2: 로그인 처리
def login(driver, user_id, user_pw):
    # ID 입력
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "id"))).send_keys(user_id) # ID 바뀔가능성 있음 -> CSS SELECTOR 로 바꿀까 생각중
    # 비밀번호 입력
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "passwd"))).send_keys(user_pw)
    # 로그인 버튼 클릭
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btn_login"))).click()

def sugang_click():
    #Work In Process
    return 0


# MAIN: 스크립트 실행
if __name__ == "__main__":
    try:
        # 1. 웹 드라이버 설정
        driver = setup_driver()

        # 2. 로그인
        login(driver, user_id, user_pw)

        # 3. 프로그램 종료 대기
        input("Press Enter to exit and close the browser...")
    finally:
        driver.quit()
