
import chromedriver_autoinstaller
import time
# from  datetime import  *
import pandas as pd
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import random
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.alert import Alert
from bs4 import BeautifulSoup

import schedule

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

# REST_API_KEY and refresh_token is borrow
REST_API_KEY ='22644bd965c28d381ea875a9dde9e2d1'
refresh_token = 'zIkN8jgb2ITalVnnyIQ56_4ym20mRA6almpDHAo9dNsAAAF8KA4bGA'

# 카카오톡 메시지 API
# rest api key와 refresth token을 이용하여 access token 갱신
def access_token_mkr(REST_API_KEY, refresh_token):
    url = "https://kauth.kakao.com/oauth/token"

    data = {
        "grant_type": "refresh_token",
        "client_id": REST_API_KEY,
        "refresh_token": refresh_token
    }
    response = requests.post(url, data=data)
    tokens2 = response.json()
    print(tokens2)

    access_token = tokens2['access_token']
    return access_token

def kakao_message(data, access_token):
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    # access_token = 'pnvTjrwWOlNoRrFHo5IEfDco_Mi9Kf7R-vC_TQorDNMAAAF8IfKFow'  # tokens['access_token']

    # 사용자 토큰
    headers = {
        "Authorization": "Bearer " + access_token}

    data = {
        "template_object": json.dumps({"object_type": "text",
                                   "text": str(data),
                                       "link": {
                                           "web_url": "www.naver.com"
                                       }
                                       })
    }

    response = requests.post(url, headers=headers, data=data)
    print(response.status_code)
    if response.json().get('result_code') == 0:
        print('메시지를 성공적으로 보냈습니다.')
    else:
        print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))

def good_luck():
      print("Good Luck for Test")
      print( time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
      access_token = access_token_mkr(REST_API_KEY,refresh_token)
      kakao_message('message test '+ str( time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))),access_token)
