class Config:
    """전역 설정값들을 관리하는 클래스"""
    DEFAULT_TIMEOUT = 10
    ALERT_TIMEOUT = 5
    DEFAULT_INTERVAL = 0.01 # 서버 시간 갱신 주기
    PRIORITIES = [3, 2, 4, 6, 1, 5] # 수강 신청 우선순위 설정 숫자-영어-한글

    SELECTORS = {
        'login_id': 'id',
        'login_pw': 'passwd',
        'login_btn': 'btn_login',
        'time_area': 'time_area',
        'apply_button': "a.s-btn.s-plus:not(.s-minus)"
    }

    FRAMES = {
        'main': 'Main',
        'pkg': 'pkg'
    }
