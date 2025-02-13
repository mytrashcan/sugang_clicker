from datetime import datetime


class TimeManager:
    """시간 관련 기능을 처리하는 클래스"""

    @staticmethod
    def convert_korean_time_to_hms(time_str):
        """한글 시간 문자열을 HH:MM:SS 형식으로 변환"""
        try:
            hours = minutes = seconds = '00'
            for part in time_str.split():
                if '시' in part:
                    hours = part.replace('시', '').strip().zfill(2)
                elif '분' in part:
                    minutes = part.replace('분', '').strip().zfill(2)
                elif '초' in part:
                    seconds = part.replace('초', '').strip().zfill(2)
            return f"{hours}:{minutes}:{seconds}"
        except Exception as e:
            print(f"시간 변환 중 오류: {e}")
            return None

    @staticmethod
    def is_target_time_reached(current_time, target_time):
        """목표 시간 도달 여부 확인"""
        try:
            current = datetime.strptime(current_time, "%H:%M:%S")
            target = datetime.strptime(target_time, "%H:%M:%S")
            print(f"\r현재 시간: {current_time} | 목표 시간: {target_time}", end="")
            return current >= target
        except Exception as e:
            print(f"시간 비교 중 오류: {e}")
            return False