def reserve_rivera(loginfo,info_date,reserve_cnt=1,reserve_type='test', multi_date = False):
    # info_rivera = {'url': 'https://www.shinangolf.com/',
    #                'loginPage': 'https://www.shinangolf.com/member/login',
    #                'id': 'ohkili',
    #                'pw': 'Sin!1203'
    #                }
    # loginfo = info_rivera
    # info_date = info_date_test
    #

    url = loginfo['url']
    loginpage = loginfo['loginPage']
    loginID = loginfo['id']
    loginPW = loginfo['pw']

    wish_date = info_date['wish_date']
    wish_hour = info_date['wish_hour']

    book_try_cnt = 0
    able_ls = []
    driver = chromedriver_autorun()

    # if reserve_cnt is True ,then reservation don't stop
    # if reserve_cnt is False ,then reservation 1 time and stop
    # driver.close()
    # driver.quit()

    driver.get(url)
    driver.get(loginpage)

    # id
    userId = driver.find_element(By.ID, 'memberId')  # /html/body/div/div[5]/div/div/div/div[2]/div/form/div[1]/div[1]/input
    userId.send_keys(loginID)  # 로그인 할 계정 id

    # password
    userPwd = driver.find_element(By.ID, 'key')  # /html/body/div/div[5]/div/div/div/div[2]/div/form/div[1]/div[2]/input
    userPwd.send_keys(loginPW)
    userPwd.send_keys(Keys.ENTER)

    # log in putton userPwd에 password를 엔터를 치면 되는데, 아래처럼 로그인 버튼을 누를수도 있다
    # loginbtn = driver.find_element(By.XPATH, "//form[@id='loginForm']/div[@class='login_btn']")
    # loginbtn.click()

    # 통합 예약/실시간예약
    # reservation = driver.find_element(By.XPATH,"/html/body/div/div[2]/div/div[2]/div[1]/ul/li[1]/div/ul/li[1]/a")  # /html/body/div/div[2]/div/div[2]/div[1]/ul/li[1]/div/ul/li[1]/a
    reservation_open = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[2]/div[1]/ul/li[1]/div/ul/li[1]/a")
    driver.execute_script("arguments[0].click();", reservation_open)
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

    """ <div id='container'>
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
    date_count = len(wish_date)
    for dt in wish_date:

        if date_count >0 :


            try:
                wish_year = dt[:4]
                wish_month = dt[4:6]
                wish_day = dt[6:8]

                calendar = driver.find_element(By.XPATH, "//div[@class='reservation_table calendar_table']/table/tbody")


                if reserve_type   ==  'real':
                    pass
                elif reserve_type == 'test':
                    status_year  = driver.find_element(By.XPATH, "//div[@class='month_wrap']/span[@class ='year']").text[:4]
                    status_month = driver.find_element(By.XPATH, "//div[@class='month_wrap']/span[@class ='month']").text[:2]
                    if wish_year > status_year or wish_month > status_month :
                        driver.find_element(By.XPATH, "//div[@class='month_wrap]/button[@class='next']").click()
                    else:
                        pass
                    calendar_week = driver.find_elements(By.XPATH,
                                                         "//div[@class='reservation_table calendar_table']/table/tbody/tr")
                    for i in range(len(calendar_week[0].find_elements(By.XPATH, "//td"))):

                        s = (calendar_week[0].find_elements(By.XPATH, "//td")[i].text)
                        if s.find('\n')>0:
                            s = s.split('\n')[0]
                            able_date = wish_year + wish_month + s.zfill(2)
                            able_ls.append(able_date)
                        else:
                            pass
                        if s  == str(int(wish_day)):
                            book_try_cnt += 1
                        else:
                            pass
                        # print(i, s, able_ls, book_try_cnt)


                else:
                    pass

            except:
                print('macro fail : date simple check')
                access_token = access_token_mkr(REST_API_KEY, refresh_token)
                kakao_message('rivera macro fail  : date simple check  \n' + str( time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))) , access_token)

            try:
                if reserve_type == 'real':
                    pass
                elif reserve_type == 'test' and len(able_ls) >0 :
                    dt = able_ls[0]
                elif reserve_type == 'test' and len(able_ls) ==0 and  book_try_cnt == len(wish_date):

                    continue
                else:
                    print('Check book_try_cnt')
                    continue


                date_selected_1 = "//tr/td/a[@class='open'  and @id =" + "'" + dt + "']"
                date_selected_2 = "//tr/td/a[@class='open active'  and @id =" + "'" + dt + "']"
                # temp_date = calendar.find_element(By.XPATH, "//tr/td/a[@class='open'  and @id ='20211028']")
                # temp_date = calendar.find_element(By.XPATH, "//tr/td/a[@class='open active'  and @id ='20211028']")
                # calendar.find_element(By.XPATH, date_selected).text 에 예약이 가능하면 팀수가 나옴 없으면 예약 불가능하므로 예약 시도 cancel

                if calendar.find_element(By.XPATH, date_selected_1).text.find('팀') >= 0:
                    calendar_selected = calendar.find_element(By.XPATH, date_selected_1)
                elif calendar.find_element(By.XPATH, date_selected_2).text.find('팀') >= 0:
                    calendar_selected = calendar.find_element(By.XPATH, date_selected_2)
                elif calendar.find_element(By.XPATH, date_selected_1).text.find('팀') == -1 and calendar.find_element(By.XPATH, date_selected_2).text.find('팀') == -1:   # 예약일이 없으면 바로 빠져 나와서 처리 속도를 높여줌
                    print('There is no book', dt)

                    break

                else :
                    print('Check Calendar')




                calendar_selected.click()     # 원하는 날짜에 해당하는 달력 check
                # calendar.find_element(By.XPATH, date_selected).text

                reservation_time = driver.find_element(By.XPATH, "//div[@class = 'reservation_table time_table']")
                reservation_time_list = reservation_time.find_elements(By.XPATH, "//table/tbody/tr/td/button")


                # s = reservation_time_list[0].get_attribute('onclick')
                # s = s.replace('showConfirm','').replace('(','').replace(')','').replace("'",'').split(',')

                # time table을 list로 만들자
                timeTable = pd.DataFrame()
                timeTable_columns = ['fulldate', 'day', 'hour', 'course_type', 'cousrse_name', 'price', 'unknown1',
                                     'unknown2', 'unknown3']

                for i in range(len(reservation_time_list)):
                    s = reservation_time_list[i].get_attribute('onclick')
                    s = s.replace('showConfirm', '').replace('(', '').replace(')', '').replace("'", '').split(',')
                    s = pd.DataFrame(data=[s])
                    timeTable = timeTable.append(s)
                    print(i, s)

                timeTable.columns = timeTable_columns
                timeTable.reset_index(drop=True, inplace=True)

                # 원하는 시간대 골라내기
                timeTable_masked = pd.DataFrame()
                for h in wish_hour:
                    first_time = h.split('~')[0]
                    end_time = h.split('~')[1]
                    mask1 = (timeTable['hour'].str[0:2] >= first_time) & (
                                timeTable['hour'].str[0:2] < end_time)  # 시간대 filter

                    timeTable_sorted = timeTable.loc[mask1, :].sort_values('hour')
                    timeTable_masked = pd.concat([timeTable_masked, timeTable_sorted])

                timeTable_masked.reset_index(inplace=True)
                while(reserve_cnt > 0):

                    if hour_option == 'first':
                        index_no = timeTable_masked['index'].iloc[0]
                    elif hour_option == 'mid':
                        index_no = timeTable_masked['index'].iloc[round(len(timeTable_sorted) / 2)]
                    elif hour_option == 'last':
                        index_no = timeTable_masked['index'].iloc[-1]

                    idx = timeTable_masked[timeTable_masked['index']== index_no].index
                    timeTable_masked = timeTable_masked.drop(idx)

                    # 골라낸 시간에 예약 버튼 누르기

                    # reservation_time_list[index_no].get_attribute('onclick')
                    # reservation_time_list[index_no].click()
                    #
                    # reservation_time_list[index_no].get_attribute('onclick')
                    driver.execute_script("arguments[0].click();", reservation_time_list[index_no])

                    # 예약 확인 pop up

                    popup_text = driver.find_element(By.XPATH,
                                                     "//div[@id='confirmModal']/div[@class='modal_content']/div[@class='confirm_modal']").text
                    print(popup_text)
                    reserve_text = driver.find_element(By.XPATH,
                                                       "//div[@id='confirmModal']/div[@class='modal_content']/div[@class='confirm_modal']/div[@class='form_btns']/button").text
                    print(reserve_text)

                    if reserve_type == 'real':
                        driver.find_element(By.XPATH,
                                        "//div[@id='confirmModal']/div[@class='modal_content']/div[@class='confirm_modal']/div[@class='form_btns']/button").click()
                        # 이렇게 하면 바로 예약 됨
                        popup_text = '[예약 완료, macro 정상 동작]\n' +  + popup_text
                        kakao_message(popup_text, access_token)

                    elif   reserve_type == 'test' and reserve_text =='예약하기':
                        # 카카오 문자 보내기
                        driver.find_element(By.XPATH,
                                            "//div[@id='confirmModal']/div[@class='modal_content']/div[@class='confirm_modal']/div[@class='form_btns']/a").click()
                        access_token = access_token_mkr(REST_API_KEY, refresh_token)
                        popup_text = '[예약 macro 정상 동작]\n' + '[예약이 된것은 아님]\n'+ popup_text
                        kakao_message(popup_text, access_token)

                    else:
                        print('Check reserve count')
                    reserve_cnt -= 1  # 예약 건수를 1개 줄임
                    if multi_date == True:
                        date_count -= 1
                    elif multi_date == False:
                        date_count = 0
                    else:
                        print('Check multidate option')


            except:
                print('macro fail:  targetting reserve')
                access_token = access_token_mkr(REST_API_KEY, refresh_token)
                kakao_message('rivera macro fail:  targetting reserve  \n' + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))), access_token)

        elif date_count == 0:
            break
        else :
            print('Check date_count')
    if book_try_cnt == len(wish_date):
        access_token = access_token_mkr(REST_API_KEY, refresh_token)
        kakao_message('There is no able day to book \n' + str( time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))), access_token)
    else:
        print('Check book_try_cnt')

    print('book_try_cnt',book_try_cnt)
    print('wish_date',wish_date)
    driver.close()

info_ipo = {'url': 'http://ipo-cc.co.kr/cmm/main/mainPage.do',
               'loginPage': 'http://ipo-cc.co.kr/uat/uia/egovLoginUsr.do',
               'id': 'ohkili',
               'pw': 'Ipocc!1203'
               }

loginfo = info_ipo
def reserve_ipo(loginfo,info_date,reserve_cnt=1,reserve_type='test', multi_date = False):

    # 1.  inforamtion of login  date

    url = loginfo['url']
    loginpage = loginfo['loginPage']
    loginID = loginfo['id']
    loginPW = loginfo['pw']

    wish_date = info_date['wish_date']
    wish_hour = info_date['wish_hour']
    hour_option = info_date['hour_option']

    book_try_cnt = 0
    able_ls = []
    driver = chromedriver_autorun()

    # if reserve_cnt is True ,then reservation don't stop
    # if reserve_cnt is False ,then reservation 1 time and stop
    # driver.close()
    # driver.quit()


    # 2.  log in page open & log in
    driver.get(url)
    driver.get(loginpage)

    # id
    userId = driver.find_element(By.ID, 'id')
    userId.send_keys(loginID)  # 로그인 할 계정 id

    # password
    userPwd = driver.find_element(By.ID, 'password')
    userPwd.send_keys(loginPW)
    userPwd.send_keys(Keys.ENTER)

    # 리베라에 해당하는 사례임
    # log in putton userPwd에 password를 엔터를 치면 되는데, 아래처럼 로그인 버튼을 누를수도 있다
    # loginbtn = driver.find_element(By.XPATH, "//form[@id='loginForm']/div[@class='login_btn']")
    # loginbtn.click()
    # /html/body/div/div[1]/div[3]/div/ul/li[1]/a
    # 통합 예약/실시간예약
    # reservation = driver.find_element(By.XPATH,"/html/body/div/div[2]/div/div[2]/div[1]/ul/li[1]/div/ul/li[1]/a")  # /html/body/div/div[2]/div/div[2]/div[1]/ul/li[1]/div/ul/li[1]/a

    # 3. reserveation page open
    reservation_open = driver.find_element(By.XPATH, "/html/body/div/div[1]/div[3]/div/ul/li[1]/a")
    driver.execute_script("arguments[0].click();", reservation_open)   # 예약 화면 오픈

    # # 달력 예약 / 마감/ 오프전 달력 취합, 오래 걸림
    # driver.find_element(By.ID, "container")
    #
    #
    # driver.find_element(By.XPATH, "//div[@id='content']/div[@class='txtcont']/div[@class='join_form']")
    # driver.find_elements(By.XPATH,"//div[@class = 'mt10 mb40 leftcont']")
    #
    #
    # calendar =  driver.find_elements(By.XPATH,"//table[@class = 'table_cal mt15']")
    # timeTable = pd.DataFrame()
    # cal_type = ['upper_month', 'lower_month']
    # i = 0
    # for cal in (calendar):
    #     month_col = cal_type[i]
    #     i +=1
    #     # 이번달 과 다음달로 나움
    #     print(cal)
    #     # 달에서 주를 나눔
    #     w_ls = cal.find_elements(By.XPATH, "//tbody/tr")
    #
    #     for w in w_ls:
    #
    #         d_ls = w.find_elements(By.XPATH,'td')
    #         for d in d_ls:
    #             try:
    #
    #                 class_col = d.get_attribute('name')
    #                 id_col    = d.get_attribute('id')
    #                 status_col = d.find_element(By.XPATH,"div[@class='cal']").text
    #                 temp = [month_col, class_col, id_col, status_col]
    #                 temp = pd.DataFrame(data=temp).T
    #                 timeTable = timeTable.append(temp)
    #             except:
    #                 pass
    # timeTable_columns = ['cal_type', 'class_col', 'id_col', 'status_col']
    # timeTable.columns = timeTable_columns
    # timeTable.reset_index(drop=True, inplace = True)

    # 3. 달력 예약 / 마감/ 오프전 달력 취합 다른 방법, 이것이 빠름

    driver.find_element(By.XPATH, "//div[@id='timeform']")
    time_ls = driver.find_elements(By.XPATH, "//div[@id='timeform']/input")

    timeTable_2nd = pd.DataFrame()

    for d in time_ls:
        try:

            class_col = d.get_attribute('type')
            id_col = d.get_attribute('id')
            name_col = d.get_attribute('name')

            temp = [class_col, id_col, name_col]
            temp = pd.DataFrame(data=temp).T
            timeTable_2nd = timeTable_2nd.append(temp)
        except:
            pass
    timeTable_2nd_columns   = ['type','id','name']
    timeTable_2nd.columns   = timeTable_2nd_columns
    timeTable_2nd['date']   = timeTable_2nd['id'].apply(lambda x: x.split('_')[1])
    timeTable_2nd['status'] = timeTable_2nd['name'].apply(lambda x: x.split('_')[3])
    timeTable_2nd.reset_index(drop=True, inplace=True)

    reserve_able_date_ls = timeTable_2nd[timeTable_2nd['status'] == '예약']



    # 4. 날짜 선택 기능

    driver.find_element(By.ID, "container")

    # 날짜 211106
    driver.find_element(By.XPATH, "//div[@id='content']/div[@class='txtcont']/div[@class='join_form']")
    driver.find_elements(By.XPATH,"//div[@class = 'mt10 mb40 leftcont']")

    wish_date =  ['20211106', '20211212']
    # # bottom is exercise
    # wish_date = '20211106'
    # date_temp = "//td[@id=" + wish_date + "]"
    # driver.find_element(By.XPATH, date_temp).text # example = '6\n마감'
    reserve_result = []

    for d in wish_date:
        date_temp = "//td[@id=" + d + "]"
        try:
            status = driver.find_element(By.XPATH, date_temp).text.split('\n')[-1]

            if status == '예약':
                reserve_result.append([d, status])
                driver.find_element(By.XPATH, date_temp).click()
                # 이부분에 시간 에약 기능이 들어가야 함

            elif status == '마감' or status =='오픈전':
                reserve_result.append([d,status])
            else:
                reserve_result.append([d, 'error'])
        except:
            reserve_result.append([d, 'exception case'])

    print(reserve_result)

    # 4. 시간 선택 기능

    timeTable_columns = ['fulldate', 'day', 'hour', 'course_type', 'cousrse_name', 'price']

    timeTable = pd.DataFrame([['' for i in range(len(timeTable_columns)) ]], columns = timeTable_columns)  # data 부분에 ['','','','','','']을 넣어줘야 함  이걸 columns 만큼 공란을 만듬

    # # 연습
    # cal = calendar[0]
    # w_ls = cal.find_elements(By.XPATH, "//tbody/tr")
    # d_ls = w_ls[0].find_elements(By.XPATH,'td')
    # d = d_ls[1]
    # d.get_attribute('id')
    # d.get_attribute('name')
    # d.find_element(By.XPATH,"div[@class='cal']").text
    # upper_month = calendar[0].find_elements(By.XPATH, "//tbody/tr")
    # timeTable = pd.DataFrame()
    # month_col =  'upper_month'
    # class_col =    upper_month[0].find_elements(By.XPATH,'td')[1].get_attribute('name')
    # id_col =       upper_month[0].find_elements(By.XPATH,'td')[1].get_attribute('id')
    # status_col =   upper_month[0].find_elements(By.XPATH, 'td')[1].find_element(By.XPATH,"div[@class='cal']").text
    # temp = [month_col,class_col,id_col, status_col]
    # temp = pd.DataFrame(data=temp).T
    # timeTable = timeTable.append(temp)


    # 오른쪽 예약 누르는 화면
    course = driver.find_elements(By.XPATH, "//div[@id='ajaxlist']/div[@class ='mt10 mb40 rightcont join_form']/div[@class ='txtcont']/div[@class='mb40']/table[@class='mt10']/tbody/tr/td")
    # editing
    # out course
    out_course = course[0].find_elements(By.XPATH, "//td[@valign='top']/table[@id='out_table' and @class='table_style2']/tbody/tr") # 시간대가 여러개 일때 리스트  07:00
    time_ls_first = out_course[0].find_element(By.XPATH, "//th").text.split(':')    # th tag에 시간이 표신 됨 ex) 07:00, 시간을 불러와서 앞에 시간만 가져옴
    price_first   = out_course[0].find_element(By.XPATH, "//td/span[@class='daypay']").text

    time_temp = pd.DataFrame(['','',time_ls_first,'','',price_first])

    # 원하는 시간대 골라내기
    timeTable_masked = pd.DataFrame()
    for h in wish_hour:
        first_time = h.split('~')[0]
        end_time = h.split('~')[1]
        mask1 = (timeTable['hour'].str[0:2] >= first_time) & (
                timeTable['hour'].str[0:2] < end_time)  # 시간대 filter

        timeTable_sorted = timeTable.loc[mask1, :].sort_values('hour')
        timeTable_masked = pd.concat([timeTable_masked, timeTable_sorted])

    timeTable_masked.reset_index(inplace=True)

    # edited 211105 15:00










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

    """ <div id='container'>
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
    date_count = len(wish_date)
    for dt in wish_date:

        if date_count >0 :


            try:
                wish_year = dt[:4]
                wish_month = dt[4:6]
                wish_day = dt[6:8]

                calendar = driver.find_element(By.XPATH, "//div[@class='reservation_table calendar_table']/table/tbody")


                if reserve_type   ==  'real':
                    pass
                elif reserve_type == 'test':
                    status_year  = driver.find_element(By.XPATH, "//div[@class='month_wrap']/span[@class ='year']").text[:4]
                    status_month = driver.find_element(By.XPATH, "//div[@class='month_wrap']/span[@class ='month']").text[:2]
                    if wish_year > status_year or wish_month > status_month :
                        driver.find_element(By.XPATH, "//div[@class='month_wrap]/button[@class='next']").click()
                    else:
                        pass
                    calendar_week = driver.find_elements(By.XPATH,
                                                         "//div[@class='reservation_table calendar_table']/table/tbody/tr")
                    for i in range(len(calendar_week[0].find_elements(By.XPATH, "//td"))):

                        s = (calendar_week[0].find_elements(By.XPATH, "//td")[i].text)
                        if s.find('\n')>0:
                            s = s.split('\n')[0]
                            able_date = wish_year + wish_month + s.zfill(2)
                            able_ls.append(able_date)
                        else:
                            pass
                        if s  == str(int(wish_day)):
                            book_try_cnt += 1
                        else:
                            pass
                        # print(i, s, able_ls, book_try_cnt)


                else:
                    pass

            except:
                print('macro fail : date simple check')
                access_token = access_token_mkr(REST_API_KEY, refresh_token)
                kakao_message('rivera macro fail  : date simple check  \n' + str( time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))) , access_token)

            try:
                if reserve_type == 'real':
                    pass
                elif reserve_type == 'test' and len(able_ls) >0 :
                    dt = able_ls[0]
                elif reserve_type == 'test' and len(able_ls) ==0 and  book_try_cnt == len(wish_date):

                    continue
                else:
                    print('Check book_try_cnt')
                    continue


                date_selected_1 = "//tr/td/a[@class='open'  and @id =" + "'" + dt + "']"
                date_selected_2 = "//tr/td/a[@class='open active'  and @id =" + "'" + dt + "']"
                # temp_date = calendar.find_element(By.XPATH, "//tr/td/a[@class='open'  and @id ='20211028']")
                # temp_date = calendar.find_element(By.XPATH, "//tr/td/a[@class='open active'  and @id ='20211028']")
                # calendar.find_element(By.XPATH, date_selected).text 에 예약이 가능하면 팀수가 나옴 없으면 예약 불가능하므로 예약 시도 cancel

                if calendar.find_element(By.XPATH, date_selected_1).text.find('팀') >= 0:
                    calendar_selected = calendar.find_element(By.XPATH, date_selected_1)
                elif calendar.find_element(By.XPATH, date_selected_2).text.find('팀') >= 0:
                    calendar_selected = calendar.find_element(By.XPATH, date_selected_2)
                elif calendar.find_element(By.XPATH, date_selected_1).text.find('팀') == -1 and calendar.find_element(By.XPATH, date_selected_2).text.find('팀') == -1:   # 예약일이 없으면 바로 빠져 나와서 처리 속도를 높여줌
                    print('There is no book', dt)

                    break

                else :
                    print('Check Calendar')




                calendar_selected.click()     # 원하는 날짜에 해당하는 달력 check
                # calendar.find_element(By.XPATH, date_selected).text

                reservation_time = driver.find_element(By.XPATH, "//div[@class = 'reservation_table time_table']")
                reservation_time_list = reservation_time.find_elements(By.XPATH, "//table/tbody/tr/td/button")


                # s = reservation_time_list[0].get_attribute('onclick')
                # s = s.replace('showConfirm','').replace('(','').replace(')','').replace("'",'').split(',')

                # time table을 list로 만들자
                timeTable = pd.DataFrame()
                timeTable_columns = ['fulldate', 'day', 'hour', 'course_type', 'cousrse_name', 'price', 'unknown1',
                                     'unknown2', 'unknown3']

                for i in range(len(reservation_time_list)):
                    s = reservation_time_list[i].get_attribute('onclick')
                    s = s.replace('showConfirm', '').replace('(', '').replace(')', '').replace("'", '').split(',')
                    s = pd.DataFrame(data=[s])
                    timeTable = timeTable.append(s)
                    print(i, s)

                timeTable.columns = timeTable_columns
                timeTable.reset_index(drop=True, inplace=True)

                # 원하는 시간대 골라내기
                timeTable_masked = pd.DataFrame()
                for h in wish_hour:
                    first_time = h.split('~')[0]
                    end_time = h.split('~')[1]
                    mask1 = (timeTable['hour'].str[0:2] >= first_time) & (
                                timeTable['hour'].str[0:2] < end_time)  # 시간대 filter

                    timeTable_sorted = timeTable.loc[mask1, :].sort_values('hour')
                    timeTable_masked = pd.concat([timeTable_masked, timeTable_sorted])

                timeTable_masked.reset_index(inplace=True)
                while(reserve_cnt > 0):

                    if hour_option == 'first':
                        index_no = timeTable_masked['index'].iloc[0]
                    elif hour_option == 'mid':
                        index_no = timeTable_masked['index'].iloc[round(len(timeTable_sorted) / 2)]
                    elif hour_option == 'last':
                        index_no = timeTable_masked['index'].iloc[-1]

                    idx = timeTable_masked[timeTable_masked['index']== index_no].index
                    timeTable_masked = timeTable_masked.drop(idx)

                    # 골라낸 시간에 예약 버튼 누르기

                    # reservation_time_list[index_no].get_attribute('onclick')
                    # reservation_time_list[index_no].click()
                    #
                    # reservation_time_list[index_no].get_attribute('onclick')
                    driver.execute_script("arguments[0].click();", reservation_time_list[index_no])

                    # 예약 확인 pop up

                    popup_text = driver.find_element(By.XPATH,
                                                     "//div[@id='confirmModal']/div[@class='modal_content']/div[@class='confirm_modal']").text
                    print(popup_text)
                    reserve_text = driver.find_element(By.XPATH,
                                                       "//div[@id='confirmModal']/div[@class='modal_content']/div[@class='confirm_modal']/div[@class='form_btns']/button").text
                    print(reserve_text)

                    if reserve_type == 'real':
                        driver.find_element(By.XPATH,
                                        "//div[@id='confirmModal']/div[@class='modal_content']/div[@class='confirm_modal']/div[@class='form_btns']/button").click()
                        # 이렇게 하면 바로 예약 됨
                        popup_text = '[예약 완료, macro 정상 동작]\n' +  + popup_text
                        kakao_message(popup_text, access_token)

                    elif   reserve_type == 'test' and reserve_text =='예약하기':
                        # 카카오 문자 보내기
                        driver.find_element(By.XPATH,
                                            "//div[@id='confirmModal']/div[@class='modal_content']/div[@class='confirm_modal']/div[@class='form_btns']/a").click()
                        access_token = access_token_mkr(REST_API_KEY, refresh_token)
                        popup_text = '[예약 macro 정상 동작]\n' + '[예약이 된것은 아님]\n'+ popup_text
                        kakao_message(popup_text, access_token)

                    else:
                        print('Check reserve count')
                    reserve_cnt -= 1  # 예약 건수를 1개 줄임
                    if multi_date == True:
                        date_count -= 1
                    elif multi_date == False:
                        date_count = 0
                    else:
                        print('Check multidate option')


            except:
                print('macro fail:  targetting reserve')
                access_token = access_token_mkr(REST_API_KEY, refresh_token)
                kakao_message('rivera macro fail:  targetting reserve  \n' + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))), access_token)

        elif date_count == 0:
            break
        else :
            print('Check date_count')
    if book_try_cnt == len(wish_date):
        access_token = access_token_mkr(REST_API_KEY, refresh_token)
        kakao_message('There is no able day to book \n' + str( time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))), access_token)
    else:
        print('Check book_try_cnt')

    print('book_try_cnt',book_try_cnt)
    print('wish_date',wish_date)
    driver.close()

