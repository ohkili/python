
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
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.alert import Alert
from bs4 import BeautifulSoup

import schedule
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import date
from apscheduler.jobstores.base import JobLookupError
import ssl
import telegram
import platform
import os
import cpuinfo  # reading cpu serial

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

def driverAct(url):
    os_ver = platform.system()
    plaform_ver = platform.platform()

    if os_ver == 'Darwin' and plaform_ver == 'Darwin-19.6.0-x86_64-i386-64bit':
        executable_path = '/Users/gwon-yonghwan/PycharmProjects/chromedriver'
        # '/Users/home/PycharmProjects/chromedriver'   # '/usr/local/bin/chromedriver'  # 크롬드라이버가 보안에 막혀서 크롬드라이버를 압축풀고 해당 폴더로 이동시켜주었다
        'driver activation for mac os'
        driver = webdriver.Chrome(executable_path=executable_path)
    elif os_ver == 'Darwin' and plaform_ver == 'macOS-10.16-x86_64-i386-64bit':
        executable_path = '/Users/home/PycharmProjects/chromedriver'
        'driver activation for mac os'
        driver = webdriver.Chrome(executable_path=executable_path)

    elif os_ver == 'Windows' and plaform_ver == 'Windows-10-10.0.19041-SP0':
        # executable_path = "C:\\Users\ohkil\\PycharmProjects\\chromedriver_win32\\chromedriver.exe"  # 크롬드라이버가 보안에 막혀서 크롬드라이버를 압축풀고 해당 폴더로 이동시켜주었다
        # executable_path = "C:/Users\ohkil/PycharmProjects/chromedriver_win32/chromedriver.exe"  # 크롬드라이버가 보안에 막혀서 크롬드라이버를 압축풀고 해당 폴더로 이동시켜주었다
        'driver activation for windows pc'
        driver = chromedriver_autorun()
    else:
        print('Check your OS type')
        telegram_message('Check your chrome driver path or version.')

    driver.set_window_size(1400, 1000)  # (가로, 세로)음
    driver.get(url)
    return driver

# REST_API_KEY and refresh_token is borrow
REST_API_KEY ='22644bd965c28d381ea875a9dde9e2d1'
refresh_token = '2hZcRLD01s1Rl0qEA0BhnenFH1om0rtTNimYSgo9cuoAAAF81jvBOA'

# https://kauth.kakao.com/oauth/authorize?client_id={REST API 키}&redirect_uri=https://localhost:3000&response_type=code&scope=talk_message
# https://kauth.kakao.com/oauth/authorize?client_id=22644bd965c28d381ea875a9dde9e2d1&redirect_uri=https://localhost:3000&response_type=code&scope=talk_message
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

def telegram_message(content='Hello world', content_type='text', description='description'):
    telegram_token = "5011897744:AAFvwnQrdllp09gz2Iy_XD6SONWy1-jQuNM"
    telegram_chat_id = 1926421781
    bot = telegram.Bot(token=telegram_token)


    # Bottom is telegram bot manual
    """ 
    # text 보내기
    bot.sendMessage(chat_id=telegram_chat_id, text='hello world')
    # image 보내기 image url
    photo_url = "https://telegram.org/img/t_logo.png"
    bot.sendPhoto(chat_id=telegram_chat_id, photo=photo_url, caption='telegrm logo')
    # hyperlink 보내기
    # 미리보기 기능 off ==>  disable_web_page_preview= True
    # []안에 문자는 제목으로 전송되고, ()안에 hyperlink 넣어주면 됨
    bot.send_message(chat_id=telegram_chat_id, text="[naver 증권](https://finance.naver.com)", parse_mode='Markdown',
                     disable_web_page_preview=False)

    # image 보내기 image file
    # os.getcwd()
    # glob.glob('E:\\python\\' + '*.jpg')
    photo_file = 'E:\\python\\주행기록.jpg'
    bot.sendPhoto(chat_id=telegram_chat_id, photo=open(photo_file, 'rb'), caption='카니발 주행기록') 
    """

    if content_type == 'text':
        # example is 'hello world'
        bot.sendMessage(chat_id=telegram_chat_id, text=content)
    elif content_type == 'imgUrl':
        # example is  "https://telegram.org/img/t_logo.png"
        bot.sendPhoto(chat_id=telegram_chat_id, photo=content, caption=description)
    elif content_type == 'imgFile':
        # example is 'E:\\python\\주행기록.jpg'
        bot.sendPhoto(chat_id=telegram_chat_id, photo=open(content, 'rb'), caption=description)
    elif content_type == 'hyperlink':
        # []안에 문자는 제목으로 전송되고, ()안에 hyperlink 넣어주면 됨
        #  example is "[naver 증권](https://finance.naver.com)"
        content_hyperlink = "[" + description + "](" + content + ")"
        bot.send_message(chat_id=telegram_chat_id, text=content_hyperlink, parse_mode='Markdown',
                         disable_web_page_preview=False)
    else:
        print('You must choice content_type as text, imgUrl, imgFile, hyperlink')

def good_luck_kakao():
      print("Good Luck for Test")
      print( time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
      access_token = access_token_mkr(REST_API_KEY,refresh_token)
      kakao_message('message test from macmini with golf '+ str( time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))),access_token)

def good_luck():
    print("Good Luck for Test")
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    content_new =  'message test from macmini with golf ' + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    telegram_message(content = content_new, content_type='text', description= 'etc' )
def reserve_rivera(loginfo,info_date,reserve_cnt=1,reserve_type='test', multi_date = False):
    # info_rivera = {'url': 'https://www.shinangolf.com/',
    #                'loginPage': 'https://www.shinangolf.com/member/login',
    #                'id': 'ohkili',
    #                'pw': 'Sin!1203'
    #                }
    # loginfo = info_rivera
    # info_date = info_date_test
    #
    'log information from loginfo var. '
    url = loginfo['url']
    loginpage = loginfo['loginPage']
    loginID = loginfo['id']
    loginPW = loginfo['pw']
    'wish date & hour information from info_date var.'
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

    driver.get(url)
    driver.get(loginpage)

    'id for login'
    userId = driver.find_element(By.ID, 'memberId')  # /html/body/div/div[5]/div/div/div/div[2]/div/form/div[1]/div[1]/input
    userId.send_keys(loginID)  # 로그인 할 계정 id

    'password for login'
    userPwd = driver.find_element(By.ID, 'key')  # /html/body/div/div[5]/div/div/div/div[2]/div/form/div[1]/div[2]/input
    userPwd.send_keys(loginPW)
    userPwd.send_keys(Keys.ENTER)

    # log in putton userPwd에 password를 엔터를 치면 되는데, 아래처럼 로그인 버튼을 누를수도 있다
    # loginbtn = driver.find_element(By.XPATH, "//form[@id='loginForm']/div[@class='login_btn']")
    # loginbtn.click()

    '통합 예약/실시간예약 접속 화면'
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
                '원하는 일정 목록에서 년 월 일 정보 추'
                wish_year = dt[:4]
                wish_month = dt[4:6]
                wish_day = dt[6:8]

                '예약 화면의 달력으로 이동'
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
                        '예약 가능한 날짜 추출'
                        s = (calendar_week[0].find_elements(By.XPATH, "//td")[i].text)
                        if s.find('\n')>0:
                            s = s.split('\n')[0]
                            able_date = wish_year + wish_month + s.zfill(2)
                            able_ls.append(able_date)
                        else:
                            pass
                        '예약 가능일이 원하는 날과 같으면 예약 시도 횟수를 +1 한다'
                        if s  == str(int(wish_day)):
                            book_try_cnt += 1
                        else:
                            pass
                        # print(i, s, able_ls, book_try_cnt)


                else:
                    pass

            except:
                print('macro fail : date simple check')
                # access_token = access_token_mkr(REST_API_KEY, refresh_token)
                # kakao_message('rivera macro fail  : date simple check  \n' + str( time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))) , access_token)

                telegram_message(content='rivera macro fail  : date simple check  \n' + str( time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                                 , content_type='text', description='description')

            try:
                if reserve_type == 'real':
                    pass

                elif reserve_type == 'test' and len(able_ls) >0 :
                    '예약 타입이 test 이면서 예약 가능일이 있으면 예약 가능일 첫 날을 dt 변수에 넣는다.'
                    dt = able_ls[0]
                elif reserve_type == 'test' and len(able_ls) ==0 and  book_try_cnt == len(wish_date):
                    '예약 타입이 test 이면서 예약 가능일이 없고 예약 시도횟수와 원하는 날 수가 같다면 반복문에서 빠져나'
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

                '원하는 시간대 골라내기'
                timeTable_filterd = pd.DataFrame()
                for h in wish_hour:
                    first_time = h.split('~')[0]
                    end_time = h.split('~')[1]
                    mask1 = (timeTable['hour'].str[0:2] >= first_time) & (
                                timeTable['hour'].str[0:2] < end_time)  # 시간대 filter

                    timeTable_sorted = timeTable.loc[mask1, :].sort_values('hour')
                    timeTable_filterd = pd.concat([timeTable_filterd, timeTable_sorted])

                timeTable_filterd.reset_index(inplace=True)
                while(reserve_cnt > 0):

                    if hour_option == 'first':
                        index_no = timeTable_filterd['index'].iloc[0]
                    elif hour_option == 'mid':
                        index_no = timeTable_filterd['index'].iloc[round(len(timeTable_sorted) / 2)]
                    elif hour_option == 'last':
                        index_no = timeTable_filterd['index'].iloc[-1]

                    idx = timeTable_filterd[timeTable_filterd['index'] == index_no].index
                    timeTable_filterd = timeTable_filterd.drop(idx)

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
                        # kakao_message(popup_text, access_token)

                        telegram_message(content=popup_text , content_type='text', description='description')

                    elif   reserve_type == 'test' and reserve_text =='예약하기':
                        # 카카오 문자 보내기
                        driver.find_element(By.XPATH,
                                            "//div[@id='confirmModal']/div[@class='modal_content']/div[@class='confirm_modal']/div[@class='form_btns']/a").click()
                        access_token = access_token_mkr(REST_API_KEY, refresh_token)
                        popup_text = '[예약 macro 정상 동작]\n' + '[예약이 된것은 아님]\n'+ popup_text
                        # kakao_message(popup_text, access_token)
                        telegram_message(content=popup_text, content_type='text', description='description')

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
                # access_token = access_token_mkr(REST_API_KEY, refresh_token)
                # kakao_message('rivera macro fail:  targetting reserve  \n' + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))), access_token)
                telegram_message(content='rivera macro fail:  targetting reserve  \n' + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))),
                                 content_type='text', description='description')

        elif date_count == 0:
            break
        else :
            print('Check date_count')
    if book_try_cnt == len(wish_date):
        # access_token = access_token_mkr(REST_API_KEY, refresh_token)
        # kakao_message('There is no able day to book \n' + str( time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))), access_token)
        telegram_message(content='There is no able day to book \n' + str( time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))),
                         content_type='text', description='description')
    else:
        print('Check book_try_cnt')

    print('book_try_cnt',book_try_cnt)
    print('wish_date',wish_date)
    driver.close()
