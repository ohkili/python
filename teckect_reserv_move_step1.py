
# 방식
# 1 화면 클릭 방식
# 2 html 입력 방식
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup
from selenium.webdriver.common.alert import Alert
os = {'mac':'mac',
      'win':'windows'}

os_option = os['win']
if os_option == 'mac':
    executable_path = '/usr/local/bin/chromedriver' # 크롬드라이버가 보안에 막혀서 크롬드라이버를 압축풀고 해당 폴더로 이동시켜주었다
elif os_option == 'windows':
    # executable_path = "C:\\Users\ohkil\\PycharmProjects\\chromedriver_win32\\chromedriver.exe"  # 크롬드라이버가 보안에 막혀서 크롬드라이버를 압축풀고 해당 폴더로 이동시켜주었다
    executable_path = "C:/Users\ohkil/PycharmProjects/chromedriver_win32/chromedriver.exe"  # 크롬드라이버가 보안에 막혀서 크롬드라이버를 압축풀고 해당 폴더로 이동시켜주었다

driver = webdriver.Chrome(executable_path = executable_path)
# driver.close()
# 사이즈조절
driver.set_window_size(1400, 1000)  # (가로, 세로)음
driver.get('https://ticket.interpark.com/Gate/TPLogin.asp') # 페이지 이동

# driver.close()
# 로그인을 위해 로그인 박스가 있는 위치를 찾는다, 아래 예문은 element를 찾은 후 switch_to.frame 메소드를 사용하였다.
# 이유는 iframe 형태로 구성되어 있으면 find_element로 하부 내용을 가져 올수 없다. 그래서 switch_to.frame을 사용하여야 element에 접근이 가능하다.
driver.switch_to.frame(driver.find_element(By.XPATH, "//div[@class='leftLoginBox']/iframe[@title='login']"))
# 아이디 입력하는곳을 찾는다.
userId = driver.find_element(By.ID, 'userId')
userId.send_keys('ohkili79')  # 로그인 할 계정 id

userPwd = driver.find_element(By.ID, 'userPwd')
userPwd.send_keys('Int!1203')  # 로그인 할 계정의 패스워드
userPwd.send_keys(Keys.ENTER)
goodsCode = 21004791
# 예매할 상품코드 가져오
driver.get('http://ticket.interpark.com/Ticket/Goods/GoodsInfo.asp?GoodsCode=' + str(goodsCode))

# 예매안내 팝업 뜸 코로나 어쩌구 저쩌, 팝업 제거 안되면 예매하기 클릭 안됨
driver.find_element(By.XPATH, "//div[@class='popupWrap']/div[@class='popupFooter']/button[@class='popupCloseBtn is-bottomBtn']").click()


# 현재 메뉴 상태가 어떤 상태인지 확인이 필요함
# 이전 예매하던 이력이 있으면 1. 관람일/회차 선택이 아닌 2. 좌석 선택으로 넘어간 경우가 있어 이 부분을 체크할 필요가 있음
# 체크후 메뉴가 맞지 않으면 원하는 곳으로 옮겨 줘야 함

# 1 관람일 회차 선택 //div[@class='contL']/iframe[@id='ifrmBookStep] , //div[@class='contFrame frameBg6']
# 1 다음단계 //div[@class='contL']/iframe[@id='ifrmBookStep] , //div[@class='contR']/div[@class='buy_info']/p[@id="LargeNextBtn"]/a

# 2 좌석선택 tag 정보 //div[@id='divBookSeat']/iframe[@id='ifrmSeat']  , //div[@class='seatL']/iframe[@id='ifrmSeatDetail']
# 2 이전단계  //div[@id="divBookSeat"]/iframe[@id="ifrmSeat"] , //div[@class='seatR']/div[@class='inner']/div[@class='btnWrap']/p[@class='fl_l']/a

# 3 가격/할인 선택 tag정보  //div[@class='contL']/iframe[@id=ifrmBookStep], //div[@class='contFrame frameBg2'
# 3 이전단계  "//div[@class ='contR']/div[@class ='buy_info']/p[@id='SmallNextBtn']/a[@id='SmallPrevBtnLink']/img[@id='SmallPrevBtnImage']"
# 3 다음단계  "//div[@class ='contR']/div[@class ='buy_info']/p[@id='SmallNextBtn']/a[@id='SmallNextBtnLink']/img[@id='SmallNextBtnImage']"

#4 배송선택/주문자확인 tag 정보 //div[@class='contL']/iframe[@id='ifrmBookStep] ,//div[@id='formDelivery']
#4 이전단계  //p[@id="SmallNextBtn"]/a[@id="SmallPrevBtnLink"]
#4 다음단계 //p[@id="SmallNextBtn"]/a[@id="SmallNextBtnLink"]

