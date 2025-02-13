import time
import os
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# .env 파일에서 사용자 정보 및 URL 로드
load_dotenv()
user_id = os.getenv("user_id")
user_pw = os.getenv("user_pw")
sugang_url = os.getenv("url")
time_url = os.getenv("time_url")

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


def convert_korean_time_to_hms(time_str):
    """한글 시간 문자열을 HH:MM:SS 형식으로 변환"""
    try:
        # 기본값 설정
        hours = minutes = seconds = '00'

        # 시간 문자열에서 각 부분 추출
        for part in time_str.split():
            if '시' in part:
                hours = part.replace('시', '').strip().zfill(2)
            elif '분' in part:
                minutes = part.replace('분', '').strip().zfill(2)
            elif '초' in part:
                seconds = part.replace('초', '').strip().zfill(2)

        formatted_time = f"{hours}:{minutes}:{seconds}"
        return formatted_time
    except Exception as e:
        print(f"시간 변환 중 오류: {e}")
        print(f"입력된 시간 문자열: {time_str}")
        return None


def get_time_and_execute(time_url, sugang_url, target_time, interval=0.01):
    """특정 시간이 되면 로그인 및 수강신청을 실행하는 함수"""
    # 시간 확인용 브라우저 설정
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    time_driver = webdriver.Chrome(service=service, options=options)
    time_driver.get(time_url)

    # 수강신청용 브라우저 설정 및 사전 준비
    sugang_options = webdriver.ChromeOptions()
    sugang_service = Service(ChromeDriverManager().install())
    sugang_driver = webdriver.Chrome(service=sugang_service, options=sugang_options)
    sugang_driver.get(sugang_url)

    # ID/PW 미리 입력
    print("로그인 정보 미리 입력 중...")
    id_field = WebDriverWait(sugang_driver, 10).until(
        EC.presence_of_element_located((By.ID, "id")))
    pw_field = WebDriverWait(sugang_driver, 10).until(
        EC.presence_of_element_located((By.ID, "passwd")))
    login_btn = WebDriverWait(sugang_driver, 10).until(
        EC.presence_of_element_located((By.ID, "btn_login")))

    id_field.send_keys(user_id)
    pw_field.send_keys(user_pw)
    print("로그인 정보 입력 완료, 대기 중...")

    executed = False

    try:
        while not executed:
            time_element = time_driver.find_element(By.ID, "time_area")
            current_time_full = time_element.text.strip()

            time_parts = current_time_full.split()
            if len(time_parts) >= 4:
                time_part = ' '.join(time_parts[3:])
                current_time_hms = convert_korean_time_to_hms(time_part)

                if current_time_hms:
                    current_datetime = datetime.strptime(current_time_hms, "%H:%M:%S")
                    target_datetime = datetime.strptime(target_time, "%H:%M:%S")

                    print(f"\r현재 시간: {current_time_hms} | 목표 시간: {target_time}", end="")

                    if current_datetime >= target_datetime:
                        print("\n목표 시간 도달! 로그인 버튼 클릭...")
                        time_driver.quit()

                        try:
                            # 로그인 버튼 클릭 시각 기록
                            print("로그인 버튼 클릭 시도...")
                            click_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                            print(f"버튼 클릭 시각: {click_time}")
                            login_btn.click()

                            priorities = [3, 2, 4, 6, 1, 5] # 수강 우선순위 지정 정렬: 숫자, 영어, 한글
                            sugang_click(sugang_driver, priorities)
                        except Exception as e:
                            print("수강신청 과정 중 오류 발생:", e)

                        executed = True
                        break

            time.sleep(interval)


    except Exception as e:
        print("\n오류 발생:", e)

    finally:
        if 'time_driver' in locals() and time_driver:
            time_driver.quit()
        print("프로그램을 종료하려면 Enter를 눌러주세요...")
        input()
        if 'sugang_driver' in locals() and sugang_driver:
            sugang_driver.quit()


if __name__ == "__main__":
    target_time = "10:00:00"  # 원하는 목표 시간 설정 정각 -1초 또는 -2초 추천
    get_time_and_execute(time_url, sugang_url, target_time, interval=0.05)
