
import chromedriver_autoinstaller # for selenium
import pandas as pd               # data processing
import requests                   # telegram connecting
from selenium import webdriver    # web driver
from selenium.webdriver.common.by import By     # web element searching
from selenium.webdriver.common.keys import Keys # enter
import schedule  # scheduler
import time      # scheduler
import telegram  # message
import platform  # checking os type
import uuid      # checking mac address
import re        # checking mac address
import os        # management for log and result file

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

    elif os_ver == 'Windows' and plaform_ver.find('Windows') >= 0 :
        # plaform_ver == 'Windows-10-10.0.19041-SP0'
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

def good_luc_from_maestro():
    print("Good Luck for Test from maestro")
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    content_new =  'message test from reservattion_maestro ' + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    telegram_message(content = content_new, content_type='text', description= 'etc' )

def info_ipo_ex(folder_name,id_no =1):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        pass

    try:
        columnNames = ['Order', 'Date', 'Front_Time', 'End_Time', 'Filter']
        columnNames1 = ['ID','Password']
        columnNames2 = ['Gen_key', 'Pass_key','run_mode']

        "part of info of ipo cc url"
        """ info_ipo = {'url': 'http://ipo-cc.co.kr/cmm/main/mainPage.do',
                    'loginPage': 'https://ipocc.com/uat/uia/egovLoginUsr.do',
                    'id': '',
                    'pw': ''
                    } """
        info_ipo = {'url': 'http://m.ipo-cc.co.kr/cmm/main/mainPage.do',
                    'loginPage': 'http://m.ipo-cc.co.kr/uat/uia/egovLoginUsr.do',
                    'id': '',
                    'pw': '',
                    'filepath':''
                    }


        timeTable = pd.read_excel(os.path.join(folder_name,'ipo_reserve_order_rev1.xlsx'),sheet_name='timeTable'+str(id_no))
        idpw = pd.read_excel(os.path.join(folder_name,'ipo_reserve_order_rev1.xlsx'), sheet_name='cc'+str(id_no))
        genpass = pd.read_excel(os.path.join(folder_name,'ipo_reserve_order_rev1.xlsx'), sheet_name='macro')

        "part of info reserve order date"
        timeTable.columns = columnNames
        timeTable = timeTable.astype('str')
        timeTable['Front_Time'] = timeTable['Front_Time'].apply(lambda x : '0' + x if len(x) == 1 else x)
        timeTable['End_Time'] = timeTable['End_Time'].apply(lambda x : '0' + x if len(x) == 1 else x)
        timeTable['Filter'] = timeTable['Filter'].apply(lambda x: x.lower())
        timeTable['Filter'] = timeTable['Filter'].apply(lambda x: 'first' if x[0] == 'f' else 'mid' if x[0] =='m' else 'last')
        timeTable.reset_index(drop=True, inplace=True)

        info_date2 ={}
        for i in range(len(timeTable)):
            info_date2[timeTable['Order'].iloc[i]] = [timeTable['Date'].iloc[i], timeTable['Front_Time'].iloc[i] +'~' + timeTable['End_Time'].iloc[i], timeTable['Filter'].iloc[i]]

        "part of info login ID & Password"
        idpw.columns = columnNames1
        idpw.reset_index(drop=True, inplace=True)

        info_ipo['id'] = idpw['ID'].iloc[0]
        info_ipo['pw'] = idpw['Password'].iloc[0]
        info_ipo['filepath'] = folder_name

        "part of info macro gen & pass key"
        genpass.columns = columnNames2
        genpass.reset_index(drop=True, inplace=True)

        key_pair = {}

        key_pair['Gen_key'] = genpass['Gen_key'].iloc[0]
        key_pair['Pass_key'] = genpass['Pass_key'].iloc[0]

        run_mode ={}
        mode_temp = genpass['run_mode'].iloc[0].lower()[0]
        if mode_temp == 'r':
            run_mode['mode'] = 'real'
        elif mode_temp == 't':
            run_mode['mode'] = 'test'
        else:
            run_mode['mode'] = 'real'

    except:
        print('Check your file, file name is ipo_reserve_order.xlsx')

    return  info_ipo, info_date2,key_pair,run_mode