def reserve_rivera_macmini(loginfo,info_date,reserve_try_cnt=9,reserve_type='test', multi_date = False):
    # driver.close()
    # loginfo = info_rivera
    # info_date = info_date_test
    'reserve_try_cnt means n times trying for reservation, when website clock is not sync with code'

    url = loginfo['url']
    loginpage = loginfo['loginPage']
    loginID = loginfo['id']
    loginPW = loginfo['pw']

    wish_date = info_date['wish_date']
    wish_hour = info_date['wish_hour']
    hour_option = info_date['hour_option']

    book_try_cnt = 0
    reserve_succees_cnt = 0
    reserve_need_cnt = len(wish_date) * len(wish_hour)
    date_count = len(wish_date)

    if reserve_type == 'real':
        pass
    elif reserve_type == 'test':
        reserve_try_cnt = 1
    else:
        reserve_try_cnt =0
        telegram_message(content='Please, check your reserve_type', content_type='text', description='description')

    able_ls = []
    try:
        driver = driverAct(url)
    except Exception as e:
        telegram_message(content=repr(e),content_type='text',description='description' )
        telegram_message(content='Check your chrome driver version', content_type='text', description='description')

    driver.get(loginpage)
    # if reserve_cnt is True ,then reservation don't stop
    # if reserve_cnt is False ,then reservation 1 time and stop
    # driver.close()
    # driver.quit()



    # id
    userId = driver.find_element(By.ID, 'memberId')  # /html/body/div/div[5]/div/div/div/div[2]/div/form/div[1]/div[1]/input
    userId.send_keys(loginID)  # 로그인 할 계정 id

    # password
    userPwd = driver.find_element(By.ID, 'key')  # /html/body/div/div[5]/div/div/div/div[2]/div/form/div[1]/div[2]/input
    userPwd.send_keys(loginPW)
    userPwd.send_keys(Keys.ENTER)




    while(reserve_need_cnt > 0 and reserve_try_cnt > 0 ):

        # log in putton userPwd에 password를 엔터를 치면 되는데, 아래처럼 로그인 버튼을 누를수도 있다
        # loginbtn = driver.find_element(By.XPATH, "//form[@id='loginForm']/div[@class='login_btn']")
        # loginbtn.click()

        # 통합 예약/실시간예약
        # reservation = driver.find_element(By.XPATH,"/html/body/div/div[2]/div/div[2]/div[1]/ul/li[1]/div/ul/li[1]/a")  # /html/body/div/div[2]/div/div[2]/div[1]/ul/li[1]/div/ul/li[1]/a
        reservation_open = driver.find_element(By.XPATH,
                                               "/html/body/div/div[2]/div/div[2]/div[1]/ul/li[1]/div/ul/li[1]/a")
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

        for dt in wish_date:
            # dt = wish_date[0]
            if date_count > 0:

                try:
                    wish_year  = dt[:4]
                    wish_month = dt[4:6]
                    wish_day   = dt[6:8]

                    calendar = driver.find_element(By.XPATH, "//div[@class='reservation_table calendar_table']/table/tbody")

                    if reserve_type   ==  'real':
                        pass
                    elif reserve_type == 'test':
                        status_year  = driver.find_element(By.XPATH, "//div[@class='month_wrap']/span[@class ='year']").text[:4]
                        status_month = driver.find_element(By.XPATH, "//div[@class='month_wrap']/span[@class ='month']").text[:2]
                        if wish_year > status_year or wish_month > status_month :
                            driver.find_element(By.XPATH, "//div[@class='month_wrap']/button[@class='next']").click()
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
                    # access_token = access_token_mkr(REST_API_KEY, refresh_token)
                    # kakao_message('rivera macro fail  : date simple check  \n' + str( time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))) , access_token)
                    telegram_message(content='rivera macro fail  : date simple check  \n' + str( time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))),
                                     content_type='text', description='description')


                try:
                    if reserve_type == 'real':
                        pass
                    elif reserve_type == 'test' and len(able_ls) >0 :
                        dt = able_ls[0]

                    elif reserve_type == 'test' and len(able_ls) ==0 and  book_try_cnt == len(wish_date):

                        pass
                    else:
                        print('Check book_try_cnt')



                    date_selected_1 = "//tr/td/a[@class='open'  and @id =" + "'" + dt + "']"
                    date_selected_2 = "//tr/td/a[@class='open active'  and @id =" + "'" + dt + "']"
                    # temp_date = calendar.find_element(By.XPATH, "//tr/td/a[@class='open'  and @id ='20211028']")
                    # temp_date = calendar.find_element(By.XPATH, "//tr/td/a[@class='open active'  and @id ='20211028']")
                    # calendar.find_element(By.XPATH, date_selected).text 에 예약이 가능하면 팀수가 나옴 없으면 예약 불가능하므로 예약 시도 cancel
                    try:
                        date_check1 = calendar.find_element(By.XPATH, date_selected_1).text.find('팀')
                    except:
                        date_check1 = -1

                    try:
                        date_check2 =  calendar.find_element(By.XPATH, date_selected_2).text.find('팀')
                    except:
                        date_check2 = -1

                    if date_check1 >= 0:
                        calendar_selected = calendar.find_element(By.XPATH, date_selected_1)
                    elif date_check2 >= 0:
                        calendar_selected = calendar.find_element(By.XPATH, date_selected_2)
                    elif date_check1 == -1 and date_check2 == -1:   # 예약일이 없으면 바로 빠져 나와서 처리 속도를 높여줌
                        print('There is no book', dt)

                    else :
                        print('Check Calendar')




                     # calendar_selected.click()     # 원하는 날짜에 해당하는 달력 check
                    driver.execute_script("arguments[0].click();", calendar_selected)
                    # calendar.find_element(By.XPATH, date_selected).text
                    reservation_time = WebDriverWait(driver, 30).until(
                        EC.presence_of_all_elements_located((By.XPATH, "//div[@class = 'reservation_table time_table']"))
                    )
                    # reservation_time = driver.find_element(By.XPATH, "//div[@class = 'reservation_table time_table']")
                    reservation_time_list = WebDriverWait(driver, 30).until(
                        EC.presence_of_all_elements_located((By.XPATH, "//table/tbody/tr/td/button"))
                    )
                    # reservation_time_list = reservation_time.find_elements(By.XPATH, "//table/tbody/tr/td/button")


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
                    timeTable_filterd = pd.DataFrame()
                    for h in wish_hour:
                        first_time = h.split('~')[0]
                        end_time = h.split('~')[1]
                        mask1 = (timeTable['hour'].str[0:2] >= first_time) & (
                                    timeTable['hour'].str[0:2] < end_time)  # 시간대 filter

                        timeTable_sorted = timeTable.loc[mask1, :].sort_values('hour')
                        timeTable_filterd = pd.concat([timeTable_filterd, timeTable_sorted])

                    timeTable_filterd.reset_index(inplace=True)
                except:
                    print('macro fail:  making reserve table')
                    # access_token = access_token_mkr(REST_API_KEY, refresh_token)
                    # kakao_message('rivera macro fail:  making reserve table \n' + str(
                    #     time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))), access_token)
                    telegram_message(content='rivera macro fail:  making reserve table \n' + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))),
                                     content_type='text', description='description')
                try:

                    while(reserve_need_cnt > 0):

                        if hour_option == 'first':
                            index_no = timeTable_filterd['index'].iloc[0]
                        elif hour_option == 'mid':
                            index_no = timeTable_filterd['index'].iloc[round(len(timeTable_sorted) / 2)]
                        elif hour_option == 'last':
                            index_no = timeTable_filterd['index'].iloc[-1]

                        idx = timeTable_filterd[timeTable_filterd['index']== index_no].index
                        timeTable_filterd = timeTable_filterd.drop(idx)

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
                        reserve_button = driver.find_element(By.XPATH,
                                            "//div[@id='confirmModal']/div[@class='modal_content']/div[@class='confirm_modal']/div[@class='form_btns']/button")
                        reserve_text = reserve_button.text
                        print(reserve_text)
                        reserve_close_button =  driver.find_element(By.XPATH, "//div[@id='confirmModal']/div[@class='modal_content']/div[@class='confirm_modal']/div[@class='form_btns']/a")

                        if reserve_type == 'real':
                            reserve_button.click()
                            # 이렇게 하면 바로 예약 됨
                            # popup_text = '[예약 완료, macro 정상 동작]\n' +  + popup_text
                            # kakao_message(popup_text, access_token)
                            reserve_succees_cnt += 1
                            reserve_need_cnt    -= 1
                            telegram_message(content=popup_text,content_type='text', description='description')

                        elif   reserve_type == 'test' and reserve_text =='예약하기':
                            # 카카오 문자 보내기
                            reserve_close_button.click()
                            # access_token = access_token_mkr(REST_API_KEY, refresh_token)
                            popup_text = '[예약 macro 정상 동작]\n' + '[예약이 된것은 아님]\n'+ popup_text
                            # kakao_message(popup_text, access_token)
                            reserve_need_cnt =0
                            reserve_try_cnt = 0
                            telegram_message(content=popup_text, content_type='text', description='description')

                        else:
                            print('Check reserve count')
                        # reserve_cnt -= 1  # 예약 건수를 1개 줄임
                        if multi_date == True:
                            date_count -= 1
                        elif multi_date == False:
                            date_count = 0
                        else:
                            print('Check multidate option')


                except:
                    print('macro fail:  targetting reserve while sentence! ')
                    # access_token = access_token_mkr(REST_API_KEY, refresh_token)
                    # kakao_message('rivera macro fail:  targetting reserve while sentence!  \n' + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))), access_token)
                    telegram_message(content='rivera macro fail:  targetting reserve while sentence!  \n' + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))),
                                     content_type='text', description='description')

            elif date_count == 0:
                pass
            else :
                print('Check date_count')
        if book_try_cnt == len(wish_date):
            # access_token = access_token_mkr(REST_API_KEY, refresh_token)
            # kakao_message('There is no able day to book \n' + str( time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))), access_token)
            telegram_message(content='There is no able day to book \n' + str( time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))),
                             content_type='text', description='description')
        else:
            print('Check book_try_cnt')
        if reserve_try_cnt >0 :
            reserve_try_cnt -= 1
        else :
            pass
        print('book_try_cnt',book_try_cnt)
        print('wish_date',wish_date)
        driver.close()


