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

# driver 초기화 하고 url 들어가는 함수, os가 윈도우인지, mac인지 구분하고 chrome driver가 저장된 위치를 명시하였으므로 개인 환경에 맞게 적절히 셋팅 필요
def driverAct(url, option ='win'):
    os = {'mac': 'mac',
          'win': 'windows'}

    os_option = os[option]
    if os_option == 'mac':
        executable_path = '/usr/local/bin/chromedriver'  # 크롬드라이버가 보안에 막혀서 크롬드라이버를 압축풀고 해당 폴더로 이동시켜주었다
    elif os_option == 'windows':
        # executable_path = "C:\\Users\ohkil\\PycharmProjects\\chromedriver_win32\\chromedriver.exe"  # 크롬드라이버가 보안에 막혀서 크롬드라이버를 압축풀고 해당 폴더로 이동시켜주었다
        executable_path = "C:/Users\ohkil/PycharmProjects/chromedriver_win32/chromedriver.exe"  # 크롬드라이버가 보안에 막혀서 크롬드라이버를 압축풀고 해당 폴더로 이동시켜주었다

    else:
        print('Check your OS type')
    driver = webdriver.Chrome(executable_path=executable_path)
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


t= 1
url = 'https://dhlottery.co.kr/common.do?method=main'
driver = driverAct(url,option='win')
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
# no_list = [[3,5,7,8,12,23], [17,26,9,43,5,22], [2,6,10,45,35,20]]
no_list = [[21,22,41,30,24,38]]

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
# lotto_log = pd.DataFrame()
# lotto_log = pd.read_pickle('E:/work/lotto_log.pkl')
lack(t)
lotto_log = pd.read_pickle('E:/work/lotto_log.pkl') # 개인 컴퓨터에 저장한 log path
lotto_log = pd.concat([lotto_log,lotto_result])
lotto_log.to_pickle('E:/work/lotto_log.pkl') # 개인 컴퓨터에 저장한 log path
print('Log was written!')
print(lotto_log)
lack(t)
driver.find_element(By.XPATH, "//div[@id='popReceipt']/div[@class='btns']/input[@id='closeLayer'] ").click()

