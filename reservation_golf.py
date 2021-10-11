
import chromedriver_autoinstaller
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.alert import Alert
from bs4 import BeautifulSoup

# chrome driver auto install and driver activation
def chromedriver_autorun():

    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  #크롬드라이버 버전 확인

    try:
        driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')
    except:
        chromedriver_autoinstaller.install(True)
        driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')

    driver.implicitly_wait(10)
    return driver

driver = chromedriver_autorun()
# driver.close()
# driver.quit()

# 1. 주요 골프장 class 만들기
#    0) 주요 골프장 리스트 마에스트로, 리베라,소노펠리체,  리베라(10/11 완료)
#    1) log in id/pw , (10/11)
#    2) 예약 날짜 시간 선택 조건으로 날짜대, 시간 대  고를수 있어야 하고, 시간대를 고르면 가능한 시간중  몇번째를 고를지 옵션 필요 (10/11 처음 중간 끝 중 고르게 하였음)
#    3)각 골프장 예약 오프되는 시간대 db로 저장 및 관리 (진행 예정)
# 2. 알림 메세지
#    1) 취소 가능일 전 미리 취소 여부 알람 메세지
#    2) 동반자에게 미리 알리기
# 3. 양도 기능
#    1) 예약 시간 양도 관련 내가 취소 즉시 다른 사람이 예약 가능하도록 변경 기능
#

rivera = {'url': 'https://www.shinangolf.com/',
          'loginPage': 'https://www.shinangolf.com/member/login',
          'id': 'ohkili',
          'pw': 'Sin!1203'
           }

# 날짜 고르기
wish_date = ['20211015','20211021','20211028']
wish_hour = ['15~19']
hour_option = 'first'  # ['first, mid, last']
# 골프장 고르기
loginfo = rivera

url = loginfo['url']
loginpage = loginfo['loginPage']
loginID = loginfo['id']
loginPW = loginfo['pw']

driver.get(url)
driver.get(loginpage)

# id
userId = driver.find_element(By.ID, 'memberId')   # /html/body/div/div[5]/div/div/div/div[2]/div/form/div[1]/div[1]/input
userId.send_keys(loginID)  # 로그인 할 계정 id

#password
userPwd = driver.find_element(By.ID, 'key') # /html/body/div/div[5]/div/div/div/div[2]/div/form/div[1]/div[2]/input
userPwd.send_keys(loginPW)
userPwd.send_keys(Keys.ENTER)

#log in putton userPwd에 password를 엔터를 치면 되는데, 아래처럼 로그인 버튼을 누를수도 있다
# loginbtn = driver.find_element(By.XPATH, "//form[@id='loginForm']/div[@class='login_btn']")
# loginbtn.click()

# 통합 예약/실시간예약
# reservation = driver.find_element(By.XPATH,"/html/body/div/div[2]/div/div[2]/div[1]/ul/li[1]/div/ul/li[1]/a")  # /html/body/div/div[2]/div/div[2]/div[1]/ul/li[1]/div/ul/li[1]/a
reservation_open = driver.find_element(By.XPATH,"/html/body/div/div[2]/div/div[2]/div[1]/ul/li[1]/div/ul/li[1]/a")
driver.execute_script("arguments[0].click();",reservation_open)
# 아래 블럭 처리한 내용은 element에서 click을 하고 시행되지 않으면 execute_script를 쓰라는 문구인데 시간을 아끼기 위해 바로 excecute_sript를 사용하였다.
#  """   try:
#         print("Element is visible? " + str(reservation_open.is_displayed()))  # elemnet visible check
#         reservation_open.click()
#         # 에러메시지가 아래와 같이 나오면 엘리먼트가 보이지 않은것이다.
#         # " selenium.common.exceptions.ElementNotInteractableException: Message: element not interactable   (Session info: chrome=94.0.4606.61) "
#
#         print("Element is visible? " + str(reservation_open.is_displayed())) # elemnet visible check
#         except:
#
#              # 그러면 아래와 같이 명령을 쓰면 해결이 된다.
#             driver.execute_script("arguments[0].click();",reservation_open)
# """



# driver.close()
# 실시간 예약