# loginfo = info_ipo

# reserve_try_cnt = 9
# reserve_able_cnt = 3
# reserve_type='test'
# info_date2 = info_date_ipo
def reserve_ipo(loginfo,info_date, reserve_try_cnt  = 9, reserve_type='test', multi_date = False):

    # inforamtion of login date initial variable.
    "로그인에 필요한 정보"
    url       = loginfo['url']
    loginpage = loginfo['loginPage']
    loginID   = loginfo['id']
    loginPW   = loginfo['pw']
    "예약을 원하는 날짜 list"
    wish_date   = info_date['wish_date']
    wish_hour   = info_date['wish_hour']
    hour_option = info_date['hour_option']

    "예약 가능한 일시를 저장하기 위함"
    reservable_table_columns = ['cc', 'course', 'date', 'time', 'status', 'price', 'key_date','key_time','key_course']
    reservable_table = pd.DataFrame(data=[], columns=reservable_table_columns)
    "예약 가능한 일시를 저장하기 위함"
    reservable_time_table = pd.DataFrame()
    "예약 완료한 일시를 저장하기 위함, 대기 예약이 가능하므로 status는 유지함"
    reserve_result_table_columns = ['cc', 'course', 'date', 'time', 'status', 'price']
    reserve_result_table = pd.DataFrame(data=[], columns=reserve_result_table_columns)


    reserve_try_cnt     = reserve_try_cnt # 예약 오픈 일시가 web server 시각과 local pc 시각 불일치를 고려 강제 시도 횟수 지정
    reserve_succees_cnt = 0
    reserve_need_cnt    = len(wish_date) * len(wish_hour)


    if reserve_type == 'real':
        pass
    elif reserve_type == 'test':
        reserve_try_cnt = 1
    else:
        reserve_try_cnt =0
        telegram_message(content= 'ipo_cc : ' + error_msg['reserve_type'], content_type='text', description='description')



    # 2.  log in page open & log in
    try:
        driver = driverAct(url)
    except Exception as e:
        telegram_message(content=repr(e), content_type='text', description='description')
        telegram_message(content='ipo_cc : ' + error_msg['chrome_dirver_version'], content_type='text', description='description')

    try:
        driver.get(loginpage)
    except:
        telegram_message(content='ipo_cc : ' + error_msg['login_url_aborted'], content_type='text', description='description')



    "ID Pasword 입력하여 login"
    try:
        # id
        userId = driver.find_element(By.ID, 'id')
        userId.send_keys(loginID)  # 로그인 할 계정 id

        # password
        userPwd = driver.find_element(By.ID, 'password')
        userPwd.send_keys(loginPW)
        userPwd.send_keys(Keys.ENTER)
    except:
        telegram_message(content='ipo_cc : ' + error_msg['login_fail'], content_type='text',
                         description='description')

    # 리베라에 해당하는 사례임
    # log in putton userPwd에 password를 엔터를 치면 되는데, 아래처럼 로그인 버튼을 누를수도 있다
    # loginbtn = driver.find_element(By.XPATH, "//form[@id='loginForm']/div[@class='login_btn']")
    # loginbtn.click()
    # /html/body/div/div[1]/div[3]/div/ul/li[1]/a
    # 통합 예약/실시간예약
    # reservation = driver.find_element(By.XPATH,"/html/body/div/div[2]/div/div[2]/div[1]/ul/li[1]/div/ul/li[1]/a")  # /html/body/div/div[2]/div/div[2]/div[1]/ul/li[1]/div/ul/li[1]/a

    # 3. reserveation page open

    while(reserve_need_cnt > 0 and reserve_try_cnt > 0 ):
        "예약 화면 open"
        reservation_open = driver.find_element(By.XPATH, "/html/body/div/div[1]/div[3]/div/ul/li[1]/a")
        driver.execute_script("arguments[0].click();", reservation_open)  # 예약 화면 오픈

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

        # 예약 달력, 날짜별 예약 가능 여부 표시 되어 있음
        "Canledar open하여 날짜별 예약 상태 수집"
        driver.find_element(By.XPATH, "//div[@id='timeform']")
        "timeform 아래에 input 속성이 날짜별로 있어 list함"
        date_ls = driver.find_elements(By.XPATH, "//div[@id='timeform']/input")

        for d in date_ls:
            # d = date_ls[15]
            try:

                status = d.get_attribute('name').split('_')[3]
                key_date = d.get_attribute('id')
                date = key_date.split('_')[1]
                # name_col = d.get_attribute('name')
                ['cc', 'course', 'date', 'time', 'status', 'price', 'key_date', 'key_time', 'key_course']
                temp_data = {'cc': ['ipo_cc'],
                             'date': [date],
                             'status': [status],
                             'key_date': [key_date]}
                # temp_1_colums = ['cc','date','status','key_date']
                temp = pd.DataFrame(data=temp_data)

                reservable_table = pd.concat([reservable_table, temp])
            except:
                pass

        reservable_table = reservable_table[reservable_table['status'] == '예약']
        reservable_table.reset_index(drop=True, inplace=True)
        # reservable_table.info()

        # 4. 날짜 선택 기능

        driver.find_element(By.ID, "container")

        # 달력 부분 활성화
        driver.find_element(By.XPATH, "//div[@id='content']/div[@class='txtcont']/div[@class='join_form']")
        driver.find_element(By.XPATH, "//div[@class = 'mt10 mb40 leftcont']")

        # d = wish_date[0] # test용
        # # bottom is exercise
        # wish_date = '20211106'
        # date_temp = "//td[@id=" + wish_date + "]"
        # driver.find_element(By.XPATH, date_temp).text # example = '6\n마감'
        " wishdate filtering"

        temp_table = pd.DataFrame()
        for date_able in wish_date:
            # date_able = wish_date[0]
            temp_table1 = reservable_table[reservable_table['date'] == date_able]
            temp_table = pd.concat([temp_table, temp_table1])
        reservable_table = temp_table

        "달력에서 날짜별 선택 아래 폼으로 찾으면 wishdate를 활성화"
        # date_id = "//td[@id=" + d + "]"
        reservable_table['key_date'] = "//td[@id=" + reservable_table['date'] + "]"

        for key_d in reservable_table['key_date'].unique():
            # key_d = reservable_table['key_date'].unique()[1]
            #
            try:
                " '14\n예약' 형태로 되어 있어 split을 하여 예약 부분을 추출"
                status = driver.find_element(By.XPATH, key_d).text.split('\n')[-1]

                if status == '예약':
                    driver.refresh()  # 'stale error issue solution but past history forgotton. '
                    driver.find_element(By.XPATH, key_d).click()
                    # 이부분에 시간 에약 기능이 들어가야 함

                    driver.find_element(By.XPATH,"//div[@class = 'mt10 mb40 rightcont join_form']")

                    # course 선택
                    course_dict = {'out': "//td[@valign = 'top']/table[@id = 'out_table']/tbody",
                                   'in' :  "//td[@valign = 'top']/table[@id = 'in_table']/tbody"}

                    for c in list(course_dict.keys()):
                        # c = list(course_dict.keys())[1]
                        # print(c)
                        # driver.find_element(By.XPATH,course_dict[c]).text
                        # 시간 list 추출
                        # course_dict['out'] + "/tr[@style = 'cursor:pointer']"

                        time_ls = driver.find_elements(By.XPATH,course_dict[c] + "/tr[@style = 'cursor:pointer']")
                        # time_ls = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(By.XPATH,course_dict[c] + "/tr[@style = 'cursor:pointer']"))
                        driver.implicitly_wait(1)
                        # time.sleep(1)
                        print('time sleep')
                        course_timetable_columns = ['date', 'time', 'price', 'key_time', 'status', 'course']
                        course_timetable = pd.DataFrame()


                        for i in range(len(time_ls)):

                            temp_date = key_d.split('=')[1][:8] # '//td[@id=20220214]'
                            temp_time = time_ls[i].find_element(By.XPATH, "th").text
                            temp_price = time_ls[i].find_element(By.XPATH, "td").text

                            temp_key_time = time_ls[i]
                            course_timetable = pd.concat(
                                [course_timetable, pd.DataFrame([temp_date, temp_time, temp_price, temp_key_time,status, c]).T])

                        print('time ls')
                        temp_key_time.click()
                        ['cc', 'course', 'date', 'time', 'status', 'price', 'key_date', 'key_time', 'key_course']
                        course_timetable.columns = course_timetable_columns



                        left_join_key = ['date', 'status' ]
                        right_join_key = ['date', 'status' ]
                        reservable_table_target = reservable_table[reservable_table['date'] == temp_date]
                        join_table = pd.merge(reservable_table_target,course_timetable,how='left',left_on=left_join_key,right_on=right_join_key)
                        join_table.drop(['course_x','time_x','key_time_x','price_x'],axis=1,inplace=True)
                        join_table.rename(columns={'time_y':'time','price_y':'price','course_y':'course','key_time_y':'key_time'},inplace=True)
                        reservable_time_table = pd.concat([reservable_time_table,join_table])
                        # reservable_time_table['key_time'].iloc[0].click()
                    reservable_time_table.reset_index(drop=True,inplace=True)

                    "220213 02:42 이 위까지 작업하였음"
                    # 4. 시간 선택 기능
                    # 원하는 시간대 골라내기
                    timeTable_masked = pd.DataFrame()
                    for h in wish_hour:
                        try:
                            if reserve_try_cnt >0 :

                                # h = wish_hour[0]
                                first_time = h.split('~')[0]
                                end_time = h.split('~')[1]
                                mask1 = (reservable_time_table['time'].str[0:2] >= first_time) & (
                                        reservable_time_table['time'].str[0:2] < end_time)  # 시간대 filter

                                timeTable_sorted = reservable_time_table.loc[mask1, :].sort_values('time')
                                timeTable_masked = pd.concat([timeTable_masked, timeTable_sorted])
                                timeTable_masked.reset_index(drop=True, inplace=True)
                                # 시간 option에 의해 선택지에서 하나 선택
                                if hour_option == 'first':
                                    index_no = 0
                                elif hour_option == 'mid':
                                    index_no = round(len(timeTable_masked) / 2)
                                elif hour_option == 'last':
                                    index_no = -1
                                # 선택한 시간 옵션으로 하나 고름
                                timeTable_masked.iloc[index_no]['key_time'].click()
                                # 예약 확인
                                reserve_message = driver.find_element(By.XPATH, "//div[@name = 'result' and @id='result']").text
                                if reserve_type == 'real':
                                    reserve_confirm = driver.find_element(By.XPATH,
                                                                          "//form[@name = 'sub04_2' and @id='sub04_2']/div[@class = 'mt20 mb50 btnarea4']/span[@class='btn_enter mr20']")
                                    reserve_confirm.click()
                                    telegram_message('예약 완료:\n' + timeTable_masked.iloc[index_no]['cc'] + '\n' + reserve_message)

                                    reserve_need_cnt -= 1
                                    reserve_try_cnt -= 1

                                elif reserve_type == 'test':

                                    telegram_message(
                                        '예약 Test:실제로 예약된 것은 아님\n' + timeTable_masked.iloc[index_no]['cc'] + '\n' + reserve_message)
                                    reserve_cancel = driver.find_element(By.XPATH,
                                                                          "//form[@name = 'sub04_2' and @id='sub04_2']/div[@class = 'mt20 mb50 btnarea4']/span[@class='btn_cancel']")

                                    reserve_try_cnt = 0
                                else:
                                    continue
                        except:
                            pass


                #
                # elif status == '마감' or status =='오픈전':
                #     reserve_result.append([d,status])
                # else:
                #     reserve_result.append([d, 'error'])
            except:
                print('error')
                reserve_try_cnt -=1
        driver.close()

        "220215 01:14 이 위까지 작업하였음"





        #여기까지 작성 2/15 12:09

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

