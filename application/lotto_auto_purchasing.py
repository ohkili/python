
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

from web_crawling.Set_chromedriver import driverAct
from web_crawling.Telegram_message import telegram_message
from util.pause import pause

def lotto_purchase():
    print('hello world')
    info_dict = {'url_homepage':'https://dhlottery.co.kr/common.do?method=main',
                 'url_loginpage' : 'https://dhlottery.co.kr/user.do?method=login&returnUrl=',
                 'url_lotto_game' : 'https://el.dhlottery.co.kr/game/TotalGame.jsp?LottoId=LO40',
                 'id':'ohkili',
                 'pw':'Lotto!1203',
                 }
    pause_time =1
    driver = driverAct(info_dict['url_homepage'])
    driver.set_window_size(1400, 1000)  # (가로, 세로)

    #로그인
    driver.get(info_dict['url_loginpage']) # 페이지 이동
    driver.find_element(By.XPATH, "//div[@id='article' and @class = 'contentsArticle']/div/div/form[@name='jform']/div[@class='box_login']/div[@class='inner']/fieldset/div[@class='form']")
    # 아이디 입력하는곳을 찾는다.
    userId = driver.find_element(By.ID, 'userId')
    userId.send_keys(info_dict['id'])  # 로그인 할 계정 id

    userPwd = driver.find_element(By.NAME, 'password')
    userPwd.send_keys(info_dict['pw'])  # 로그인 할 계정의 패스워드
    userPwd.send_keys(Keys.ENTER)

    pause(pause_time)
    #구매
    # driver.find_element(By.XPATH, "//div[@id='gnb']/ul/li[@class='gnb1']").click()

    # lotto game page
    driver.get(info_dict['url_lotto_game'])
    driver.switch_to.frame(driver.find_element(By.XPATH, "//div[@id='container']/iframe[@id='ifrm_tab']"))
    pause(pause_time)
    #구매 방법 혼합 선택
    driver.find_element(By.XPATH , "//div[@class='game-645-wrap']/div[@class='game-645-content']/div[@class='select-number']/div[@class='header']/ul[@id='tabWay2Buy']/li/a").click()
    # 선택 page
    number_table = "//div[@class='game-645-wrap']/div[@class='game-645-content']/div[@class='select-number']/div[@class='ways']/div[@id='divWay2Buy1']/div[@class='paper']/div[@id='checkNumGroup']"

    no_dic ={}
    for i in range(1,46):
        no_dic[i] = 'check645num' +str(i)


    # 로또 번호 선택 지정 번호만 사도록 하였음, 자동 또는 부분 자동은 개발하지 않았음
    no_list = [[3,5,7,8,12,23], [5,9,17,22,26,43], [2,6,10,20,35,45]]

    for s in no_list:
        for k in s:
            driver.find_element(By.XPATH ,number_table + "/label[@for=" +  "'" +  no_dic[k] + "']").click()
        # 확인 버튼
        driver.find_element(By.XPATH,
                            "//div[@class='game-645-wrap']/div[@class='game-645-content']/div[@class='select-number']/div[@class='ways']/div[@id='divWay2Buy1']/div[@class='amount']/input[@id='btnSelectNum']").click()

    pause(pause_time)
    #구매하기버튼 클릭
    driver.find_element(By.XPATH,"//div[@class='game-645-wrap']/div[@class='game-645-content']/div[@class='selected-games']/div[@class='footer']/input[@id='btnBuy']").click()
    pause(pause_time)
    # 구매 확인 버틑
    driver.find_element(By.XPATH, "//div[@class='layer-alert' and @id='popupLayerConfirm']/div[@class='box']/div[@class='btns']/input[@value='확인']").click()
    pause(pause_time)

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
    telegram_message(content=str(lotto_result), content_type='text', description='description')
    # lotto_log = pd.DataFrame()
    # lotto_log = pd.read_pickle('E:/work/lotto_log.pkl')
    pause(pause_time)
    try:

        lotto_log = pd.read_pickle('E:/work/lotto_log.pkl') # 개인 컴퓨터에 저장한 log path
        lotto_log = pd.concat([lotto_log,lotto_result])
        lotto_log.to_pickle('E:/work/lotto_log.pkl') # 개인 컴퓨터에 저장한 log path
        print('Log was written!')
        print(lotto_log)
        pause(pause_time)
    except:
        pass
    driver.find_element(By.XPATH, "//div[@id='popReceipt']/div[@class='btns']/input[@id='closeLayer'] ").click()

def Message(sentence = "Good Luck for Test"):
      print(sentence)
      print( time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

# Task scheduling
# After every 10mins geeks() is called.
# schedule.every(2/60).minutes.do(Message(sentence = "Good Luck for Test"))

# After every hour geeks() is called.
# schedule.every().hour.do(geeks)

# Every day at 12am or 00:00 time bedtime() is called.
# schedule.every().day.at("18:30").do(Message(sentence = "Good Luck for Test"))

# After every 5 to 10mins in between run work()
# schedule.every(5).to(10).minutes.do(work)

# Every monday good_luck() is called
# schedule.every().monday.do(good_luck)

# Every tuesday at 18:00 sudo_placement() is called
#schedule.every().sunday.at("18:30").do(lotto_purchase)

# Loop so that the scheduling task
# keeps on running all time.
if __name__ == '__main__':
    lotto_purchase()
    #
    # while True:
    #
    #     # Checks whether a scheduled task
    #     # is pending to run or not
    #     schedule.run_pending()
    #     time.sleep(1)