#5 결제하기 tag 정보 //div[@class='contL']/iframe[@id='ifrmBookStep]  ,//div[@class='contFrame frameBg3']
#5 이전단계 //p[@id="SmallNextBtn"]/a[@id="SmallPrevBtnLink"]
#5 이후단계 //p[@id="SmallNextBtn"]/a[@id="SmallNextBtnLink"]
# menu_dic 'step info': 'main address','sub address', 'prev button', 'next button'
menu_dic = { 'step_1':["//div[@class='contL']/iframe[@id='ifrmBookStep']" ,"//div[@class='contFrame frameBg6']"],
             'step_2':["//div[@id='divBookSeat']/iframe[@id='ifrmSeat']"  ,
                       "//div[@class='seatL']/iframe[@id='ifrmSeatDetail']" ,
                      "//div[@class ='seatR']/div[@class='inner']/div[@class='btnWrap']/p[@class ='fl_l']/a"],
             'step_3':["//div[@class='contL']/iframe[@id='ifrmBookStep']",
                       "//div[@class='contFrame frameBg2']",
                       "//div[@class ='contR']/div[@class ='buy_info']/p[@id='SmallNextBtn']/a[@id='SmallPrevBtnLink']/img[@id='SmallPrevBtnImage']",
                       "//div[@class ='contR']/div[@class ='buy_info']/p[@id='SmallNextBtn']/a[@id='SmallNextBtnLink']/img[@id='SmallNextBtnImage']"],
             'step_4':["//div[@class='contL']/iframe[@id='ifrmBookStep']",
                       "//form[@id='formDelivery']",
                       "//div[@class ='contR']/div[@class ='buy_info']/p[@id='SmallNextBtn']/a[@id='SmallPrevBtnLink']/img[@id='SmallPrevBtnImage']",
                       "//div[@class ='contR']/div[@class ='buy_info']/p[@id='SmallNextBtn']/a[@id='SmallNextBtnLink']/img[@id='SmallNextBtnImage']"],

             'step_5':["//div[@class='contL']/iframe[@id='ifrmBookStep']",
                       "//div[@class='contFrame frameBg3']" ,
                       "//div[@class ='contR']/div[@class ='buy_info']/p[@id='SmallNextBtn']/a[@id='SmallPrevBtnLink']/img[@id='SmallPrevBtnImage']",
                       "//div[@class ='contR']/div[@class ='buy_info']/p[@id='SmallNextBtn']/a[@id='SmallNextBtnLink']/img[@id='SmallNextBtnImage']"]
             }

driver.window_handles
driver.switch_to.window(main[1])

# 아래 구문을 함수로 만들어서 메뉴 오류가 생기지 않도록 할 예정임(210804 01:;40)

# check step_1
driver.switch_to.frame(driver.find_element(By.XPATH, menu_dic['step_1'][0]))
driver.find_element(By.XPATH, menu_dic['step_1'][1]) # 1 관람일/회차선택 메뉴 선택, 에러나면 해당 메뉴가 아니고 다른 메뉴임

# check step_2
driver.switch_to.frame(driver.find_element(By.XPATH, menu_dic['step_2'][0]))
driver.find_element(By.XPATH, menu_dic['step_2'][1])
# return step_1
driver.find_element(By.XPATH, menu_dic['step_2'][2]).click()  # iframe 안에서 실행하기 때문에 iframe 밖으로 나올 필요가 없다.

#check step_3
driver.switch_to.frame(driver.find_element(By.XPATH, menu_dic['step_3'][0]))
driver.find_element(By.XPATH, menu_dic['step_3'][1])
# return step2
driver.switch_to.default_content()   # iframe 밖에 이전단계 버틑이 있어 iframe 밖으로 나와야 함
driver.find_element(By.XPATH, menu_dic['step_3'][2]).click()

#check step_4
driver.switch_to.frame(driver.find_element(By.XPATH, menu_dic['step_4'][0]))
driver.find_element(By.XPATH, menu_dic['step_4'][1])
#retrun step_3
driver.switch_to.default_content()   # iframe 밖에 이전단계 버틑이 있어 iframe 밖으로 나와야 함
driver.find_element(By.XPATH, menu_dic['step_4'][2]).click()

#check step_5
driver.switch_to.frame(driver.find_element(By.XPATH, menu_dic['step_5'][0]))
driver.find_element(By.XPATH, menu_dic['step_5'][1])
#return step_4
driver.switch_to.default_content()   # iframe 밖에 이전단계 버틑이 있어 iframe 밖으로 나와야 함
driver.find_element(By.XPATH, menu_dic['step_5'][2]).click()