"resrve_ipo2는 실패"
def reserve_ipo2(loginfo,info_date2, reserve_try_cnt  = 9,reserve_able_cnt = 3, reserve_type='test', multi_date = False):

    # inforamtion of login date initial variable.
    "로그인에 필요한 정보"
    url       = loginfo['url']
    loginpage = loginfo['loginPage']
    loginID   = loginfo['id']
    loginPW   = loginfo['pw']
    "예약을 원하는 날짜 list"
    info_date2.keys()
    wish_date = []
    wish_date = [info_date2[k][0] for k in list(info_date2.keys()) ]
    # wish_date   = info_date['wish_date']
    # wish_hour = []
    # wish_hour = [info_date2[k][1] for k in list(info_date2.keys()) ]
    # wish_hour   = info_date['wish_hour']
    # hour_option =[]
    # hour_option = [info_date2[k][2] for k in list(info_date2.keys()) ]
    # hour_option = info_date['hour_option']

    "예약 가능한 일시를 저장하기 위함"
    reservable_table_columns = ['cc', 'course', 'date', 'time', 'status', 'price', 'key_date','key_time','key_course']
    reservable_table = pd.DataFrame(data=[], columns=reservable_table_columns)
    "예약 가능한 일시를 저장하기 위함"

    reserve_result_table_columns = ['cc', 'course', 'date', 'time', 'status', 'price']
    reserve_result_table = pd.DataFrame(data=[], columns=reserve_result_table_columns)


    reserve_try_cnt     = reserve_try_cnt # 예약 오픈 일시가 web server 시각과 local pc 시각 불일치를 고려 강제 시도 횟수 지정
    reserve_succees_cnt = 0
    reserve_need_cnt    = len(info_date2)


    if reserve_type == 'real':
        pass
    elif reserve_type == 'test':
        reserve_try_cnt = 1
        reserve_able_cnt =1
    else:
        reserve_try_cnt =0
        telegram_message(content= 'ipo_cc : ' + error_msg['reserve_type'], content_type='text', description='description')



    # 2.  log in page open & log in
    try:
        driver = driverAct(url)
    except Exception as e:
        telegram_message(content=repr(e), content_type='text', description='description')
        telegram_message(content='ipo_cc : ' + error_msg['chrome_dirver_version'], content_type='text', description='description')

    try:
        driver.get(loginpage)
    except:
        telegram_message(content='ipo_cc : ' + error_msg['login_url_aborted'], content_type='text', description='description')



    "ID Pasword 입력하여 login"
    try:
        # id
        userId = driver.find_element(By.ID, 'id')
        userId.send_keys(loginID)  # 로그인 할 계정 id

        # password
        userPwd = driver.find_element(By.ID, 'password')
        userPwd.send_keys(loginPW)
        userPwd.send_keys(Keys.ENTER)
    except:
        telegram_message(content='ipo_cc : ' + error_msg['login_fail'], content_type='text',
                         description='description')

    # 리베라에 해당하는 사례임
    # log in putton userPwd에 password를 엔터를 치면 되는데, 아래처럼 로그인 버튼을 누를수도 있다
    # loginbtn = driver.find_element(By.XPATH, "//form[@id='loginForm']/div[@class='login_btn']")
    # loginbtn.click()
    # /html/body/div/div[1]/div[3]/div/ul/li[1]/a
    # 통합 예약/실시간예약
    # reservation = driver.find_element(By.XPATH,"/html/body/div/div[2]/div/div[2]/div[1]/ul/li[1]/div/ul/li[1]/a")  # /html/body/div/div[2]/div/div[2]/div[1]/ul/li[1]/div/ul/li[1]/a

    # 3. reserveation page open

    while(reserve_need_cnt > 0 and reserve_try_cnt > 0 and reserve_able_cnt > 0 ):
        "예약 화면 open"
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

        # 예약 달력, 날짜별 예약 가능 여부 표시 되어 있음
        "Canledar open하여 날짜별 예약 상태 수집"
        driver.find_element(By.XPATH, "//div[@id='timeform']")
        "timeform 아래에 input 속성이 날짜별로 있어 list함"
        date_ls = driver.find_elements(By.XPATH, "//div[@id='timeform']/input")


        for d in date_ls:
            # d = date_ls[15]
            try:

                status = d.get_attribute('name').split('_')[3]
                key_date = d.get_attribute('id')
                date      = key_date.split('_')[1]
                # name_col = d.get_attribute('name')
                ['cc', 'course', 'date', 'time', 'status', 'price', 'key_date', 'key_time', 'key_course']
                temp_data = {'cc':['ipo_cc'],
                          'date':[date],
                          'status':[status],
                          'key_date':[ key_date]}
                # temp_1_colums = ['cc','date','status','key_date']
                temp = pd.DataFrame(data=temp_data)

                reservable_table = pd.concat([reservable_table,temp])
            except:
                pass

        reservable_table = reservable_table[reservable_table['status'] == '예약']
        reservable_table.reset_index(drop=True,inplace=True)
        # reservable_table.info()

        # 4. 날짜 선택 기능

        driver.find_element(By.ID, "container")

        # 달력 부분 활성화
        driver.find_element(By.XPATH, "//div[@id='content']/div[@class='txtcont']/div[@class='join_form']")
        driver.find_element(By.XPATH,"//div[@class = 'mt10 mb40 leftcont']")

        # d = wish_date[0] # test용
        # # bottom is exercise
        # wish_date = '20211106'
        # date_temp = "//td[@id=" + wish_date + "]"
        # driver.find_element(By.XPATH, date_temp).text # example = '6\n마감'
        " wishdate filtering"

        temp_table = pd.DataFrame()
        info_date_temp = {}
        for date_able in wish_date:
            # date_able = wish_date[0]
            temp_table1 = reservable_table[reservable_table['date'] == date_able]
            temp_table = pd.concat([temp_table,temp_table1])
        for kd in list(info_date2.keys()):
            if info_date2[kd][0] in temp_table['date'].unique():
                info_date_temp[kd] = info_date2[kd]

        reservable_table = temp_table

        "달력에서 날짜별 선택 아래 폼으로 찾으면 wishdate를 활성화"
        # date_id = "//td[@id=" + d + "]"
        reservable_table['key_date'] = "//td[@id=" + reservable_table['date'] + "]"
        '여기서 날짜를 infro date dic에서 가져와서 순서대로 진행해야 함 2/27 01:00'



        for kd in list(info_date_temp.keys()):
            reservable_time_table = pd.DataFrame()
            "예약 완료한 일시를 저장하기 위함, 대기 예약이 가능하므로 status는 유지함"
            kd = list(info_date_temp.keys())[0]
            if reserve_able_cnt > 0:
                if info_date_temp[kd][0] in reservable_table['date'].unique():
                    key_d = "//td[@id=" + info_date_temp[kd][0] + "]"
                    try:
                        " '14\n예약' 형태로 되어 있어 split을 하여 예약 부분을 추출"
                        status = driver.find_element(By.XPATH, key_d).text.split('\n')[-1]

                        if status == '예약':
                            driver.refresh()  # 'stale error issue solution but past history forgotton. '
                            driver.find_element(By.XPATH, key_d).click()
                            # 이부분에 시간 에약 기능이 들어가야 함

                            driver.find_element(By.XPATH,"//div[@class = 'mt10 mb40 rightcont join_form']")

                            # course 선택
                            course_dict = {'out': "//td[@valign = 'top']/table[@id = 'out_table']/tbody",
                                           'in' :  "//td[@valign = 'top']/table[@id = 'in_table']/tbody"}
                            course_timetable_columns = ['date', 'time', 'price', 'key_time', 'status', 'course']
                            course_timetable = pd.DataFrame()
                            for c in list(course_dict.keys()):
                                c = list(course_dict.keys())[0]
                                print(c)
                                # driver.find_element(By.XPATH,course_dict[c]).text
                                # 시간 list 추출
                                # course_dict['out'] + "/tr[@style = 'cursor:pointer']"

                                time_ls = driver.find_elements(By.XPATH,course_dict[c] + "/tr[@style = 'cursor:pointer']")
                                # time_ls = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(By.XPATH,course_dict[c] + "/tr[@style = 'cursor:pointer']"))
                                driver.implicitly_wait(1)
                                # time.sleep(1)
                                print('time sleep')



                                for i in range(len(time_ls)):
                                    # i = 1
                                    temp_date = key_d.split('=')[1][:8] # '//td[@id=20220214]'
                                    temp_time = time_ls[i].find_element(By.XPATH, "th").text
                                    temp_price = time_ls[i].find_element(By.XPATH, "td").text

                                    temp_key_time = time_ls[i]
                                    course_timetable = pd.concat(
                                        [course_timetable, pd.DataFrame([temp_date, temp_time, temp_price, temp_key_time,status, c]).T])

                                    print('time ls')
                                    # temp_key_time.click()
                                    ['cc', 'course', 'date', 'time', 'status', 'price', 'key_date', 'key_time', 'key_course']
                                    course_timetable.columns = course_timetable_columns



                                    left_join_key = ['date', 'status' ]
                                    right_join_key = ['date', 'status' ]
                                    reservable_table_target = reservable_table[reservable_table['date'] == temp_date]
                                    join_table = pd.merge(reservable_table_target,course_timetable,how='left',left_on=left_join_key,right_on=right_join_key)
                                    join_table.drop(['course_x','time_x','key_time_x','price_x'],axis=1,inplace=True)
                                    join_table.rename(columns={'time_y':'time','price_y':'price','course_y':'course','key_time_y':'key_time'},inplace=True)
                                    reservable_time_table = pd.concat([reservable_time_table,join_table])
                                    # reservable_time_table['key_time'].iloc[0].click()
                                    reservable_time_table.reset_index(drop=True,inplace=True)

                                "220213 02:42 이 위까지 작업하였음"
                                # 4. 시간 선택 기능
                                # 원하는 시간대 골라내기
                                wish_hour = info_date_temp[kd][1]
                                hour_option = info_date_temp[kd][2]



                            # timeTable_masked = pd.DataFrame()

                            try:
                                first_time = wish_hour.split('~')[0]
                                end_time = wish_hour.split('~')[1]
                                mask1 = (reservable_time_table['time'].str[0:2] >= first_time) & (
                                        reservable_time_table['time'].str[0:2] < end_time)  # 시간대 filter

                                timeTable_sorted = reservable_time_table.loc[mask1, :].sort_values('time')
                                # timeTable_masked = pd.concat([timeTable_masked, timeTable_sorted])
                                timeTable_masked = timeTable_sorted
                                timeTable_masked.reset_index(drop=True, inplace=True)
                                # 시간 option에 의해 선택지에서 하나 선택
                                if hour_option == 'first':
                                    index_no = 0
                                elif hour_option == 'mid':
                                    index_no = round(len(timeTable_masked) / 2)
                                elif hour_option == 'last':
                                    index_no = -1
                                # 선택한 시간 옵션으로 하나 고름
                                timeTable_masked.iloc[index_no]['key_time'].click()
                                # 예약 확인
                                reserve_price = timeTable_masked.iloc[index_no]['price']
                                reserve_message = driver.find_element(By.XPATH, "//div[@name = 'result' and @id='result']").text + ' Price:' + reserve_price


                                if reserve_type == 'real':
                                    reserve_confirm = driver.find_element(By.XPATH,
                                                                          "//form[@name = 'sub04_2' and @id='sub04_2']/div[@class = 'mt20 mb50 btnarea4']/span[@class='btn_enter mr20']")
                                    reserve_confirm.click()
                                    telegram_message('예약 완료:\n' + timeTable_masked.iloc[index_no]['cc'] + '\n' + reserve_message)

                                    reserve_need_cnt -= 1
                                    reserve_able_cnt -= 1

                                elif reserve_type == 'test':

                                    telegram_message(
                                        '예약 Test:실제로 예약된 것은 아님\n' + timeTable_masked.iloc[index_no]['cc'] + '\n' + reserve_message)
                                    reserve_cancel = driver.find_element(By.XPATH,
                                                                          "//form[@name = 'sub04_2' and @id='sub04_2']/div[@class = 'mt20 mb50 btnarea4']/span[@class='btn_cancel']")

                                    reserve_try_cnt = 0
                                    reserve_able_cnt = 0
                            except:
                                pass
                    except:
                        pass

                else:
                    pass
            else:
                continue

        reserve_try_cnt -= 1

                            #
                            # elif status == '마감' or status =='오픈전':
                            #     reserve_result.append([d,status])
                            # else:
                            #     reserve_result.append([d, 'error'])

    driver.close()

    "220215 01:14 이 위까지 작업하였음"





    #여기까지 작성 2/15 12:09

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
"resrve_ipo3는 성공"
def reserve_ipo3(loginfo,info_date2, reserve_try_cnt  = 9,reserve_able_cnt = 3, reserve_type='test', multi_date = False):

    # inforamtion of login date initial variable.
    "로그인에 필요한 정보"
    url       = loginfo['url']
    loginpage = loginfo['loginPage']
    loginID   = loginfo['id']
    loginPW   = loginfo['pw']
    "예약을 원하는 날짜 list"
    info_date2.keys()
    wish_date = []
    wish_date = [info_date2[k][0] for k in list(info_date2.keys()) ]
    # wish_date   = info_date['wish_date']
    # wish_hour = []
    # wish_hour = [info_date2[k][1] for k in list(info_date2.keys()) ]
    # wish_hour   = info_date['wish_hour']
    # hour_option =[]
    # hour_option = [info_date2[k][2] for k in list(info_date2.keys()) ]
    # hour_option = info_date['hour_option']

    "예약 가능한 일시를 저장하기 위함"
    reservable_table_columns = ['cc', 'course', 'date', 'time', 'status', 'price', 'key_date','key_time','key_course']
    reservable_table = pd.DataFrame(data=[], columns=reservable_table_columns)
    "예약 가능한 일시를 저장하기 위함"

    reserve_result_table_columns = ['cc', 'course', 'date', 'time', 'status', 'price']
    reserve_result_table = pd.DataFrame(data=[], columns=reserve_result_table_columns)


    reserve_try_cnt     = reserve_try_cnt # 예약 오픈 일시가 web server 시각과 local pc 시각 불일치를 고려 강제 시도 횟수 지정
    reserve_succees_cnt = 0
    reserve_need_cnt    = len(info_date2)


    if reserve_type == 'real':
        pass
    elif reserve_type == 'test':
        reserve_try_cnt = 1
        reserve_able_cnt =1
        pass
    else:
        reserve_try_cnt =0
        telegram_message(content= 'ipo_cc : ' + error_msg['reserve_type'], content_type='text', description='description')



    # 2.  log in page open & log in
    try:
        driver = driverAct(url)
    except Exception as e:
        telegram_message(content=repr(e), content_type='text', description='description')
        telegram_message(content='ipo_cc : ' + error_msg['chrome_dirver_version'], content_type='text', description='description')

    try:
        driver.get(loginpage)
    except:
        telegram_message(content='ipo_cc : ' + error_msg['login_url_aborted'], content_type='text', description='description')



    "ID Pasword 입력하여 login"
    try:
        # id
        userId = driver.find_element(By.ID, 'id')
        userId.send_keys(loginID)  # 로그인 할 계정 id

        # password
        userPwd = driver.find_element(By.ID, 'password')
        userPwd.send_keys(loginPW)
        userPwd.send_keys(Keys.ENTER)
    except:
        telegram_message(content='ipo_cc : ' + error_msg['login_fail'], content_type='text',
                         description='description')

    # 리베라에 해당하는 사례임
    # log in putton userPwd에 password를 엔터를 치면 되는데, 아래처럼 로그인 버튼을 누를수도 있다
    # loginbtn = driver.find_element(By.XPATH, "//form[@id='loginForm']/div[@class='login_btn']")
    # loginbtn.click()
    # /html/body/div/div[1]/div[3]/div/ul/li[1]/a
    # 통합 예약/실시간예약
    # reservation = driver.find_element(By.XPATH,"/html/body/div/div[2]/div/div[2]/div[1]/ul/li[1]/div/ul/li[1]/a")  # /html/body/div/div[2]/div/div[2]/div[1]/ul/li[1]/div/ul/li[1]/a

    # 3. reserveation page open

    reservation_log_path = "D:/result_reservation.txt"
    if os.path.exists(reservation_log_path):
        os.remove(reservation_log_path)
    else:
        pass
    result_not_able_log_path = "D:/result_not_able.txt"
    if os.path.exists(result_not_able_log_path):
        os.remove(result_not_able_log_path)
    else:
        pass

    while(reserve_need_cnt > 0 and reserve_try_cnt > 0 and reserve_able_cnt > 0 ):
        "예약 화면 open"
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

        # 예약 달력, 날짜별 예약 가능 여부 표시 되어 있음
        "Canledar open하여 날짜별 예약 상태 수집"
        driver.find_element(By.XPATH, "//div[@id='timeform']")
        "timeform 아래에 input 속성이 날짜별로 있어 list함"
        date_ls = driver.find_elements(By.XPATH, "//div[@id='timeform']/input")


        for d in date_ls:
            # d = date_ls[15]
            try:

                status = d.get_attribute('name').split('_')[3]
                key_date = d.get_attribute('id')
                date      = key_date.split('_')[1]
                # name_col = d.get_attribute('name')
                ['cc', 'course', 'date', 'time', 'status', 'price', 'key_date', 'key_time', 'key_course']
                temp_data = {'cc':['ipo_cc'],
                          'date':[date],
                          'status':[status],
                          'key_date':[ key_date]}
                # temp_1_colums = ['cc','date','status','key_date']
                temp = pd.DataFrame(data=temp_data)

                reservable_table = pd.concat([reservable_table,temp])
            except:
                pass

        reservable_table = reservable_table[reservable_table['status'] == '예약']
        reservable_table.reset_index(drop=True,inplace=True)
        # reservable_table.info()

        # 4. 날짜 선택 기능

        driver.find_element(By.ID, "container")

        # 달력 부분 활성화
        driver.find_element(By.XPATH, "//div[@id='content']/div[@class='txtcont']/div[@class='join_form']")
        driver.find_element(By.XPATH,"//div[@class = 'mt10 mb40 leftcont']")

        # d = wish_date[0] # test용
        # # bottom is exercise
        # wish_date = '20211106'
        # date_temp = "//td[@id=" + wish_date + "]"
        # driver.find_element(By.XPATH, date_temp).text # example = '6\n마감'
        " wishdate filtering"

        temp_table = pd.DataFrame()
        info_date_temp = {}
        for date_able in wish_date:
            # date_able = wish_date[0]
            temp_table1 = reservable_table[reservable_table['date'] == date_able]
            temp_table = pd.concat([temp_table,temp_table1])
        for kd in list(info_date2.keys()):
            if info_date2[kd][0] in temp_table['date'].unique():
                info_date_temp[kd] = info_date2[kd]

        reservable_table = temp_table

        "달력에서 날짜별 선택 아래 폼으로 찾으면 wishdate를 활성화"
        # date_id = "//td[@id=" + d + "]"
        reservable_table['key_date'] = "//td[@id=" + reservable_table['date'] + "]"
        '여기서 날짜를 infro date dic에서 가져와서 순서대로 진행해야 함 2/27 01:00'
        if len(reservable_table) == 0 :

            telegram_message('예약 가능일 없음\n' + '당신의 요청 예약일\n' + str(info_date2))
            print('예약 가능일 없음\n' + '당신의 요청 예약일\n' + str(info_date2))
            time.sleep(1)

            file = open(result_not_able_log_path, 'w')
            file.write('예약 가능일 없음\n' + '당신의 요청 예약일\n' + str(info_date2))
            file.close()

            break

        else:
            pass


        for kd in list(info_date_temp.keys()):
            reservable_time_table = pd.DataFrame()
            "예약 완료한 일시를 저장하기 위함, 대기 예약이 가능하므로 status는 유지함"
            # kd = list(info_date_temp.keys())[0]
            if reserve_able_cnt > 0:
                if info_date_temp[kd][0] in reservable_table['date'].unique():
                    key_d = "//td[@id=" + info_date_temp[kd][0] + "]"
                    try:
                        " '14\n예약' 형태로 되어 있어 split을 하여 예약 부분을 추출"
                        status = driver.find_element(By.XPATH, key_d).text.split('\n')[-1]

                        if status == '예약':
                            driver.refresh()  # 'stale error issue solution but past history forgotton. '
                            driver.find_element(By.XPATH, key_d).click()
                            # 이부분에 시간 에약 기능이 들어가야 함

                            driver.find_element(By.XPATH,"//div[@class = 'mt10 mb40 rightcont join_form']")

                            # course 선택
                            course_dict = {'out': "//td[@valign = 'top']/table[@id = 'out_table']/tbody",
                                           'in' :  "//td[@valign = 'top']/table[@id = 'in_table']/tbody"}

                            for c in list(course_dict.keys()):
                                # c = list(course_dict.keys())[0]
                                # print(c)
                                # driver.find_element(By.XPATH,course_dict[c]).text
                                # 시간 list 추출
                                # course_dict['out'] + "/tr[@style = 'cursor:pointer']"

                                time_ls = driver.find_elements(By.XPATH,course_dict[c] + "/tr[@style = 'cursor:pointer']")
                                # time_ls = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(By.XPATH,course_dict[c] + "/tr[@style = 'cursor:pointer']"))
                                driver.implicitly_wait(1)
                                # time.sleep(1)
                                # print('time sleep')



                                for i in range(len(time_ls)):
                                    # i = 2
                                    course_timetable_columns = ['date', 'time', 'price', 'key_time', 'status', 'course']
                                    course_timetable = pd.DataFrame()
                                    temp_date = key_d.split('=')[1][:8] # '//td[@id=20220214]'
                                    temp_time = time_ls[i].find_element(By.XPATH, "th").text
                                    temp_price = time_ls[i].find_element(By.XPATH, "td").text

                                    temp_key_time = time_ls[i]
                                    course_timetable = pd.concat(
                                        [course_timetable, pd.DataFrame([temp_date, temp_time, temp_price, temp_key_time,status, c]).T])

                                    # print('time ls')
                                    # temp_key_time.click()
                                    ['cc', 'course', 'date', 'time', 'status', 'price', 'key_date', 'key_time', 'key_course']
                                    course_timetable.columns = course_timetable_columns



                                    left_join_key = ['date', 'status' ]
                                    right_join_key = ['date', 'status' ]
                                    reservable_table_target = reservable_table[reservable_table['date'] == temp_date]
                                    join_table = pd.merge(reservable_table_target,course_timetable,how='left',left_on=left_join_key,right_on=right_join_key)
                                    join_table.drop(['course_x','time_x','key_time_x','price_x'],axis=1,inplace=True)
                                    join_table.rename(columns={'time_y':'time','price_y':'price','course_y':'course','key_time_y':'key_time'},inplace=True)

                                    reservable_time_table = pd.concat([reservable_time_table,join_table])
                                    # reservable_time_table['key_time'].iloc[0].click()
                                    reservable_time_table.reset_index(drop=True,inplace=True)

                                "220213 02:42 이 위까지 작업하였음"
                                # 4. 시간 선택 기능
                                # 원하는 시간대 골라내기
                                wish_hour = info_date_temp[kd][1]
                                hour_option = info_date_temp[kd][2]



                            # timeTable_masked = pd.DataFrame()

                            try:
                                first_time = wish_hour.split('~')[0]
                                end_time = wish_hour.split('~')[1]
                                mask1 = (reservable_time_table['time'].str[0:2] >= first_time) & (
                                        reservable_time_table['time'].str[0:2] < end_time)  # 시간대 filter

                                timeTable_sorted = reservable_time_table.loc[mask1, :].sort_values('time')
                                # timeTable_masked = pd.concat([timeTable_masked, timeTable_sorted])
                                timeTable_masked = timeTable_sorted
                                timeTable_masked.reset_index(drop=True, inplace=True)
                                # 시간 option에 의해 선택지에서 하나 선택
                                if hour_option == 'first':
                                    index_no = 0
                                elif hour_option == 'mid':
                                    index_no = round(len(timeTable_masked) / 2)
                                elif hour_option == 'last':
                                    index_no = -1
                                # 선택한 시간 옵션으로 하나 고름
                                timeTable_masked.iloc[index_no]['key_time'].click()
                                # 예약 확인
                                reserve_price = timeTable_masked.iloc[index_no]['price']
                                reserve_message = driver.find_element(By.XPATH, "//div[@name = 'result' and @id='result']").text + ' Price:' + reserve_price


                                if reserve_type == 'real':
                                    reserve_confirm = driver.find_element(By.XPATH,
                                                                          "//form[@name = 'sub04_2' and @id='sub04_2']/div[@class = 'mt20 mb50 btnarea4']/span[@class='btn_enter mr20']")
                                    reserve_confirm.click()
                                    final_reserve_message = '예약 완료:\n' + timeTable_masked.iloc[index_no]['cc'] + '\n' + reserve_message
                                    telegram_message(final_reserve_message)
                                    print(final_reserve_message)
                                    time.sleep(1)
                                    # print('pause')

                                    reserve_need_cnt -= 1
                                    reserve_able_cnt -= 1

                                elif reserve_type == 'test':
                                    final_reserve_message = '예약 Test:실제로 예약된 것은 아님\n' + timeTable_masked.iloc[index_no]['cc'] + '\n' + reserve_message
                                    telegram_message(final_reserve_message)
                                    print(final_reserve_message)
                                    time.sleep(1)
                                    # print('pause')
                                    reserve_cancel = driver.find_element(By.XPATH,
                                                                          "//form[@name = 'sub04_2' and @id='sub04_2']/div[@class = 'mt20 mb50 btnarea4']/span[@class='btn_cancel']")

                                    reserve_try_cnt = 0
                                    reserve_able_cnt = 0

                                reservation_log_path = "D:/result_reservation.txt"
                                if os.path.exists(reservation_log_path):
                                    file = open(reservation_log_path, 'a')
                                    file.write('\n'+ final_reserve_message +'\n')
                                    file.close()
                                else:
                                    file = open(reservation_log_path, 'w')
                                    file.write(final_reserve_message +'\n')
                                    file.close()
                            except:
                                pass
                    except:
                        pass

                else:
                    pass
            else:
                continue

        reserve_try_cnt -= 1

                            #
                            # elif status == '마감' or status =='오픈전':
                            #     reserve_result.append([d,status])
                            # else:
                            #     reserve_result.append([d, 'error'])

    driver.close()

    "220215 01:14 이 위까지 작업하였음"





    #여기까지 작성 2/15 12:09

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
def info_date_test2():

    #  wish_date 자동 생성
    info_date_test2 ={}
    tm = time.time()
    for t in range(30):
        d = tm + t * 86400
        temp_tm = time.localtime(d)
        string = time.strftime('%Y%m%d', temp_tm)
        info_date_test2[t] = [string,'05~23','first']

    return info_date_test2