def reserve_ipo5_mobile(loginfo,info_date2, reserve_try_cnt  = 9,reserve_able_cnt = 3, reserve_type='test', reserve_open_time = '09:00', multi_date = False):

    def homefunc(driver):
        t = 0
        while (t < 3):
            driver.implicitly_wait(1)
            driver.find_element(By.XPATH, "/html/body/div[@id ='wrap']/div[@id='header']"
                                          "/header/h1/a/img[@alt='IPO Country Club']"
                                ).click()
            t += 1
        return driver
    def loginfunc(driver,logintrycnt = 10):
        homefunc(driver)
        "ID Pasword 입력하여 login"
        "check login status"
        login_btn = driver.find_element(By.XPATH,
                                           "/html/body/div[@id='wrap']/div[@id='header']/header/div[@class='btn-login']/a").text
        login_trycnt = 0
        while login_btn == 'Login' and login_trycnt <logintrycnt:
             try:
                driver.get(loginpage)
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

             "check login status"
             login_btn = driver.find_element(By.XPATH,"/html/body/div[@id='wrap']/div[@id='header']/header/div[@class='btn-login']/a" ).text
             login_trycnt +=1

             if login_btn == 'Logout':
                 break

        print(login_btn,login_trycnt)

        return driver

    "미리 로그인을 하고 있다가 9시가 되면 예약 시작"
    # inforamtion of login date initial variable.
    "로그인에 필요한 정보"
    url       = loginfo['url']
    loginpage = loginfo['loginPage']
    loginID   = str(loginfo['id'])
    loginPW   = str(loginfo['pw'])
    info_path  = loginfo['filepath']

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
        # reserve_try_cnt = 1
        # reserve_able_cnt =1
        pass
    else:
        reserve_try_cnt =0
        telegram_message(content= 'ipo_cc : ' + error_msg['reserve_type'], content_type='text', description='description')

    "log file 저장할 폴더 및 파일 생성"
    if not os.path.exists(info_path):
        os.makedirs(info_path)
    else:
        pass

    reservation_log_path = info_path + "/result_reservation_" + loginID + ".txt"
    if os.path.exists(reservation_log_path):
        os.remove(reservation_log_path)
    else:
        pass
    result_not_able_log_path = info_path + "/result_not_able_" + loginID + ".txt"
    if os.path.exists(result_not_able_log_path):
        os.remove(result_not_able_log_path)
    else:
        pass



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


    loginfunc(driver)

    "시간 대기"
    c = 0
    time_present =0
    rot = int(reserve_open_time.replace(':','')+'00')
    while time_present < rot and reserve_type =='real':
        time_present = int(time.strftime('%H%M%S'))

        print(time_present)
        print(time.strftime('%H:%M:%S'))
        if time.strftime('%M')[1:] =='7':
            loginfunc(driver)
        c += 1
        time.sleep(0.5)

    if reserve_type =='real':
        telegram_message('time over 09:00:00 at' + time.strftime('%H:%M:%S'))
    else:
        pass


    driver.refresh()

    # 리베라에 해당하는 사례임
    # log in putton userPwd에 password를 엔터를 치면 되는데, 아래처럼 로그인 버튼을 누를수도 있다
    # loginbtn = driver.find_element(By.XPATH, "//form[@id='loginForm']/div[@class='login_btn']")
    # loginbtn.click()
    # /html/body/div/div[1]/div[3]/div/ul/li[1]/a
    # 통합 예약/실시간예약
    # reservation = driver.find_element(By.XPATH,"/html/body/div/div[2]/div/div[2]/div[1]/ul/li[1]/div/ul/li[1]/a")  # /html/body/div/div[2]/div/div[2]/div[1]/ul/li[1]/div/ul/li[1]/a

    # 3. reserveation page open


    while(reserve_need_cnt > 0 and reserve_try_cnt > 0 and reserve_able_cnt > 0 ):
        homefunc(driver)
        loginfunc(driver)
        "예약 화면 open"
        cnt = 0
        reservation_status = ''
        while reservation_status != '온라인예약' and cnt < 10:

            reservation_open = driver.find_element(By.XPATH, "/html/body/div[@id ='wrap']/article[@class='main_article']"
                                                             "/section[@class='main_viaul']/div[@class='main_btn']"
                                                             "/ul/li/a")
            driver.execute_script("arguments[0].click();", reservation_open)   # 예약 화면 오픈

            reservation_status = driver.find_element(By.XPATH, "/html/body/div[@id ='wrap']/article[@class='sub_article']/h2").text

            cnt +=1

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

        driver.find_element(By.ID, "wrap")

        # 달력 부분 활성화
        driver.find_element(By.XPATH, "//article[@class='sub_article']/section[@class='contents']/div[@class='txtcont']/div[@class='join_form']")
        driver.find_element(By.XPATH,"//div[@class = 'mt10 mb40']")

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
        else:
            pass


        for kd in list(info_date_temp.keys()):

            loginfunc(driver)
            reservation_open = driver.find_element(By.XPATH,
                                                   "/html/body/div[@id ='wrap']/article[@class='main_article']"
                                                   "/section[@class='main_viaul']/div[@class='main_btn']"
                                                   "/ul/li/a")
            driver.execute_script("arguments[0].click();", reservation_open)  # 예약 화면 오픈

            reservable_time_table = pd.DataFrame()
            "예약 완료한 일시를 저장하기 위함, 대기 예약이 가능하므로 status는 유지함"
            # kd = list(info_date_temp.keys())[1]
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

                            driver.find_element(By.XPATH,"//div[@class = 'mt10 mb40 join_form']")

                            # course 선택
                            course_dict = {'out': "//div[@class = 'txtcont mb40']/table[@id = 'out_table']/tbody",
                                           'in' :  "//div[@class = 'mt10 mb40 join_form']/div[@class = 'txtcont mb40']/table[@id = 'in_table']/tbody"}

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
                                    # i = 0
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

                                    t =0
                                    while(t<3):

                                        driver.implicitly_wait(1)
                                        driver.refresh()
                                        t +=1


                                    homefunc(driver)



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
# info_path = 'C:/ipocc_info'
# loginfo, info_date2, key_pair, run_mode = info_ipo_ex(info_path, id_no=1)
reserve_try_cnt  = 9
reserve_able_cnt = 3
reserve_type='test'