def info_date_test():

    #  wish_date 자동 생성
    time_ls = []
    tm = time.time()
    for t in range(30):
        d = tm + t * 86400
        temp_tm = time.localtime(d)
        string = time.strftime('%Y%m%d', temp_tm)
        time_ls.append(string)

    info_date_test = {'wish_date': time_ls,
                      'wish_hour': ['05~23'],
                      'hour_option': 'first'
                      }
    return info_date_test

# info_date_test = {'wish_date': time_ls,
#                   'wish_hour': ['05~23'],
#                   'hour_option': 'first'
#                   }

info_date_test = {'wish_date': ['20211016','20211017'],
                  'wish_hour': ['05~23'],
                  'hour_option': 'first'
                  }


# 날짜 계산 연습
# tm = time.localtime(1575142526.500323)
# string = time.strftime('%Y-%m-%d %I:%M:%S %p', tm)
# print(string)
# t = time.time() 오늘 날짜
# t = time.localtime(t)
# t1 = t + 86400*100 100일 후 연산
# t1 = time.localtime(t1)
# string = time.strftime('%Y%m%d', t1)
# print(string)



info_rivera = {'url': 'https://www.shinangolf.com/',
               'loginPage': 'https://www.shinangolf.com/member/login',
               'id': 'ohkili',
               'pw': 'Sin!1203'
               }