""" <div id='condainer'>
       <div id='content'>
           <div class ='board_info_wrap'>
              <div class = 'inner'>
                  < div class = 'page_tap_wrap'>  # 신안 계열 골프장 리스트
                  < div class = 'month_wrap'> #달력
                   < button type ='button' class= 'prev'> 지난달 버튼
                   < span class ='year'>   올해 년도
                   < span class = 'month'> 이번 달
                   < button type = 'button' class 'next'> 다음달 버튼
                   < div class = 'reservation_table calender_table> 예약 날짜 목록
                     <table>
                      <tbody> 이아래에 날짜별로 목록이 존재
                       <tr> tr이 주간 묶음이고 하위에 <td>가 날짜를 뜻한다
                        <td> 공란이면 해당 월에 날이 없는것을 말함(예약 가능일이 아니고 달력 기준 날짜)
                          < div class ='day'>1 </div>  날짜
                          < div class ='white'> 이면 예약 가능한 날이 없다는 것이다
                          or 
                          <div class ='day'>12 </div> 예약이 가능한 경우는
                          <a class='open' id='20211012'> 1팀/<a>  날짜와 예약 가능 팀수를 알수 있다. 클릭하면 상세 날짜가 나온다 
                    <div id ='reservationSelect'> 예약 상세 page 위에 날짜를 선택해야 상세 page가 열림
                      <div class ='date_wrap' > 해당 날짜
                        < div class = 'reservation_table time_table>
                           <table>
                             <thread> 
                                <tr> 예약 상세화면의 컬럼 정보, [코스, 시간, 그린피, 예약]
                             <tbody> 
                                 <tr> 예약 상세정보 이게 중요한 예약 가능 정보임, 
                                    <th rowspan =2> LAKES </th>  코스 정보 및 해당 코스(LAKES) 에 몇개 예약(rowspn)이 가능한지 숫자 나옴
                                    <td> 18:52 </td> 시간
                                    <td> 130,000 </td> 금액
                                    <td> 
                                       <button conclick> 예약 선택 버튼 """
                                    
for d in wish_date:
    d = wish_date[2]
    wish_year = d[:4]
    wish_month = d[4:6]
    wish_day = d[6:8]
    try:

        calendar = driver.find_element(By.XPATH, "//div[@class='reservation_table calendar_table']/table/tbody")
        date_selected =  "//tr/td/a[@class='open'  and @id =" + "'" + d + "']"
        # temp_date = calendar.find_element(By.XPATH, "//tr/td/a[@class='open'  and @id ='20211028']")
        # calendar.find_element(By.XPATH, date_selected).text 에 예약이 가능하면 팀수가 나옴 없으면 예약 불가능하므로 예약 시도 cancel
        if calendar.find_element(By.XPATH, date_selected).text.find('팀')>=0 :
            calendar.find_element(By.XPATH, date_selected).click()   #원하는 날짜에 해당하는 달력 check
            # calendar.find_element(By.XPATH, date_selected).text

            reservation_time = driver.find_element(By.XPATH, "//div[@class = 'reservation_table time_table']")
            reservation_time_list = reservation_time.find_elements(By.XPATH,"//table/tbody/tr/td/button")

            # s = reservation_time_list[0].get_attribute('onclick')
            # s = s.replace('showConfirm','').replace('(','').replace(')','').replace("'",'').split(',')

            # time table을 list로 만들자
            timeTable = pd.DataFrame()
            timeTable_columns = ['fulldate','day','hour','course_type','cousrse_name','price','unknown1','unknown2','unknown3']

            for i in range(len(reservation_time_list)):
                s = reservation_time_list[i].get_attribute('onclick')
                s = s.replace('showConfirm', '').replace('(', '').replace(')', '').replace("'", '').split(',')
                s = pd.DataFrame(data=[s])
                timeTable = timeTable.append(s)
                print(i,s)

            timeTable.columns = timeTable_columns
            timeTable.reset_index(drop=True, inplace= True)

            # 원하는 시간대 골라내기
            first_time = wish_hour[0].split('~')[0]
            end_time = wish_hour[0].split('~')[1]
            mask1 = (timeTable['hour'].str[0:2] >= first_time) & (timeTable['hour'].str[0:2] < end_time)  # 시간대 filter
            timeTable_masked = timeTable.loc[mask1,: ]

            timeTable_sorted = timeTable_masked.sort_values('hour')
            timeTable_sorted.reset_index(inplace=True)

            if hour_option == 'first':
                index_no = timeTable_sorted['index'].iloc[0]
            elif hour_option == 'mid':
                index_no = timeTable_sorted['index'].iloc[round(len(timeTable_sorted)/2)]
            elif hour_option == 'last':
                index_no = timeTable_sorted['index'].iloc[-1]


            # 골라낸 시간에 예약 버튼 누르기


            # reservation_time_list[index_no].get_attribute('onclick')
            # reservation_time_list[index_no].click()
            #
            # reservation_time_list[index_no].get_attribute('onclick')
            driver.execute_script("arguments[0].click();",reservation_time_list[index_no])


            # 예약 확인 pop up
            # reserve_text = driver.find_element(By.XPATH,
            #                     "//div[@id='confirmModal']/div[@class='modal_content']/div[@class='confirm_modal']/div[@class='form_btns']/button").text
            # print(reserve_text)
            driver.find_element(By.XPATH, "//div[@id='confirmModal']/div[@class='modal_content']/div[@class='confirm_modal']/div[@class='form_btns']/button").click()
            # 이렇게 하면 바로 예약 됨
        
        elif calendar.find_element(By.XPATH, date_selected).text.find('팀') == -1:   # 예약일이 없으면 바로 빠져 나와서 처리 속도를 높여줌
            print('There is no book', d)
            break
        else:
            print('Check your input condition!')
    except:
        print('There is no book', d)

driver.close()



                  
                
                
                  
           