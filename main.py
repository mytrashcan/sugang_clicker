import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
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

def sugang_click(driver):
    try:
        # 'Main' 프레임으로 전환
        driver.switch_to.frame("Main")

        # 'pkg' 프레임으로 전환
        driver.switch_to.frame("pkg")

        # 모든 신청 버튼 찾기
        apply_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.s-btn.s-plus"))
        )

        print(f"총 {len(apply_buttons)}개의 수강신청 버튼을 찾았습니다.")

        # 각 버튼에 대해 수강신청 진행
        for i, button in enumerate(apply_buttons, 1):
            try:
                print(f"\n{i}번째 과목 수강신청 시도 중...")

                # 버튼이 보이는 위치로 스크롤
                driver.execute_script("arguments[0].scrollIntoView(true);", button)
                time.sleep(0.2)  # 스크롤 완료 대기

                # 버튼 클릭
                button.click()

                # 첫 번째 알림창 처리 (수강신청 확인)
                first_alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
                print("첫 번째 알림:", first_alert.text)
                first_alert.accept()

                # 두 번째 알림창 처리 (수강신청 완료)
                second_alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
                print("두 번째 알림:", second_alert.text)
                second_alert.accept()

                print(f"{i}번째 과목 수강신청 완료")
                time.sleep(0.2)  # 다음 과목 신청 전 잠시 대기

            except TimeoutException:
                print(f"{i}번째 과목 수강신청 중 알림창 대기 시간 초과")
                continue
            except Exception as e:
                print(f"{i}번째 과목 수강신청 중 오류 발생: {str(e)}")
                continue

        return 0

    except TimeoutException:
        print("프레임 또는 버튼을 찾을 수 없습니다 (시간 초과)")
        return 1
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return 1

# MAIN: 스크립트 실행
if __name__ == "__main__":
    try:
        # 1. 웹 드라이버 설정
        driver = setup_driver()

        # 2. 로그인
        login(driver, user_id, user_pw)

        # 3. 과목 클릭
        sugang_click(driver)
        
        # 3. 프로그램 종료 대기
        input("Press Enter to exit and close the browser...")
    finally:
        driver.quit()