info_maestro = {'url'      : 'https://www.maestrocc.co.kr/index.asp',
            'loginPage': 'https://www.maestrocc.co.kr/login/login.asp',
             'id'      : 'ohkili',
             'pw'      : 'mae!1203',
             'filepath':  ''
               }
loginfo = info_maestro
info_date2 = {'wish_1st_datehour': ['20220328', '05~18','mid'],
              'wish_2nd_datehour': ['20220327', '08~09', 'mid'],
              'wish_3rd_datehour': ['20220326', '07~08', 'mid'],
              'wish_4th_datehour': ['20220325', '10~19', 'mid'],
              'wish_5th_datehour': ['20220324', '10~19', 'mid'],
              'wish_6th_datehour': ['20220323', '11~19', 'mid'],
              'wish_7th_datehour': ['20220322', '13~19', 'mid'],
              'wish_8th_datehour': ['20220321', '08~17', 'last'],
              'wish_9th_datehour': ['20220320', '04~19', 'mid'],
           }

def reserve_maestro(loginfo,info_date2, reserve_try_cnt  = 9,reserve_able_cnt = 3, reserve_type='test', reserve_open_time = '09:00', multi_date = False):

    def homefunc(driver):
        t = 0
        while (t < 3):
            driver.implicitly_wait(1)
            driver.find_element(By.XPATH, "/html/body/div[@id ='wrap']/div[@id='header']"
                                          "/div[@class='head']/h1/a/img[@alt='MAESTRO']"
                                ).click()
            t += 1
        return driver
    def loginfunc(driver,logintrycnt = 10):
        homefunc(driver)
        "ID Pasword 입력하여 login"
        "check login status"
        login_btn = driver.find_element(By.XPATH,
                                           "/html/body/div[@id='wrap']/div[@id='header']/header/div[@class='btn-login']/a").text
        login_trycnt = 0
        while login_btn == 'Login' and login_trycnt <logintrycnt:
             try:
                driver.get(loginpage)
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

             "check login status"
             login_btn = driver.find_element(By.XPATH,"/html/body/div[@id='wrap']/div[@id='header']/header/div[@class='btn-login']/a" ).text
             login_trycnt +=1

             if login_btn == 'Logout':
                 break

        print(login_btn,login_trycnt)

        return driver

    "미리 로그인을 하고 있다가 9시가 되면 예약 시작"
    # inforamtion of login date initial variable.
    "로그인에 필요한 정보"
    url       = loginfo['url']
    loginpage = loginfo['loginPage']
    loginID   = str(loginfo['id'])
    loginPW   = str(loginfo['pw'])
    info_path  = loginfo['filepath']

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
    reserve_success_cnt = 0
    reserve_need_cnt    = len(info_date2)


    if reserve_type == 'real':
        pass
    elif reserve_type == 'test':
        # reserve_try_cnt = 1
        # reserve_able_cnt =1
        pass
    else:
        reserve_try_cnt =0
        telegram_message(content= 'ipo_cc : ' + error_msg['reserve_type'], content_type='text', description='description')

    # "log file 저장할 폴더 및 파일 생성"
    # if not os.path.exists(info_path):
    #     os.makedirs(info_path)
    # else:
    #     pass
    #
    # reservation_log_path = info_path + "/result_reservation_" + loginID + ".txt"
    # if os.path.exists(reservation_log_path):
    #     os.remove(reservation_log_path)
    # else:
    #     pass
    # result_not_able_log_path = info_path + "/result_not_able_" + loginID + ".txt"
    # if os.path.exists(result_not_able_log_path):
    #     os.remove(result_not_able_log_path)
    # else:
    #     pass
    #


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
        userId = driver.find_element(By.ID, 'login_id')
        userId.send_keys(loginID)  # 로그인 할 계정 id

        # password
        userPwd = driver.find_element(By.ID, 'login_pw')
        userPwd.send_keys(loginPW)
        userPwd.send_keys(Keys.ENTER)
    except:
        telegram_message(content='ipo_cc : ' + error_msg['login_fail'], content_type='text',
                         description='description')
    # pop up을 없애기 위해 불필요 명령을 내림
    driver.find_elements().text

    loginfunc(driver)

    "시간 대기"
    c = 0
    time_present =0
    rot = int(reserve_open_time.replace(':','')+'00')
    while time_present < rot and reserve_type =='real':
        time_present = int(time.strftime('%H%M%S'))

        print(time_present)
        print(time.strftime('%H:%M:%S'))
        if time.strftime('%M')[1:] =='7':
            loginfunc(driver)
        c += 1
        time.sleep(0.5)

    if reserve_type =='real':
        telegram_message('time over 09:00:00 at' + time.strftime('%H:%M:%S'))
    else:
        pass


    driver.refresh()

    # 리베라에 해당하는 사례임
    # log in putton userPwd에 password를 엔터를 치면 되는데, 아래처럼 로그인 버튼을 누를수도 있다
    # loginbtn = driver.find_element(By.XPATH, "//form[@id='loginForm']/div[@class='login_btn']")
    # loginbtn.click()
    # /html/body/div/div[1]/div[3]/div/ul/li[1]/a
    # 통합 예약/실시간예약
    # reservation = driver.find_element(By.XPATH,"/html/body/div/div[2]/div/div[2]/div[1]/ul/li[1]/div/ul/li[1]/a")  # /html/body/div/div[2]/div/div[2]/div[1]/ul/li[1]/div/ul/li[1]/a

    # 3. reserveation page open


    while(reserve_need_cnt > 0 and reserve_try_cnt > 0 and reserve_able_cnt > 0 ):
        homefunc(driver)
        loginfunc(driver)
        "예약 화면 open"
        cnt = 0
        reservation_status = ''
        while reservation_status != 'RESERVATION' and cnt < 10:

            # reservation_open = driver.find_element(By.XPATH, "/html/body/div[@id ='wrap']/div[@id='header']"
            #                                                  "/div[@class='gnb']/ul/li[@id='gnb_reservation']"
            #                                                  "/ul[@class='dep2']/li[@id='gnb2_reservation_live']/a"
            #                                                  ) #"/ul[@class='dep2']/li[@id='gnb2_reservation_live']/a"
            # driver.execute_script("arguments[0].click();", reservation_open)   # 예약 화면 오픈
            driver.get('https://www.maestrocc.co.kr/pagesite/reservation/live.asp')
            reservation_status = driver.find_element(By.XPATH, "/html/body/div[@id ='wrap']/div[@id='body']/div[@class='content_sub']"
                                                               "/div[@class='content_sub_in']/div[@class='lnb']/h2/span").text

            cnt +=1

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
        fisrt_month3 = driver.find_element(By.XPATH,
                                     "//div[@id='cm_calendar_small_01']/div[@id='calendar_view_ajax_1']"
                                     "/div[@class='cm_calender_top']/strong").text

        second_month5 = driver.find_element(By.XPATH,
                                     "//div[@id='cm_calendar_small_02']/div[@id='calendar_view_ajax_2']"
                                     "/div[@class='cm_calender_top']/strong").text


        "/html/body/div[@id='wrap']/div[@id='body']/div[@class='content_sub']/div[@class='content_sub_in']"
        "/div[@class='content']/div[@class='sub_top']/div[@id='content_body']/div[@id='cm_homepage']/div[@id='cm_reservation']"
        "//div[@id='cm_reservation_left']/div[@class='cm_calender_area_in']"

        "timeform 아래에 input 속성이 날짜별로 있어 list함"
        "worked at 220312 17:15"
        date_temp_1st = driver.find_elements(By.XPATH,
                                     "//div[@id='cm_calendar_small_01']/div[@id='calendar_view_ajax_1']"
                                     "/table[@class='cm_calender_tbl']/tbody/tr")
        date_temp_1st_dep1 = date_temp_1st[0].find_elements(By.XPATH,"td")
        date_temp_1st_dep1[33].text
        for i in range(len(date_temp_1st_dep1)):
            print(i, date_temp_1st_dep1[i].text)
        "worked at 220312 18:49"
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

        driver.find_element(By.ID, "wrap")

        # 달력 부분 활성화
        driver.find_element(By.XPATH, "//article[@class='sub_article']/section[@class='contents']/div[@class='txtcont']/div[@class='join_form']")
        driver.find_element(By.XPATH,"//div[@class = 'mt10 mb40']")

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
        else:
            pass


        for kd in list(info_date_temp.keys()):

            loginfunc(driver)
            reservation_open = driver.find_element(By.XPATH,
                                                   "/html/body/div[@id ='wrap']/article[@class='main_article']"
                                                   "/section[@class='main_viaul']/div[@class='main_btn']"
                                                   "/ul/li/a")
            driver.execute_script("arguments[0].click();", reservation_open)  # 예약 화면 오픈

            reservable_time_table = pd.DataFrame()
            "예약 완료한 일시를 저장하기 위함, 대기 예약이 가능하므로 status는 유지함"
            # kd = list(info_date_temp.keys())[1]
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

                            driver.find_element(By.XPATH,"//div[@class = 'mt10 mb40 join_form']")

                            # course 선택
                            course_dict = {'out': "//div[@class = 'txtcont mb40']/table[@id = 'out_table']/tbody",
                                           'in' :  "//div[@class = 'mt10 mb40 join_form']/div[@class = 'txtcont mb40']/table[@id = 'in_table']/tbody"}

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
                                    # i = 0
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

                                    t =0
                                    while(t<3):

                                        driver.implicitly_wait(1)
                                        driver.refresh()
                                        t +=1


                                    homefunc(driver)



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
def info_date_test_afer14days():

    #  wish_date 자동 생성
    info_date_test2 ={}
    tm = time.time()
    for t in range(30):
        d = tm + (t+14) * 86400
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

