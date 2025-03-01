from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from .config import Config  # 수정: 상대 경로로 import


class SugangHandler:
    """수강신청 관련 기능을 처리하는 클래스"""

    def __init__(self, driver):
        self.driver = driver

    def switch_to_frames(self):
        """필요한 프레임으로 전환"""
        try:
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame(Config.FRAMES['main'])
            self.driver.switch_to.frame(Config.FRAMES['pkg'])
        except Exception as e:
            print(f"프레임 전환 중 오류: {e}")
            raise

    def get_apply_buttons(self):
        """수강신청 버튼들 가져오기"""
        try:
            buttons = WebDriverWait(self.driver, Config.DEFAULT_TIMEOUT).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, Config.SELECTORS['apply_button'])
                )
            )
            return buttons
        except Exception as e:
            print(f"수강신청 버튼 가져오기 실패: {e}")
            return []

    def click_buttons_in_order(self, buttons, priorities):
        """우선순위에 따라 버튼 클릭"""
        try:
            if not priorities:
                priorities = Config.PRIORITIES

            for priority in priorities:
                if priority <= len(buttons):
                    try:
                        buttons[priority - 1].click()
                        self.handle_alerts()
                    except Exception as e:
                        print(f"{priority}번 과목 신청 실패: {e}")
                        continue
        except Exception as e:
            print(f"버튼 클릭 중 오류: {e}")

    def handle_alerts(self):
        """알림창 처리"""
        try:
            for i in range(2):
                alert = WebDriverWait(self.driver, Config.ALERT_TIMEOUT).until(
                    EC.alert_is_present())
                print(f"{i + 1}번째 알림:", alert.text)
                alert.accept()
        except TimeoutException:
            print("알림창 대기 시간 초과")
        except Exception as e:
            print(f"알림창 처리 중 오류: {e}")

    def process_sugang(self, priorities=None):
        """수강신청 처리"""
        try:
            self.switch_to_frames()
            buttons = self.get_apply_buttons()
            if buttons:
                self.click_buttons_in_order(buttons, priorities)
                return True
            else:
                print("수강신청 버튼을 찾을 수 없습니다.")
                return False
        except Exception as e:
            print(f"수강신청 처리 중 오류: {e}")
            return False