# a = info_date_test()
# time_ls =[]
# tm = time.time()
# for t in range(2):
#     d = tm + t* 86400
#     temp_tm = time.localtime(d)
#     string = time.strftime('%Y%m%d', temp_tm)
#     time_ls.append(string)
# info_date_test = {'wish_date': time_ls,
#                 'wish_hour': ['05~23'],
#                 'hour_option': 'first'   }

# info_date_test = {'wish_date': ['20211016','20211017'],
#                  'wish_hour': ['05~23'],
#                  'hour_option': 'first'
#                  }


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

def info_date_ex():
    try:
        columnNames = ['Order', 'Date', 'Front_Time', 'End_Time', 'Filter']
        columnNames1 = ['ID', 'Password']

        info_ipo = {'url': 'http://ipo-cc.co.kr/cmm/main/mainPage.do',
                    'loginPage': 'https://ipocc.com/uat/uia/egovLoginUsr.do',
                    'id': '',
                    'pw': ''
                    }

        temp = pd.read_excel('D:/ipo_reserve_order.xlsx', sheet_name='timeTable')
        temp1 = pd.read_excel('D:/ipo_reserve_order.xlsx', sheet_name='ID')

        temp.columns = columnNames
        temp = temp.astype('str')
        temp['Front_Time'] = temp['Front_Time'].apply(lambda x: '0' + x if len(x) == 1 else x)
        temp['End_Time'] = temp['End_Time'].apply(lambda x: '0' + x if len(x) == 1 else x)
        temp['Filter'] = temp['Filter'].apply(lambda x: x.lower())
        temp['Filter'] = temp['Filter'].apply(lambda x: 'first' if x[0] == 'f' else 'mid' if x[0] == 'm' else 'last')

        temp.reset_index(drop=True, inplace=True)

        info_date2 = {}
        for i in range(len(temp)):
            info_date2[temp['Order'].iloc[i]] = [temp['Date'].iloc[i],
                                                 temp['Front_Time'].iloc[i] + '~' + temp['End_Time'].iloc[i],
                                                 temp['Filter'].iloc[i]]

        temp1.columns = columnNames1
        temp1.reset_index(drop=True, inplace=True)

        info_ipo['id'] = temp1['ID'].iloc[0]
        info_ipo['pw'] = temp1['Password'].iloc[0]

    except:
        print('Check your file, file name is ipo_reserve_order.xlsx')

    return info_date2