error_msg = {'login_url_aborted    ':'Check your login url',
             'login_fail'           :'Check your login id or password',
             'reserve_type'         :'Check your resever type or typo',
             'chrome_dirver_version': 'Check your chrome driver version'
             }

info_ipo = {'url'      : 'http://ipo-cc.co.kr/cmm/main/mainPage.do',
            'loginPage': 'https://ipocc.com/uat/uia/egovLoginUsr.do',
             'id'      : '',
             'pw'      : ''
               }
info_maestro = {'url'      : 'https://www.maestrocc.co.kr/index.asp',
            'loginPage': 'https://www.maestrocc.co.kr/login/login.asp',
             'id'      : 'ohkili',
             'pw'      : 'Mae!1203'
               }


# 날짜 고르기
info_date2 = {'wish_1st_datehour': ['20220315', '05~18','mid'],
              'wish_2nd_datehour': ['20220228', '08~09', 'mid'],
              'wish_3rd_datehour': ['20220302', '07~08', 'mid'],
              'wish_4th_datehour': ['20220303', '10~19', 'mid'],
              'wish_5th_datehour': ['20220306', '10~19', 'mid'],
              'wish_6th_datehour': ['20220309', '11~19', 'mid'],
              'wish_7th_datehour': ['20220310', '13~19', 'mid'],
              'wish_8th_datehour': ['20220307', '08~17', 'last'],
              'wish_9th_datehour': ['20220307', '04~19', 'mid'],
           }                                 # hour_option 'first, 'mid', 'last'

