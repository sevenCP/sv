from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from coupon_reader import read_coupon_codes 



# --- 추가: Selenium Manager 또는 Service 객체 임포트 ---
# 일반적으로 webdriver_manager 라이브러리를 사용하는 것이 가장 편리합니다.
# pip install webdriver-manager 로 설치하세요.
try:
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    print("webdriver_manager 라이브러리가 설치되어 있지 않습니다. 'pip install webdriver-manager'를 실행하세요.")
    print("수동으로 chromedriver를 관리하거나, PATH에 추가해야 할 수 있습니다.")
    ChromeService = None # 임시로 None 설정
    ChromeDriverManager = None # 임시로 None 설정
def button_click(btn_selector,driver,wait):
    print(f"제출 버튼을 찾고 있습니다: {btn_selector}")
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, btn_selector)))
                
    # 4. 이제 버튼을 클릭
    try:
        btn.click() # ActionChains에서 move_to_element만 했으므로 다시 click() 호출
    except Exception as click_error:
        print(f"JavaScript 클릭 시도...")
        driver.execute_script("arguments[0].click();", btn)

    print("결과 대기 중...")
    time.sleep(1) # 결과 페이지 또는 알림 대기

def automate_coupon_entry(url, coupon_codes, uid_value ,uid_input_selector, coupon_input_selector, submit_button_selector,ok_btn, ok_btn2,dup_btn, driver_path=None):
    """
    지정된 URL에 접속하여 쿠폰 코드 리스트를 순회하며 입력하고 제출합니다.

    Args:
        url (str): 쿠폰 입력 페이지 URL.
        coupon_codes (list): 입력할 쿠폰 코드 리스트.
        coupon_input_selector (str): 쿠폰 입력 필드의 CSS Selector 또는 XPath.
        submit_button_selector (str): 쿠폰 적용/등록 버튼의 CSS Selector 또는 XPath.
        driver_path (str, optional): WebDriver의 경로. None이면 PATH 환경 변수에서 찾거나,
                                      webdriver_manager가 자동으로 처리합니다.
    """
    driver = None # 드라이버 변수 초기화

    try:
        # --- 드라이버 초기화 부분 변경 ---
        if ChromeService and ChromeDriverManager:
            # webdriver_manager를 사용하여 자동으로 드라이버 다운로드 및 설정
            print("WebDriver Manager를 사용하여 Chrome 드라이버를 초기화합니다.")
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service)
        elif driver_path:
            # driver_path가 지정된 경우 (수동으로 드라이버를 관리할 때)
            # Service 객체를 사용하여 경로 지정
            print(f"지정된 경로 '{driver_path}'로 Chrome 드라이버를 초기화합니다.")
            service = ChromeService(executable_path=driver_path)
            driver = webdriver.Chrome(service=service)
        else:
            # PATH에 드라이버가 있거나, 기본 위치에 있는 경우 (자동 감지)
            print("기본 경로에서 Chrome 드라이버를 찾아 초기화합니다.")
            driver = webdriver.Chrome()
        # --- 드라이버 초기화 부분 변경 끝 ---

        # (나머지 코드는 이전과 동일)
        for i, code in enumerate(coupon_codes):
            print(f"[{i+1}/{len(coupon_codes)}] 쿠폰 코드 입력 시도: {code}")
            driver.get(url)
            
            # 페이지 로딩 및 요소 가시성 대기
            wait = WebDriverWait(driver, 5) 

            try:
                # --- UID 입력 필드 찾기 및 입력 ---
                # uid_input_selector와 uid_value가 모두 제공되었을 때만 실행
                if uid_input_selector and uid_value: 
                    print(f"UID 입력 필드를 찾고 있습니다: {uid_input_selector}")
                    uid_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, uid_input_selector)))
                    uid_input.clear()
                    uid_input.send_keys(uid_value) # 함수 파라미터로 받은 uid_value 사용
                    print(f"UID '{uid_value}' 입력 완료.")
                    time.sleep(1) # UID 입력 후 잠시 대기
                
                
                # 쿠폰 입력 필드 찾기 및 입력
                coupon_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, coupon_input_selector)))
                coupon_input.clear()
                coupon_input.send_keys(code)
                print(f"'{code}' 입력 완료.")
                
                time.sleep(1) 

                # 사용하기 버튼
                print(f"제출 버튼을 찾고 있습니다: {submit_button_selector}")
                button_click(submit_button_selector,driver,wait)
                #제출후 ok버튼
                button_click(ok_btn,driver,wait)

                button_click(dup_btn,driver,wait)
                #쿠폰 등록 성공 후 돌아가기 버튼
                button_click(ok_btn2,driver,wait)
            except Exception as e:
                print(f"오류: 쿠폰 '{code}' 처리 중 문제 발생 - {e}")
                
            
            print("-" * 30) 
            time.sleep(1) 

    except Exception as e:
        print(f"자동화 실행 중 전역 오류 발생: {e}")
    finally:
        if driver:
            print("웹 드라이버를 종료합니다.")
            driver.quit()

    