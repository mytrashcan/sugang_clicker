from application import SugangApplication


def main():
    try:
        app = SugangApplication()
        target_time = "09:59:58"  # 1, 2초 정도 빠르게 설정할것을 추천(안정적: 1초, 빠르게: 2초)
        app.run(target_time, interval=0.05)
    except Exception as e:
        print(f"프로그램 실행 중 오류 발생: {e}")
    finally:
        input("프로그램을 종료하려면 Enter를 눌러주세요...")


if __name__ == "__main__":
    main()
