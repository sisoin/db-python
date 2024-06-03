#-----가격 가져오는 코드--------------------
        # # 'action' 클래스 내의 링크 가져오기
        # action_link = li.find_element(By.CSS_SELECTOR, ".right .row .action a").get_attribute("href")
        # # 해당 링크로 이동
        # driver.get(action_link)
        
        # # id가 Trim_1 인 클래스가 로드될 때까지 대기
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Trim_1')))
        # time.sleep(0.1)
        # # id가 Trim_1 인 요소 내부의 모든 choice 클래스 요소 찾기
        # choice_elements = driver.find_elements(By.CSS_SELECTOR, "#Trim_1 .estimate__cont.eTrimBox .eChkTrimList.article-box.article-box--open .article-box__cont .choice")
    
        # # 가장 마지막 choice 클래스 요소 찾기
        # last_choice_element = choice_elements[0]
        
        # # choice__wrap 클래스 내부의 choice__cell choice__price 클래스 내부의 txt 클래스 내부의 num 클래스 값 가져오기
        # price_element = last_choice_element.find_element(By.CSS_SELECTOR, ".choice__wrap .choice__cell.choice__price .txt .num")
        
        # # 가격 값 가져오기
        # price_value = int(price_element.text.replace(',', ''))
        # price_sum = price_value
        
        # # id가 Optn_1 인 클래스가 로드될 때까지 대기
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Optn_1')))
        # time.sleep(0.1)
        # # id가 Optn_1 인 요소 내부의 모든 choice-toggle.choice-toggle--close 클래스 요소 찾기
        # toggle_elements = driver.find_elements(By.CSS_SELECTOR, "#Optn_1 .estimate__cont.eChkItemList .article-box .article-box__cont .choice-toggle.choice-toggle--close")
        
        # for toggle_element in toggle_elements:
        #     # choice-toggle__header sendGA 클래스를 가진 요소 찾기
        #     header_element = toggle_element.find_element(By.CSS_SELECTOR, "#Optn_1 .choice-toggle__header")
            
        #     # 대기 후 요소 찾기
        #     WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".choice-toggle.choice-toggle--close .choice__wrap .choice__cell.choice__price .txt .num")))
        #     time.sleep(0.1)
        #     # choice__wrap 클래스 내부의 choice__cell choice__price 클래스의 txt 클래스의 num 클래스의 값을 가져오기
        #     price_element = header_element.find_element(By.CSS_SELECTOR, ".choice-toggle.choice-toggle--close .choice__wrap .choice__cell.choice__price .txt .num")
            
        #     # 가격 값 가져오기
        #     price_value = price_element.text.strip()
        #     if price_value:
        #         price_sum += int(price_value.replace(',', ''))
        
        # driver.back()