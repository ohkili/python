# 방식
# 1 화면 클릭 방식
# 2 html 입력 방식
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
import schedule
import time
import os
import json
import requests
import telegram
import chromedriver_autoinstaller

# REST_API_KEY and refresh_token is borrow
REST_API_KEY ='22644bd965c28d381ea875a9dde9e2d1'
refresh_token = '2hZcRLD01s1Rl0qEA0BhnenFH1om0rtTNimYSgo9cuoAAAF81jvBOA'

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

# driver 초기화 하고 url 들어가는 함수, os가 윈도우인지, mac인지 구분하고 chrome driver가 저장된 위치를 명시하였으므로 개인 환경에 맞게 적절히 셋팅 필요
# def driverAct(url, option ='macmini'):
#     os = {'macmini': 'macmini',
#           'macpro' : 'macpro',
#           'win': 'windows'}

#     os_option = os[option]
#     if os_option == 'macmini':
#         executable_path =  '/Users/gwon-yonghwan/PycharmProjects/chromedriver'
#         #'/Users/home/PycharmProjects/chromedriver'   # '/usr/local/bin/chromedriver'  # 크롬드라이버가 보안에 막혀서 크롬드라이버를 압축풀고 해당 폴더로 이동시켜주었다
#     elif os_option == 'macpro':
#         executable_path = '/Users/home/PycharmProjects/chromedriver'
#     elif os_option == 'windows':
#         # executable_path = "C:\\Users\ohkil\\PycharmProjects\\chromedriver_win32\\chromedriver.exe"  # 크롬드라이버가 보안에 막혀서 크롬드라이버를 압축풀고 해당 폴더로 이동시켜주었다
#         executable_path = "C:/Users\ohkil/PycharmProjects/chromedriver_win32/chromedriver.exe"  # 크롬드라이버가 보안에 막혀서 크롬드라이버를 압축풀고 해당 폴더로 이동시켜주었다

#     else:
#         print('Check your OS type')
#     driver = webdriver.Chrome(executable_path=executable_path)
#     driver.set_window_size(1400, 1000)  # (가로, 세로)음
#     driver.get(url)
#     return driver
def chromedriver_autorun():

    # chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  #크롬드라이버 버전 확인
    #
    # try:
    #     driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')
    # except:
    #     chromedriver_autoinstaller.install(True)
    #     driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')


    path = chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(path)

    driver.implicitly_wait(10)


    return driver
def driverAct(url):
    # os_ver = platform.system()
    # plaform_ver = platform.platform()
    #
    # if os_ver == 'Darwin' and plaform_ver == 'Darwin-19.6.0-x86_64-i386-64bit':
    #     executable_path = '/Users/gwon-yonghwan/Downloads/chromedriver'
    #     # '/Users/home/PycharmProjects/chromedriver'   # '/usr/local/bin/chromedriver'  # 크롬드라이버가 보안에 막혀서 크롬드라이버를 압축풀고 해당 폴더로 이동시켜주었다
    #     'driver activation for mac os'
    #     driver = webdriver.Chrome(executable_path=executable_path)
    # elif os_ver == 'Darwin' and plaform_ver == 'macOS-10.16-x86_64-i386-64bit':
    #     executable_path = '/Users/home/Downloads/chromedriver'
    #     'driver activation for mac os'
    #     driver = webdriver.Chrome(executable_path=executable_path)
    #
    # elif os_ver == 'Windows' and plaform_ver.find('Windows') >= 0 :
    #     # plaform_ver == 'Windows-10-10.0.19041-SP0'
    #     # executable_path = "C:\\Users\ohkil\\PycharmProjects\\chromedriver_win32\\chromedriver.exe"  # 크롬드라이버가 보안에 막혀서 크롬드라이버를 압축풀고 해당 폴더로 이동시켜주었다
    #     # executable_path = "C:/Users\ohkil/PycharmProjects/chromedriver_win32/chromedriver.exe"  # 크롬드라이버가 보안에 막혀서 크롬드라이버를 압축풀고 해당 폴더로 이동시켜주었다
    #     'driver activation for windows pc'
    #     driver = chromedriver_autorun()
    # else:
    #     print('Check your OS type')
    #     telegram_message('Check your chrome driver path or version.')
    driver = chromedriver_autorun()
    driver.set_window_size(1400, 1000)  # (가로, 세로)음
    driver.get(url)
    return driver

