from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import re
import time
import mysql.connector

def prioritize_fuel_type(data):
    # 데이터 우선순위 정의
    priority_order = ["디젤", "가솔린", "가솔린+디젤"]
    
    # 데이터를 우선순위에 따라 필터링
    for fuel_type in priority_order:
        if fuel_type in data:
            return fuel_type
    
    # 전기인 경우는 빈 문자열 반환
    return ""

def extract_numbers(text):
    # 정규표현식을 사용하여 문자열에서 쉼표를 무시하고 숫자와 소수점을 추출
    numbers = re.findall(r'\d+(?:,\d+)*\.\d+|\d+(?:,\d+)*', text)
    # 쉼표를 제거하고 숫자를 실수 또는 정수로 변환하여 반환
    return float(numbers[0].replace(',', '')) if '.' in numbers[0] else int(numbers[0].replace(',', ''))


# MySQL 데이터베이스 연결 설정
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
)

# 데이터베이스 커서 생성
mycursor = mydb.cursor()

# 'cars' 데이터베이스가 존재하지 않는 경우에만 데이터베이스 생성
mycursor.execute("CREATE DATABASE IF NOT EXISTS cars")

# 'cars' 데이터베이스를 사용하도록 연결
mycursor.execute("USE cars")

# 테이블이 존재하는지 확인
mycursor.execute("SHOW TABLES LIKE 'cars'")
result = mycursor.fetchone()

# 테이블이 존재하지 않는 경우에만 테이블 생성 쿼리 실행
create_sql = '''
    CREATE TABLE cars(
        id INT AUTO_INCREMENT PRIMARY KEY,
        company VARCHAR(255),
        name VARCHAR(255),
        type VARCHAR(255),
        fuel VARCHAR(255),
        cc VARCHAR(255),
        efficiency VARCHAR(255),
        price VARCHAR(255),
        tax VARCHAR(255),
        oil_price VARCHAR(255)
    );
'''
if not result:
    mycursor.execute(create_sql)

