from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

import time

# 웹드라이버 설정(Chrome, Firefox 등)
driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))
#driver = webdriver.Chrome('/path/to/chromedriver')

# 웹페이지 접속
driver.get('https://auto.danawa.com/newcar/?&page=1')

try:
    # 'domestic' 클래스가 로드될 때까지 대기
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'domestic')))

    # 'domestic' 클래스 내의 모든 버튼 찾기
    buttons = driver.find_elements(By.XPATH, "//div[@class='domestic']//button")

    # 각 버튼 클릭
    for i in range(6):
        buttons[i].click()
        time.sleep(1) 
    
    # 리스트 갯수를 선택할 <select> 요소 찾기
    list_count_select = Select(driver.find_element(By.ID, 'listCount'))
    
    # 리스트 갯수를 100개로 설정
    list_count_select.select_by_value('100')
    
    contents = driver.find_element(By.ID, "container_newcarlist")
    
    # 'list modelList' 클래스가 로드될 때까지 최대 10초 동안 대기
    model_list_elements = WebDriverWait(contents, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".list.modelList li")))

    # 각 'li' 요소 내부에 있는 'info' 클래스 내부에 있는 'detail' 클래스 내부에 있는 'spec' 클래스에 해당하는 모든 'span' 요소의 데이터 가져오기
    for li in model_list_elements:
        span_elements = WebDriverWait(li, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".info .detail .spec span")))
        for span in span_elements:
            text = WebDriverWait(span, 10).until(lambda s: s.text)
            print(text)

finally:
    # 웹드라이버 종료
    driver.quit()
    