def lack(t):
    print('sleep {0} sec'.format(t))
    time.sleep(t)

def check_exists_by_element(by, name):
    try:
        driver.find_element(by, name)
    except NoSuchElementException:
        return False
    return True

 # lotto homepage : 'https://dhlottery.co.kr/common.do?method=main'

def lotto_purchase():
    print('hello world')
    t= 1
    url = 'https://dhlottery.co.kr/common.do?method=main'
    driver = driverAct(url)
    driver.set_window_size(1400, 1000)  # (가로, 세로)

    #로그인
    driver.get('https://dhlottery.co.kr/user.do?method=login&returnUrl=') # 페이지 이동
    driver.find_element(By.XPATH, "//div[@id='article' and @class = 'contentsArticle']/div/div/form[@name='jform']/div[@class='box_login']/div[@class='inner']/fieldset/div[@class='form']")
    # 아이디 입력하는곳을 찾는다.
    userId = driver.find_element(By.ID, 'userId')
    userId.send_keys('ohkili')  # 로그인 할 계정 id

    userPwd = driver.find_element(By.NAME, 'password')
    userPwd.send_keys('Lotto!1203')  # 로그인 할 계정의 패스워드
    userPwd.send_keys(Keys.ENTER)

    lack(t)
    #구매
    # driver.find_element(By.XPATH, "//div[@id='gnb']/ul/li[@class='gnb1']").click()

    # lotto page
    url_lotto = 'https://el.dhlottery.co.kr/game/TotalGame.jsp?LottoId=LO40'
    driver.get(url_lotto)
    driver.switch_to.frame(driver.find_element(By.XPATH, "//div[@id='container']/iframe[@id='ifrm_tab']"))
    lack(t)
    #구매 방법 혼합 선택
    driver.find_element(By.XPATH , "//div[@class='game-645-wrap']/div[@class='game-645-content']/div[@class='select-number']/div[@class='header']/ul[@id='tabWay2Buy']/li/a").click()
    # 선택 page
    number_table = "//div[@class='game-645-wrap']/div[@class='game-645-content']/div[@class='select-number']/div[@class='ways']/div[@id='divWay2Buy1']/div[@class='paper']/div[@id='checkNumGroup']"

    no_dic ={}
    for i in range(1,46):
        no_dic[i] = 'check645num' +str(i)


    # 로또 번호 선택 지정 번호만 사도록 하였음, 자동 또는 부분 자동은 개발하지 않았음
    no_list = [[3,5,7,8,12,23], [17,26,9,43,5,22], [2,6,10,45,35,20]]
    #
    # no_list = [[8,45,28,22,34,17]]

    for s in no_list:
        for k in s:
            driver.find_element(By.XPATH ,number_table + "/label[@for=" +  "'" +  no_dic[k] + "']").click()
        # 확인 버튼
        driver.find_element(By.XPATH,
                            "//div[@class='game-645-wrap']/div[@class='game-645-content']/div[@class='select-number']/div[@class='ways']/div[@id='divWay2Buy1']/div[@class='amount']/input[@id='btnSelectNum']").click()

    lack(t)
    #구매하기버튼 클릭
    driver.find_element(By.XPATH,"//div[@class='game-645-wrap']/div[@class='game-645-content']/div[@class='selected-games']/div[@class='footer']/input[@id='btnBuy']").click()
    lack(t)
    # 구매 확인 버틑
    driver.find_element(By.XPATH, "//div[@class='layer-alert' and @id='popupLayerConfirm']/div[@class='box']/div[@class='btns']/input[@value='확인']").click()
    lack(t)

    driver.window_handles
    # 구매 내역 확인 창
    lotto_type = driver.find_element(By.XPATH, "//div[@id='popReceipt']/div[@class='date-info']/h3/span ").text
    lotto_round = driver.find_element(By.XPATH, "//div[@id='popReceipt']/div[@class='date-info']/h3/strong[@id='buyRound']").text
    lotto_issue = driver.find_element(By.XPATH, "//div[@id='popReceipt']/div[@class='date-info']/ul/li/span[@id='issueDay']").text
    lotto_draw = driver.find_element(By.XPATH, "//div[@id='popReceipt']/div[@class='date-info']/ul/li/span[@id='drawDate']").text
    lotto_paylimit = driver.find_element(By.XPATH, "//div[@id='popReceipt']/div[@class='date-info']/ul/li/span[@id='payLimitDate']").text
    lotto_purchaseNo = driver.find_element(By.XPATH, "//div[@id='popReceipt']/div[@class='selected']/ul[@id='reportRow']").text
    lotto_purchaseNo = lotto_purchaseNo.replace("\n","|")

    lotto_result = pd.DataFrame([[lotto_type,lotto_round,lotto_issue,lotto_draw,lotto_paylimit,lotto_purchaseNo]],
                                columns =['lotto_type','lotto_round','lotto_issue','lotto_draw','lotto_paylimit','lotto_purchaseNo'])
    # access_token = access_token_mkr(REST_API_KEY, refresh_token)
    # kakao_message(lotto_result, access_token)
    l= str(lotto_result)
    telegram_message(content=l, content_type='text', description='description')

    # lotto_log = pd.DataFrame()
    # lotto_log = pd.read_pickle('/Users/gwon-yonghwan/pythonProject/lotto_log.pkl')
    lack(t)
    # '/Users/gwon-yonghwan/pythonProject/lotto_log.pkl'
    lotto_log = pd.read_pickle('/Users/gwon-yonghwan/pythonProject/lotto_log.pkl') # 개인 컴퓨터에 저장한 log path
    lotto_log = pd.concat([lotto_log,lotto_result])
    lotto_log.to_pickle('/Users/gwon-yonghwan/pythonProject/lotto_log.pkl') # 개인 컴퓨터에 저장한 log path
    print('Log was written!')
    print(lotto_log)
    lack(t)
    driver.find_element(By.XPATH, "//div[@id='popReceipt']/div[@class='btns']/input[@id='closeLayer'] ").click()
    driver.quit()
    return lotto_result
# Functions setup

def good_luck():
      print("Good Luck for Test")
      print( time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
      # access_token = access_token_mkr(REST_API_KEY,refresh_token)
      # kakao_message('message test from macmini with lotto'+ str( time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))),access_token)
      telegram_message(content='message test from macmini with lotto'+ str( time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))), content_type='text', description='description')


def work():
      print("Study and work hard")
      print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

good_luck()
# Task scheduling
# After every 10 mins geeks() is called.
# schedule.every(10/60).minutes.do(good_luck)

# After every hour geeks() is called.
# schedule.every().hour.do(geeks)

# Every day at 12am or 00:00 time bedtime() is called.
schedule.every().day.at("18:30").do(good_luck)
schedule.every().day.at("06:30").do(good_luck)

# After every 5 to 10mins in between run work()
# schedule.every(5).to(10).minutes.do(work)

# Every monday good_luck() is called
# schedule.every().monday.do(good_luck)

# Every tuesday at 18:00 sudo_placement() is called
schedule.every().sunday.at("14:30").do(lotto_purchase)

# Loop so that the scheduling task
# keeps on running all time.
while True:

	# Checks whether a scheduled task
	# is pending to run or not
	schedule.run_pending()

	time.sleep(1)
