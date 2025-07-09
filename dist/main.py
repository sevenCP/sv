from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from coupon_reader import read_coupon_codes # coupon_reader.py에서 함수 임포트
from web_automator import automate_coupon_entry # automate_coupon_entry 함수 임포트
from config import ( # config.py에서 필요한 모든 상수 임포트
    UID_VALUE,
    URL,
    WEBDRIVER_PATH,
    UID_INPUT,
    COUPON_INPUT,
    COUPON_PATH,
    SUBMIT_BTN,
    OK_BTN,
    OK_BTN2,
    DUPLICATION_BTN,
    
)



# --- 전체 프로그램 실행 예시 ---
if __name__ == "__main__":
    coupon_file = "coupons.txt" # 쿠폰 코드가 저장된 메모장 파일
    website_url = "https://www.example.com/coupon_page" # 쿠폰 입력 페이지 URL
    
    # !!! 중요: 이 부분은 실제 웹사이트에 맞게 수정해야 합니다 !!!
    # 개발자 도구(F12)를 열어 쿠폰 입력 필드와 버튼의 CSS Selector 또는 XPath를 찾아야 합니다.
    coupon_input_selector = "#coupon_code_input" # 예시: ID가 'coupon_code_input'인 요소
    submit_button_selector = "button.apply_coupon_btn" # 예시: 클래스가 'apply_coupon_btn'인 버튼

    # 1. 쿠폰 코드 읽어오기
    coupon_codes_list = read_coupon_codes(COUPON_PATH)

    if coupon_codes_list:
        print(f"Found {len(coupon_codes_list)} coupon codes.")
        # 2. 웹사이트 자동화 시작
        automate_coupon_entry(url= URL, coupon_codes= coupon_codes_list,uid_value = UID_VALUE, uid_input_selector= UID_INPUT,coupon_input_selector= COUPON_INPUT, submit_button_selector= SUBMIT_BTN,ok_btn=OK_BTN, ok_btn2=OK_BTN2,dup_btn=DUPLICATION_BTN, driver_path= WEBDRIVER_PATH)
    
    else:
        print("No coupon codes found to process.")