# 웹드라이버 설정(Chrome, Firefox 등)
driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))

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
        time.sleep(0.1) 
    
    # 리스트 갯수를 선택할 <select> 요소 찾기
    list_count_select = Select(driver.find_element(By.ID, 'listCount'))
    
    # 리스트 갯수를 100개로 설정
    list_count_select.select_by_value('100')
    
    contents = driver.find_element(By.ID, "container_newcarlist")
    time.sleep(0.1) 
    
    # 'list modelList' 클래스가 로드될 때까지 최대 10초 동안 대기
    model_list_elements = WebDriverWait(contents, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".list.modelList li:not(.list_banner)")))
    time.sleep(1) 

    print('found ' + str(len(model_list_elements)) + ' cars')
    for li in model_list_elements:
        # 'price' 클래스의 텍스트 가져오기
        try:
            # 'price' 클래스의 텍스트 가져오기
            price_element = li.find_element(By.CSS_SELECTOR, ".right .row .price")
            price_text = price_element.text.strip()
            print(price_text)
        except NoSuchElementException:
            print("Price element not found in this li.")
            continue

        # 만약 가격이 '가격미정'(출시되지 않은 차량)이면 건너뜀
        if price_text == '가격미정':
            continue

        span_elements = li.find_elements(By.CSS_SELECTOR, ".info .detail .spec span")
        # 연비 인증단계를 거치는 중인 차량은 데이터를 가져오지 않음
        contains_certification = False
        for span in span_elements:
            text = span.text.strip()
            if '인증中' in text:
                contains_certification = True
                break
        
        # '인증'을 포함하는 span 요소가 있으면 해당 li 요소를 건너뜁니다.
        if contains_certification:
            continue
        
        #-----가격 가져오는 코드--------------------
        # 'action' 클래스 내의 링크 가져오기
        action_link = li.find_element(By.CSS_SELECTOR, ".right .row .action a").get_attribute("href")
        # 해당 링크로 이동
        driver.get(action_link)
        
        # id가 Trim_1 인 클래스가 로드될 때까지 대기
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Trim_1')))
        time.sleep(0.1)
        # id가 Trim_1 인 요소 내부의 모든 choice 클래스 요소 찾기
        choice_elements = driver.find_elements(By.CSS_SELECTOR, "#Trim_1 .estimate__cont.eTrimBox .eChkTrimList.article-box.article-box--open .article-box__cont .choice")
    
        # 가장 마지막 choice 클래스 요소 찾기
        if len(choice_elements) == 0:
            print("T_T\n")
            continue
        last_choice_element = choice_elements[0]
        
        # choice__wrap 클래스 내부의 choice__cell choice__price 클래스 내부의 txt 클래스 내부의 num 클래스 값 가져오기
        price_element = last_choice_element.find_element(By.CSS_SELECTOR, ".choice__wrap .choice__cell.choice__price .txt .num")
        
        # 가격 값 가져오기
        price_value = int(price_element.text.replace(',', ''))
        price_sum = price_value
        print(price_sum)
        
        # id가 Optn_1 인 클래스가 로드될 때까지 대기
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Optn_1')))
        time.sleep(0.1)
        # id가 Optn_1 인 요소 내부의 모든 choice-toggle.choice-toggle--close 클래스 요소 찾기
        toggle_elements = driver.find_elements(By.CSS_SELECTOR, "#Optn_1 .estimate__cont.eChkItemList .article-box .article-box__cont .choice-toggle.choice-toggle--close")
        
        for toggle_element in toggle_elements:
            # choice-toggle__header sendGA 클래스를 가진 요소 찾기
            header_element = toggle_element.find_element(By.CSS_SELECTOR, "#Optn_1 .choice-toggle__header")
            
            # 대기 후 요소 찾기
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".choice-toggle.choice-toggle--close .choice__wrap .choice__cell.choice__price .txt .num")))
            time.sleep(0.1)
            # choice__wrap 클래스 내부의 choice__cell choice__price 클래스의 txt 클래스의 num 클래스의 값을 가져오기
            price_element = header_element.find_element(By.CSS_SELECTOR, ".choice-toggle.choice-toggle--close .choice__wrap .choice__cell.choice__price .txt .num")
            
            # 가격 값 가져오기
            price_value = price_element.text.strip()
            if price_value:
                price_sum += int(price_value.replace(',', ''))
        
        driver.back()
        #---------------------------------
        
        car_element = li.find_element(By.CSS_SELECTOR, ".info .detail_middle a img")
        car_brand = car_element.get_attribute("alt")
        car_name_element = li.find_element(By.CSS_SELECTOR, ".info .detail_middle a.name")
        car_name = car_name_element.text.strip()
        if car_brand in car_name:
            car_name = car_name.replace(car_brand, "").strip()
            
        mycursor.execute("SELECT * FROM cars WHERE name = %s", (car_name,))
        existing_car = mycursor.fetchone()
        if existing_car:
            continue
        
        # 차량 스펙 데이터를 추출
        spec_data = []
        contains_certification = False
        
        for span in span_elements:
            text = span.text.strip()
            if '출시' not in text and '판매' not in text and '총주행거리' not in text and '배터리 용량' not in text:
                spec_data.append(text)
                
        spec_data.extend([None] * (4 - len(spec_data)))
        # spec_data[2] 값이 존재하면서 spec_data[3]가 None이라면 spec_data[2] 값을 spec_data[3]에 삽입하고 spec_data[2] 값은 None으로 만듦
        if spec_data[2] and not spec_data[3]:
            spec_data[3] = spec_data[2]
            spec_data[2] = None

        fuel = prioritize_fuel_type(spec_data[1])
        if len(fuel) == 0:
            continue

        cc = extract_numbers(spec_data[2])
        ef = extract_numbers(spec_data[3])
        tax_per_cc = 200 if cc > 1600 else (140 if cc > 1000 else 80)
        tax = tax_per_cc * cc # 교육세 포함 x
            
        car_price = price_sum * 10000
        # 데이터베이스에 삽입할 데이터 준비
        car_data = (
            car_brand,
            car_name,
            spec_data[0],
            fuel,
            str(cc),
            str(ef),
            str(car_price),
            str(tax),
            str(1500 if fuel == '디젤' else 1700 if fuel == '가솔린' else 1600)
        )

        print(car_data)

        # MySQL 데이터베이스에 데이터 삽입
        sql = "INSERT INTO cars (company, name, type, fuel, cc, efficiency, price, tax, oil_price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        mycursor.execute(sql, car_data)
        mydb.commit()
finally:
    # 웹드라이버 종료
    driver.quit()