good_luc_from_maestro()                                # telegram conneting check one time at program run


#===================================================================
"option"
info_path = 'C:/ipocc_info'
id_cnt = 2
reserve_time = "09:00"
# run_mode = 'test' #'real

#===================================================================


if id_cnt == 2:

    info_ipo_ex1,info_date_ex1, key_pair ,run_mode = info_ipo_ex(info_path, id_no = 1) # login info, reserve date, running key for macro from ipo_reserve_order.xlsx
    info_ipo_ex2,info_date_ex2, key_pair ,run_mode = info_ipo_ex(info_path, id_no = 2) # login info, reserve date, running key for macro from ipo_reserve_order.xlsx
else:
    info_ipo_ex1, info_date_ex1, key_pair,run_mode  = info_ipo_ex(info_path,
                                                        id_no=1)  # login info, reserve date, running key for macro from ipo_reserve_order.xlsx


"미리 실행하여 로그인 상태로 대기하다가 예약시간이 열리면 예약 화면 갱신후 예약 실행"

#
# job123 = schedule.every().day.at("23:22").do(lambda: reserve_ipo5_mobile(info_ipo_ex1,info_date_ex1, reserve_try_cnt  = 9,reserve_able_cnt = 3, reserve_type='test', reserve_open_time = reserve_time, multi_date = False))