def info_ipo_ex():

    try:
        columnNames = ['Order', 'Date', 'Front_Time', 'End_Time', 'Filter']
        columnNames1 = ['ID','Password']
        columnNames2 = ['Gen_key', 'Pass_key']

        "part of info of ipo cc url"
        info_ipo = {'url': 'http://ipo-cc.co.kr/cmm/main/mainPage.do',
                    'loginPage': 'https://ipocc.com/uat/uia/egovLoginUsr.do',
                    'id': '',
                    'pw': ''
                    }

        temp = pd.read_excel('D:/ipo_reserve_order.xlsx',sheet_name='timeTable')
        temp1 = pd.read_excel('D:/ipo_reserve_order.xlsx', sheet_name='cc')
        temp2 = pd.read_excel('D:/ipo_reserve_order.xlsx', sheet_name='macro')

        "part of info reserve order date"
        temp.columns = columnNames
        temp = temp.astype('str')
        temp['Front_Time'] = temp['Front_Time'].apply(lambda x : '0' + x if len(x) == 1 else x)
        temp['End_Time'] = temp['End_Time'].apply(lambda x : '0' + x if len(x) == 1 else x)
        temp['Filter'] = temp['Filter'].apply(lambda x: x.lower())
        temp['Filter'] = temp['Filter'].apply(lambda x: 'first' if x[0] == 'f' else 'mid' if x[0] =='m' else 'last')
        temp.reset_index(drop=True, inplace=True)

        info_date2 ={}
        for i in range(len(temp)):
            info_date2[temp['Order'].iloc[i]] = [temp['Date'].iloc[i], temp['Front_Time'].iloc[i] +'~' + temp['End_Time'].iloc[i], temp['Filter'].iloc[i]]

        "part of info login ID & Password"
        temp1.columns = columnNames1
        temp1.reset_index(drop=True, inplace=True)

        info_ipo['id'] = temp1['ID'].iloc[0]
        info_ipo['pw'] = temp1['Password'].iloc[0]

        "part of info macro gen & pass key"
        temp2.columns = columnNames2
        temp2.reset_index(drop=True, inplace=True)

        key_pair = {}

        key_pair['Gen_key'] = temp2['Gen_key'].iloc[0]
        key_pair['Pass_key'] = temp2['Pass_key'].iloc[0]

    except:
        print('Check your file, file name is ipo_reserve_order.xlsx')

    return  info_ipo, info_date2,key_pair

