import os
import time
import random
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
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


def sugang_click(driver, priorities=None):
    try:
        driver.switch_to.frame("Main")
        driver.switch_to.frame("pkg")

        apply_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.s-btn.s-plus:not(.s-minus)"))
        )

        print(f"총 {len(apply_buttons)}개의 수강신청 버튼을 찾았습니다.")

        # priorities 에서 지정한 순서대로 처리
        if priorities:
            button_indices = priorities
        else:
            button_indices = range(1, len(apply_buttons) + 1)

        for i in button_indices:
            try:
                #time.sleep(random.uniform(0.5, 1.0))

                print(f"\n{i}번째 과목 수강신청 시도 중...")

                # 프레임 재설정
                driver.switch_to.default_content()
                driver.switch_to.frame("Main")
                driver.switch_to.frame("pkg")

                # 버튼 다시 찾기
                button = driver.find_elements(By.CSS_SELECTOR, "a.s-btn.s-plus:not(.s-minus)")[i - 1]

                # 버튼 클릭
                button.click()
                print(f"{i}번째 과목 버튼 클릭 완료")

                # 첫 번째 알림창 처리
                first_alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
                print("첫 번째 알림:", first_alert.text)
                first_alert.accept()

                # 두 번째 알림창 처리
                second_alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
                print("두 번째 알림:", second_alert.text)
                second_alert.accept()

                print(f"{i}번째 과목 수강신청 완료")
                #time.sleep(1)

            except TimeoutException:
                print(f"{i}번째 과목 수강신청 중 알림창 대기 시간 초과")
                try:
                    alert = driver.switch_to.alert
                    alert.accept()
                except:
                    pass
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
    finally:
        try:
            driver.switch_to.default_content()
        except:
            pass


# MAIN: 스크립트 실행
if __name__ == "__main__":
    try:
        # 1. 웹 드라이버 설정
        driver = setup_driver()

        # 2. 로그인
        login(driver, user_id, user_pw)

        # 수강신청
        priorities = [3, 2, 4, 6, 1, 5]  # 3번 과목 먼저, 그 다음 2번, 4번, 6번 순서로 정렬은 숫자, 영어, 한글 순
        sugang_click(driver, priorities)

        # 3. 프로그램 종료 대기
        input("Press Enter to exit and close the browser...")
    finally:
        driver.quit()