if run_mode['mode'] == 'test':
    # try:
    #
    #    # reserve_ipo3(info_ipo_ex1, info_date_ex1, reserve_try_cnt  = 9,reserve_able_cnt = 3, reserve_type='test', multi_date = False)
    #     reserve_ipo4_mobile(info_ipo_ex1, info_date_ex1, reserve_try_cnt=9, reserve_able_cnt=3, reserve_type='test',
    #                         multi_date=False)
    # except:
    #     pass

    try:
        reserve_ipo5_mobile(info_ipo_ex1, info_date_ex1, reserve_try_cnt=9, reserve_able_cnt=2, reserve_type= run_mode['mode'] ,
                            multi_date=False)
        reserve_ipo5_mobile(info_ipo_ex2, info_date_ex2, reserve_try_cnt=9, reserve_able_cnt=2, reserve_type=run_mode['mode'] , multi_date=False)
    except:
        pass
    " test part"
    job2 = schedule.every().day.at("08:00").do(good_luc_from_maestro)
    job3 = schedule.every().day.at("09:00").do(lambda: reserve_ipo5_mobile(info_ipo_ex1,info_date_test_afer14days(), reserve_try_cnt  = 9,reserve_able_cnt = 2, reserve_type=run_mode['mode'] , multi_date = False)  )

elif run_mode['mode'] == 'real':

    "real part"
    good_luc_from_maestro()

    try:
        reserve_ipo5_mobile(info_ipo_ex1, info_date_ex1, reserve_try_cnt=9, reserve_able_cnt=3, reserve_type= 'test' ,reserve_open_time = reserve_time, multi_date=False)
        reserve_ipo5_mobile(info_ipo_ex2, info_date_ex2, reserve_try_cnt=9, reserve_able_cnt=3, reserve_type= 'test' ,reserve_open_time = reserve_time, multi_date=False)
    except:
        pass

    job3 = schedule.every().day.at("08:30").do(good_luc_from_maestro)

    try:
        job_real1 = schedule.every().day.at("08:40").do(lambda:  reserve_ipo5_mobile(info_ipo_ex1,info_date_ex1, reserve_try_cnt  = 9,reserve_able_cnt = 2, reserve_type=run_mode['mode'] , reserve_open_time = reserve_time,multi_date = False) )
    except:
        pass
    try:
        job_real2 = schedule.every().day.at("08:40").do(lambda: reserve_ipo5_mobile(info_ipo_ex2, info_date_ex2, reserve_try_cnt=9, reserve_able_cnt=2, reserve_type=run_mode['mode'] ,reserve_open_time = reserve_time, multi_date=False))
    except:
        pass

else:
    pass

count = 0
while True:
    schedule.run_pending()
    time.sleep(1)
    count += 1

    if run_mode == 'real':
         if count >0 :
              try:
                  print('try1')
                  schedule.cancel_job(job_real1)
              except:
                  pass
              try:
                  print('try2')
                  schedule.cancel_job(job_real2)
              except:
                  pass
         else:
            pass
    else:
        pass
else:
    print('Please, check your Gen_key or Pass_key')
    telegram_message('Please, check your Gen_key or Pass_key')