error_msg = {'login_url_aborted    ':'Check your login url',
             'login_fail'           :'Check your login id or password',
             'reserve_type'         :'Check your resever type or typo',
             'chrome_dirver_version': 'Check your chrome driver version'
             }


info_ipo = {'url'      : 'http://ipo-cc.co.kr/cmm/main/mainPage.do',
            'loginPage': 'https://ipocc.com/uat/uia/egovLoginUsr.do',
             'id'      : 'ohkili',
             'pw'      : 'Ipocc!1203'
               }
info_rivera = {'url': 'https://www.shinangolf.com/',
               'loginPage': 'https://www.shinangolf.com/member/login',
               'id': 'ohkili',
               'pw': 'Sin!1203'

               }

# 날짜 고르기
info_date = {'wish_date': ['20220302', '20220303'],
           'wish_hour': ['07~09', '18~19'],
           'hour_option': 'first'
           } # hour_option 'first, 'mid', 'last'

info_date2 = {'wish_1st_datehour': ['20220224', '07~09','first'],
              'wish_2nd_datehour': ['20220228', '08~09', 'mid'],
              'wish_3rd_datehour': ['20220302', '07~08', 'mid'],
              'wish_4th_datehour': ['20220303', '10~19', 'mid'],
              'wish_5th_datehour': ['20220306', '10~19', 'mid'],
              'wish_6th_datehour': ['20220309', '11~19', 'mid'],
              'wish_7th_datehour': ['20220310', '13~19', 'mid'],
              'wish_8th_datehour': ['20220307', '08~17', 'last'],
              'wish_9th_datehour': ['20220307', '04~19', 'mid'],
           } # hour_option 'first, 'mid', 'last'