info_ipo = {'url': 'http://ipo-cc.co.kr/cmm/main/mainPage.do',
               'loginPage': 'http://ipo-cc.co.kr/uat/uia/egovLoginUsr.do',
               'id': 'ohkili',
               'pw': 'Ipocc!1203'
               }

# 날짜 고르기
info_date = {'wish_date': ['20211023', '20211028'],
             'wish_hour': ['14~16', '18~19'],
             'hour_option': 'first'
             }
info_date_test = info_date_test()
# test
reserve_rivera(info_rivera, info_date_test(), reserve_cnt=1, reserve_type='test', multi_date=False)

# Every day at 12am or 00:00 time bedtime() is called.
schedule.every().day.at("19:30").do(good_luck)
schedule.every().day.at("07:30").do(good_luck)
# str(random.randrange(9,14)).zfill(2)
schedule.every().day.at("12:30").do(lambda:  reserve_rivera(info_rivera,info_date_test(),reserve_cnt=1,reserve_type='test', multi_date = False) )
while True:

	# Checks whether a scheduled task
	# is pending to run or not
	schedule.run_pending()

	time.sleep(1)


# # test  part
# # 1. 주요 골프장 class 만들기
# #    0) 주요 골프장 리스트 마에스트로, 리베라,소노펠리체,  리베라(10/11 완료)
# #    1) log in id/pw , (10/11)
# #    2) 예약 날짜 시간 선택 조건으로 날짜대, 시간 대  고를수 있어야 하고, 시간대를 고르면 가능한 시간중  몇번째를 고를지 옵션 필요 (10/11 처음 중간 끝 중 고르게 하였음)
# #    3)각 골프장 예약 오프되는 시간대 db로 저장 및 관리 (진행 예정)
# # 2. 알림 메세지
# #    1) 취소 가능일 전 미리 취소 여부 알람 메세지
# #    2) 동반자에게 미리 알리기
# # 3. 양도 기능
# #    1) 예약 시간 양도 관련 내가 취소 즉시 다른 사람이 예약 가능하도록 변경 기능
# #
#
# info_rivera = {'url': 'https://www.shinangolf.com/',
#                'loginPage': 'https://www.shinangolf.com/member/login',
#                'id': 'ohkili',
#                'pw': 'Sin!1203'
#                }
#
# # 날짜 고르기
# info_date = {'wish_date': ['20211023', '20211028'],
#              'wish_hour': ['14~16', '18~19'],
#              'hour_option': 'first'
#              }
#
# # wish_date = ['20211015','20211021','20211028']
# # wish_hour = ['15~19']
# # hour_option = 'first'  # ['first, mid, last']
# # 골프장 고르기
# loginfo = info_rivera
#
# url = loginfo['url']
# loginpage = loginfo['loginPage']
# loginID = loginfo['id']
# loginPW = loginfo['pw']
#
# driver = chromedriver_autorun()
# # driver.close()
# # driver.quit()
#
# driver.get(url)
# driver.get(loginpage)
#
# # id
# userId = driver.find_element(By.ID, 'memberId')  # /html/body/div/div[5]/div/div/div/div[2]/div/form/div[1]/div[1]/input
# userId.send_keys(loginID)  # 로그인 할 계정 id
#
# # password
# userPwd = driver.find_element(By.ID, 'key')  # /html/body/div/div[5]/div/div/div/div[2]/div/form/div[1]/div[2]/input
# userPwd.send_keys(loginPW)
# userPwd.send_keys(Keys.ENTER)
#
# # log in putton userPwd에 password를 엔터를 치면 되는데, 아래처럼 로그인 버튼을 누를수도 있다
# # loginbtn = driver.find_element(By.XPATH, "//form[@id='loginForm']/div[@class='login_btn']")
# # loginbtn.click()
#
# # 통합 예약/실시간예약
# # reservation = driver.find_element(By.XPATH,"/html/body/div/div[2]/div/div[2]/div[1]/ul/li[1]/div/ul/li[1]/a")  # /html/body/div/div[2]/div/div[2]/div[1]/ul/li[1]/div/ul/li[1]/a
# reservation_open = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[2]/div[1]/ul/li[1]/div/ul/li[1]/a")
# driver.execute_script("arguments[0].click();", reservation_open)
# # 아래 블럭 처리한 내용은 element에서 click을 하고 시행되지 않으면 execute_script를 쓰라는 문구인데 시간을 아끼기 위해 바로 excecute_sript를 사용하였다.
# #  """   try:
# #         print("Element is visible? " + str(reservation_open.is_displayed()))  # elemnet visible check
# #         reservation_open.click()
# #         # 에러메시지가 아래와 같이 나오면 엘리먼트가 보이지 않은것이다.
# #         # " selenium.common.exceptions.ElementNotInteractableException: Message: element not interactable   (Session info: chrome=94.0.4606.61) "
# #
# #         print("Element is visible? " + str(reservation_open.is_displayed())) # elemnet visible check
# #         except:
# #
# #              # 그러면 아래와 같이 명령을 쓰면 해결이 된다.
# #             driver.execute_script("arguments[0].click();",reservation_open)
# # """
#
#
# # driver.close()
# # 실시간 예약
#
# """ <div id='container'>
#        <div id='content'>
#            <div class ='board_info_wrap'>
#               <div class = 'inner'>
#                   < div class = 'page_tap_wrap'>  # 신안 계열 골프장 리스트
#                   < div class = 'month_wrap'> #달력
#                    < button type ='button' class= 'prev'> 지난달 버튼
#                    < span class ='year'>   올해 년도
#                    < span class = 'month'> 이번 달
#                    < button type = 'button' class 'next'> 다음달 버튼
#                    < div class = 'reservation_table calender_table> 예약 날짜 목록
#                      <table>
#                       <tbody> 이아래에 날짜별로 목록이 존재
#                        <tr> tr이 주간 묶음이고 하위에 <td>가 날짜를 뜻한다
#                         <td> 공란이면 해당 월에 날이 없는것을 말함(예약 가능일이 아니고 달력 기준 날짜)
#                           < div class ='day'>1 </div>  날짜
#                           < div class ='white'> 이면 예약 가능한 날이 없다는 것이다
#                           or
#                           <div class ='day'>12 </div> 예약이 가능한 경우는
#                           <a class='open' id='20211012'> 1팀/<a>  날짜와 예약 가능 팀수를 알수 있다. 클릭하면 상세 날짜가 나온다
#                     <div id ='reservationSelect'> 예약 상세 page 위에 날짜를 선택해야 상세 page가 열림
#                       <div class ='date_wrap' > 해당 날짜
#                         < div class = 'reservation_table time_table>
#                            <table>
#                              <thread>
#                                 <tr> 예약 상세화면의 컬럼 정보, [코스, 시간, 그린피, 예약]
#                              <tbody>
#                                  <tr> 예약 상세정보 이게 중요한 예약 가능 정보임,
#                                     <th rowspan =2> LAKES </th>  코스 정보 및 해당 코스(LAKES) 에 몇개 예약(rowspn)이 가능한지 숫자 나옴
#                                     <td> 18:52 </td> 시간
#                                     <td> 130,000 </td> 금액
#                                     <td>
#                                        <button conclick> 예약 선택 버튼 """
#
# for d in wish_date:
#     d = wish_date[2]
#     wish_year = d[:4]
#     wish_month = d[4:6]
#     wish_day = d[6:8]
#     try:
#
#         calendar = driver.find_element(By.XPATH, "//div[@class='reservation_table calendar_table']/table/tbody")
#         date_selected = "//tr/td/a[@class='open'  and @id =" + "'" + d + "']"
#         # temp_date = calendar.find_element(By.XPATH, "//tr/td/a[@class='open'  and @id ='20211028']")
#         # calendar.find_element(By.XPATH, date_selected).text 에 예약이 가능하면 팀수가 나옴 없으면 예약 불가능하므로 예약 시도 cancel
#         if calendar.find_element(By.XPATH, date_selected).text.find('팀') >= 0:
#             calendar.find_element(By.XPATH, date_selected).click()  # 원하는 날짜에 해당하는 달력 check
#             # calendar.find_element(By.XPATH, date_selected).text
#
#             reservation_time = driver.find_element(By.XPATH, "//div[@class = 'reservation_table time_table']")
#             reservation_time_list = reservation_time.find_elements(By.XPATH, "//table/tbody/tr/td/button")
#
#             # s = reservation_time_list[0].get_attribute('onclick')
#             # s = s.replace('showConfirm','').replace('(','').replace(')','').replace("'",'').split(',')
#
#             # time table을 list로 만들자
#             timeTable = pd.DataFrame()
#             timeTable_columns = ['fulldate', 'day', 'hour', 'course_type', 'cousrse_name', 'price', 'unknown1',
#                                  'unknown2', 'unknown3']
#
#             for i in range(len(reservation_time_list)):
#                 s = reservation_time_list[i].get_attribute('onclick')
#                 s = s.replace('showConfirm', '').replace('(', '').replace(')', '').replace("'", '').split(',')
#                 s = pd.DataFrame(data=[s])
#                 timeTable = timeTable.append(s)
#                 print(i, s)
#
#             timeTable.columns = timeTable_columns
#             timeTable.reset_index(drop=True, inplace=True)
#
#             # 원하는 시간대 골라내기
#             first_time = wish_hour[0].split('~')[0]
#             end_time = wish_hour[0].split('~')[1]
#             mask1 = (timeTable['hour'].str[0:2] >= first_time) & (timeTable['hour'].str[0:2] < end_time)  # 시간대 filter
#             timeTable_masked = timeTable.loc[mask1, :]
#
#             timeTable_sorted = timeTable_masked.sort_values('hour')
#             timeTable_sorted.reset_index(inplace=True)
#
#             if hour_option == 'first':
#                 index_no = timeTable_sorted['index'].iloc[0]
#             elif hour_option == 'mid':
#                 index_no = timeTable_sorted['index'].iloc[round(len(timeTable_sorted) / 2)]
#             elif hour_option == 'last':
#                 index_no = timeTable_sorted['index'].iloc[-1]
#
#             # 골라낸 시간에 예약 버튼 누르기
#
#             # reservation_time_list[index_no].get_attribute('onclick')
#             # reservation_time_list[index_no].click()
#             #
#             # reservation_time_list[index_no].get_attribute('onclick')
#             driver.execute_script("arguments[0].click();", reservation_time_list[index_no])
#
#             # 예약 확인 pop up
#             # reserve_text = driver.find_element(By.XPATH,
#             #                     "//div[@id='confirmModal']/div[@class='modal_content']/div[@class='confirm_modal']/div[@class='form_btns']/button").text
#             # print(reserve_text)
#             driver.find_element(By.XPATH,
#                                 "//div[@id='confirmModal']/div[@class='modal_content']/div[@class='confirm_modal']/div[@class='form_btns']/button").click()
#             # 이렇게 하면 바로 예약 됨
#
#         elif calendar.find_element(By.XPATH, date_selected).text.find('팀') == -1:  # 예약일이 없으면 바로 빠져 나와서 처리 속도를 높여줌
#             print('There is no book', d)
#             break
#         else:
#             print('Check your input condition!')
#     except:
#         print('There is no book', d)
#
# driver.close()