info_date_ipo ={'wish_1st_datehour': ['20220312', '07~09','first'],
                'wish_2nd_datehour': ['20220312', '11~14', 'mid'],
                'wish_3rd_datehour': ['20220312', '10~12', 'mid'],
                'wish_4th_datehour': ['20220312', '14~19', 'mid'],
                # 'wish_5th_datehour': ['20220306', '10~19', 'mid'],
              # 'wish_6th_datehour': ['20220309', '11~19', 'mid'],
              # 'wish_7th_datehour': ['20220310', '13~19', 'mid'],
              # 'wish_8th_datehour': ['20220307', '08~17', 'last'],
              # 'wish_9th_datehour': ['20220307', '04~19', 'mid'],
              } # hour_option 'first, 'mid', 'last'


good_luck()


import uuid
import re

"macro part"
def pass_cal():

    # print(f"Mac-Address: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}")
    macaddress = ''.join(re.findall('..', '%012x' % uuid.getnode())).upper()
    macaddress_int = int(''.join([str(ord(s)) for s in macaddress]))
    pass_cal = macaddress_int % 790604
    return pass_cal
"users's tool"
def macaddress_ex():
    macaddress = ''.join(re.findall('..', '%012x' % uuid.getnode())).upper()

    return macaddress
"developer's IP"
def pass_key(macaddress):
    macaddress_int = int(''.join([str(ord(s)) for s in macaddress]))
    pass_key = macaddress_int % 790604
    return pass_key
pk = pass_key('BC5FF4395741')
print(pk)
"시나리온 developer가 제공하는 pass_key를 넣어서 pass_cal의 결과와 일치하면 실행"
if pass_key(macaddress_ex())  == pass_cal():
    print('True')
else:
    print('Falase')


# reserve_ipo(info_ipo, info_date, reserve_try_cnt=2, reserve_type='test', multi_date=False)

# info_ipo_ex,info_date_ex,key_pair = info_ipo_ex()

# reserve_ipo3(info_ipo_ex,info_date_ex, reserve_try_cnt  = 9,reserve_able_cnt = 3, reserve_type='test', multi_date = False)
# reserve_ipo3(info_ipo,info_date_test2(), reserve_try_cnt  = 9,reserve_able_cnt = 3, reserve_type='test', multi_date = False)
# reserve_rivera_macmini(info_rivera, info_date_test(), reserve_cnt=1, reserve_type='test', multi_date=False)

# reserve_rivera(info_rivera, info_date_test(), reserve_cnt=1, reserve_type='test', multi_date=False)

# Every day at 12am or 00:00 time bedtime() is called.
job1 = schedule.every().day.at("19:30").do(good_luck)
job2 = schedule.every().day.at("07:30").do(good_luck)
# str(random.randrange(9,14)).zfill(2)
job3 = schedule.every().day.at("16:15").do(lambda:  reserve_rivera_macmini(info_rivera,info_date_test(),reserve_try_cnt=1,reserve_type='test', multi_date = False) )
job4 = schedule.every().day.at("17:15").do(lambda: reserve_ipo3(info_ipo,info_date_test2(), reserve_try_cnt  = 9,reserve_able_cnt = 1, reserve_type='test', multi_date = False)  )

job_real1 = schedule.every().day.at("09:00").do(lambda:  reserve_ipo3(info_ipo,info_date_ipo, reserve_try_cnt  = 9,reserve_able_cnt = 1, reserve_type='real', multi_date = False) )

count = 0
while True:
    schedule.run_pending()
    time.sleep(1)
    count += 1

    if count >0 :
        schedule.cancel_job(job_real1)


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
#             timeTable_filterd = timeTable.loc[mask1, :]
#
#             timeTable_sorted = timeTable_filterd.sort_values('hour')
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