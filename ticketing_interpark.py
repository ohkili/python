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

# 예매 화면에서 관람일/회차선택으로 위치하게 하는 함수, 간혹 어뚱하게 좌석 선택 배송 선택등에 위치하는 경우가 있음
def interparkTicketting_move_step1(driver):
    # step_dic 'step info': 'main address','sub address', 'prev button', 'next button'
    step_dic = {'step_1': ["//div[@class='contL']/iframe[@id='ifrmBookStep']",
                           "//div[@class='contFrame frameBg6']"],
                'step_2': ["//div[@id='divBookSeat']/iframe[@id='ifrmSeat']",
                           "//div[@class='seatL']/iframe[@id='ifrmSeatDetail']",
                           "//div[@class ='seatR']/div[@class='inner']/div[@class='btnWrap']/p[@class ='fl_l']/a"],
                'step_3': ["//div[@class='contL']/iframe[@id='ifrmBookStep']",
                           "//div[@class='contFrame frameBg2']",
                           "//div[@class ='contR']/div[@class ='buy_info']/p[@id='SmallNextBtn']/a[@id='SmallPrevBtnLink']/img[@id='SmallPrevBtnImage']",
                           "//div[@class ='contR']/div[@class ='buy_info']/p[@id='SmallNextBtn']/a[@id='SmallNextBtnLink']/img[@id='SmallNextBtnImage']"],
                'step_4': ["//div[@class='contL']/iframe[@id='ifrmBookStep']",
                           "//form[@id='formDelivery']",
                           "//div[@class ='contR']/div[@class ='buy_info']/p[@id='SmallNextBtn']/a[@id='SmallPrevBtnLink']/img[@id='SmallPrevBtnImage']",
                           "//div[@class ='contR']/div[@class ='buy_info']/p[@id='SmallNextBtn']/a[@id='SmallNextBtnLink']/img[@id='SmallNextBtnImage']"],
                'step_5': ["//div[@class='contL']/iframe[@id='ifrmBookStep']",
                           "//div[@class='contFrame frameBg3']",
                           "//div[@class ='contR']/div[@class ='buy_info']/p[@id='SmallNextBtn']/a[@id='SmallPrevBtnLink']/img[@id='SmallPrevBtnImage']",
                           "//div[@class ='contR']/div[@class ='buy_info']/p[@id='SmallNextBtn']/a[@id='SmallNextBtnLink']/img[@id='SmallNextBtnImage']"]
                }
    step_flag =5
    driver.switch_to.default_content()
    try:
        #check step_5
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element(By.XPATH, step_dic['step_5'][0]))
        driver.find_element(By.XPATH, step_dic['step_5'][1])
        #return step_4
        driver.switch_to.default_content()   # iframe 밖에 이전단계 버틑이 있어 iframe 밖으로 나와야 함
        driver.find_element(By.XPATH, step_dic['step_5'][2]).click()

    except NoSuchElementException:
        print('NoSuchElementException')
        print('Maybe your step is before step',step_flag)
    step_flag -= 1
    try:
        # check step_4
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element(By.XPATH, step_dic['step_4'][0]))
        driver.find_element(By.XPATH, step_dic['step_4'][1])
        # retrun step_3
        driver.switch_to.default_content()  # iframe 밖에 이전단계 버틑이 있어 iframe 밖으로 나와야 함
        driver.find_element(By.XPATH, step_dic['step_4'][2]).click()
    except NoSuchElementException:
        print('NoSuchElementException')
        print('Maybe your step is before step', step_flag)
    step_flag -= 1
    try:
        # check step_3
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element(By.XPATH, step_dic['step_3'][0]))
        driver.find_element(By.XPATH, step_dic['step_3'][1])
        # return step2
        driver.switch_to.default_content()  # iframe 밖에 이전단계 버틑이 있어 iframe 밖으로 나와야 함
        driver.find_element(By.XPATH, step_dic['step_3'][2]).click()
    except NoSuchElementException:
        print('NoSuchElementException')
        print('Maybe your step is before step', step_flag)
    step_flag -=1

    try:
        # check step_2
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element(By.XPATH, step_dic['step_2'][0]))
        driver.find_element(By.XPATH, step_dic['step_2'][1])
        # return step_1
        driver.find_element(By.XPATH, step_dic['step_2'][2]).click()  # iframe 안에서 실행하기 때문에 iframe 밖으로 나올 필요가 없다.
    except NoSuchElementException:
        print('NoSuchElementException')
        print('Maybe your step is before step', step_flag)
    step_flag -= 1

    try:
        # check step_1
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element(By.XPATH, step_dic['step_1'][0]))
        driver.find_element(By.XPATH, step_dic['step_1'][1])  # 1 관람일/회차선택 메뉴 선택, 에러나면 해당 메뉴가 아니고 다른 메뉴임
    except NoSuchElementException:
        print('NoSuchElementException')
        print('Maybe your step is before step', step_flag)
    step_flag -=1

    if step_flag<1:
        print('Check your interpark reservation window, there is no match!')
    else:
        print('You are on step 1')

def lack(t):
    print('sleep {0} sec'.format(t))
    time.sleep(t)

def check_exists_by_element(by, name):
    try:
        driver.find_element(by, name)
    except NoSuchElementException:
        return False
    return True



# 예매조건
wantYear = '2021'
wantMonth = '8'
wantDate = '16'
wantHour = '18'
wantMin = '00'

url = 'https://ticket.interpark.com/Gate/TPLogin.asp'
driver = driverAct(url)

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


# 예매하기 버튼 클릭기
# pop up  창 확인하여 닫아주기
print(driver.window_handles)

# lack(1)

# 예매안내 팝업 뜸 코로나 어쩌구 저쩌, 팝업 제거 안되면 예매하기 클릭 안됨
# driver.find_element(By.XPATH, "//div[@class='popupWrap']/div[@class='popupFooter']/button[@class='popupCloseBtn is-bottomBtn']").click()

# 다음버튼 클릭
next = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.XPATH,"//div[@class='popupWrap']/div[@class='popupFooter']/button[@class='popupCloseBtn is-bottomBtn']"))
            )
next[0].click()


driver.page_source
soup_first = BeautifulSoup(driver.page_source,'html.parser') # 새로 생긴 티켓예매 탭의 html을 파싱했음

reserv_first_txt = str(soup_first)

# 파일 쓰기
f = open('E:/work/reserv_first_txt.txt','w', encoding='UTF-8')
f.write(reserv_first_txt)
f.close()



# poticket.interpark.com 내용 제목으로 팝업 뜸, 관람일 전일 오후 어쩌구 저쩌구 취소/변경/환불 불가하다고 팝업 뜸 예매 진행하시겠습니까?
# 라고 팝업 뜸
# 이상태는 인터넷 탭이 하나 추가 된 상태임, 관람일 좌석 가격 선택하는 탭이 생성이 되었음 이제 해당 탭으로 옮겨 가야함
# 예매하기 누르기전에 날짜를 선택하는것으로 변경
driver.switch_to.window(driver.window_handles[0])
calen = driver.find_elements(By.CSS_SELECTOR, ".datepicker-panel")
uls = calen[0].find_elements(By.TAG_NAME, "ul")
year_month = uls[0].find_elements(By.TAG_NAME, "li")[1].text.split('. ')
year = year_month[0]  # 년
month = year_month[1]  # 월

yearC = int(wantYear) - int(year)
monthC = int(wantMonth) - int(month)

prev = uls[0].find_elements(By.TAG_NAME, "li")[0]
next = uls[0].find_elements(By.TAG_NAME, "li")[2]

s = yearC * 12 + monthC
i = 0
if s > 0:
    while i < s:
        next.click()
        i = i + 1
elif s < 0:
    while i < s:
        prev.click()
        i = i - 1

# 선택 가능한 날짜 모두 가져오기
CellPlayDate =driver.find_elements(By.XPATH, "//ul[@data-view='days']/li[@class!='disabled']")
for cell in CellPlayDate:
    if cell.text == wantDate:
        cell.click()
        break

    # 선택 가능한 시간 가져오기
time_li = driver.find_elements(By.XPATH, "//a[@class='timeTableLabel']/span")

hour_min = wantHour + ":" + wantMin

for li in time_li:
    if li.text == hour_min:
        li.click()
        break



# 예매하기 버튼임, 아래 구문을 보면 /a 다음에 속성 정보가 없는데 이렇게 하면 a tag 전체를 선택하게 되는것임
driver.find_element(By.XPATH, "//div[@class='sideBtnWrap']/a").click() # 클릭까지 성공(210728)



# 파일 읽기
# f = open('E:/work/soup_txt.txt','r', encoding='euc-kr')
# content = f.read()
# print(content)




driver.window_handles
driver.switch_to.window(driver.window_handles[1])



# poticket.interpark.com 내용 제목으로 팝업 뜸, 관람일 전일 오후 어쩌구 저쩌구 취소/변경/환불 불가하다고 팝업 뜸 예매 진행하시겠습니까?
# 라고 팝업 뜸
# 이상태는 인터넷 탭이 하나 추가 된 상태임, 관람일 좌석 가격 선택하는 탭이 생성이 되었음 이제 해당 탭으로 옮겨 가야함
# 예매하기 누르기전에 날짜를 선택하는것으로 변경 




 # 예매안내 만 13세 어쩌구 저쩌구  팝업 속성은 아래와 같으며 close 버튼 찾아서 눌러줌
# driver.find_element(By.XPATH, "//div[(@class='bookNoticeLayer')]/div[@class='layerWrap']/div[@class='titleArea']/a[@class='closeBtn']").click()
# 다음버튼 클릭
next1 = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.XPATH,"//div[(@class='bookNoticeLayer')]/div[@class='layerWrap']/div[@class='titleArea']/a[@class='closeBtn']"))
            )
next1[0].click()



driver.page_source
soup_second = BeautifulSoup(driver.page_source,'html.parser') # 새로 생긴 티켓예매 탭의 html을 파싱했음

reserv_second_txt = str(soup_second)

# 파일 쓰기
f = open('E:/work/reserv_second_txt.txt','w', encoding='UTF-8')
f.write(reserv_second_txt)
f.close()

# 날짜는 예매하기 누르기 전에 선택하였으니 좌석 선택으로 넘어가자
# step1로 이동하는 함수 어디에 위치해 있든 step1로 이동
interparkTicketting_move_step1(driver)

# 
# 시간 클릭 전 활성화 대기
# 태그가 만들어 질 때 까지 30초간 기다림 , 30초전 태그가 활성화 되면 바로 실행

# iframe의 부모 프레임으로 돌아가기
driver.switch_to.default_content()
# 다음버튼 클릭
next = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@class='contR']/div[@class='buy_info']/p[@id='LargeNextBtn']/a/img"))
            )
next[0].click()

# 자동예매 방지 문자열입력이 떠있는지 확인
driver.switch_to.frame(driver.find_element(By.XPATH, "//div[@id='divBookSeat']/iframe[@id='ifrmSeat']"))
capchaLayer_check = check_exists_by_element(By.XPATH, "//div[@id='divRecaptcha']")
# 자동예매 방지 문자열 입력창이 있다면 5초 대기
# 공연에 따라 자동 예매 방지 문자열 입력을 하라고 팝업창이 나올 수가 있습니다.
# 이건....  자동으로 입력이 불가능해서 사용자가 입력할 시간을 기다려 준 후 움직이게 해 줍니다.
# 대기시간을 5초는 입력하는 시간보다 많이 길 수 있어서 원하는 대로 줄여도 무방합니다.
if capchaLayer_check:
    time.sleep(5)


# 좌석 선택 iframe, 해당 ifram의 parent node를 선택하면 됨, parent의parent까지 찾아갈 필요 없음
driver.switch_to.frame(driver.find_element(By.XPATH, "//div[@class='seatL']/iframe[@id='ifrmSeatDetail']"))
# 활성화 되어 있는 좌석의 class 속성 stySeat
seat_check = driver.find_elements(By.CSS_SELECTOR, "img.stySeat")
seat_title = [s.get_attribute('title') for s in seat_check]
seat_ls = [s.split('-') for s in seat_title]
# 좌석 선택하는 태그의 title 속성의 포멧
# [VIP석] 1층-A구역18열-11
# [VIP석] 1층-B구역 11열-1
# [VIP석] 1층-D열-99
# [VIP석] 1층-11열-11
# [VIP석] 1층-A블럭8열-10

'-'.join(seat_ls[0]) # list 내부 문자열을 join 으로 합치기
# 좌석 이름 규치, 등급(R,S,),층(1,2),열(A~Z),좌석(1~1000)
# seatLevel = seat_ls[0][0].split(' ')[0].replace('[','').replace(']','').replace('석','')
# seatFloor = seat_ls[0][0].split(' ')[1].replace('층','')
# seatCol = seat_ls[0][1].replace('열','')
# seatNo = seat_ls[0][2]

def seat_info(seat_ls):
    result = []
    for i in range(len(seat_ls)):
        seatLevel = seat_ls[i][0].split(' ')[0].replace('[', '').replace(']', '').replace('석', '')
        seatFloor = seat_ls[i][0].split(' ')[1].replace('층', '')
        seatCol = seat_ls[i][1].replace('열', '')
        seatNo = seat_ls[i][2]
        result.append([[seatLevel, seatFloor, seatCol, seatNo], '-'.join(seat_ls[i])])
    return result
#
#
# result = []
# for i in range(len(seat_ls)):
#     seatLevel = seat_ls[i][0].split(' ')[0].replace('[', '').replace(']', '').replace('석', '')
#     seatFloor = seat_ls[i][0].split(' ')[1].replace('층', '')
#     seatCol = seat_ls[i][1].replace('열', '')
#     seatNo = seat_ls[i][2]
#     result.append([ [seatLevel, seatFloor, seatCol, seatNo], '-'.join(seat_ls[i]) ])

seat_info = seat_info(seat_ls)

# 선택 유형 고르면 좌석 번호는 작은 순번으로 고르기로 함
choice_level = ['R','S']
choice_floor = ['1','2']
choice_col = ['C','D','E','F','G']
choice_no = ['10','11','12','13','20']
# seat_info[0][1]

choice_ls =[]
for l in choice_level:
    for f in choice_floor:
        for c in choice_col:
            for n in choice_no:
                temp = []
                temp.append(l)
                temp.append(f)
                temp.append(c)
                temp.append(n)
                choice_ls.append(temp)



seat_matched =[]
for s in seat_info:
    for l in choice_ls:
        if s[0] ==  l:
            print('seat catched :', s[1])
            seat_matched.append(s[1])
        else:
            print('no seat ', s[1])

seat_matched

# seat_selected =  "//img[ @class='stySeat' and @title=" + "'" + seat_matched[0] + "']"
# seat_selected1 =  "//img[ @class='stySeat' and @title=" + "'" + seat_matched[1] + "']"

# driver.find_elements(By.CSS_SELECTOR, "img.stySeat" )
# driver.find_element(By.XPATH, "//img[ @class='stySeat'  and  @title='[R석] 1층-D열-20']").click()
# driver.find_element(By.XPATH,seat_selected).click()
# driver.find_element(By.XPATH,seat_selected1).click()

# 좌석 선택 매수 선택
cnt_select =2

for i in range(cnt_select):
    seat_selected = "//img[ @class='stySeat' and @title=" + "'" + seat_matched[i] + "']"
    driver.find_element(By.XPATH, seat_selected).click()

# 원래 팝업 프레임으로 돌아가기
driver.switch_to.default_content()
driver.switch_to.frame(driver.find_element(By.XPATH, "//div[@id='divBookSeat']/iframe[@id='ifrmSeat']"))
# 다음 버튼 클릭
driver.find_element(By.XPATH, "//div[@class='seatR']/div[@class='inner']/div[@class='btnWrap']/a/img").click()
# 좌석 선택을 할 때 내가 원하는 좌석을 지정해서 선택을 하고 싶어서 title속성에 좌석 좌표를 이용해서 원하는 좌석을 선택할 수 있게 해 줍니다.

# step 3 가격/할인 선택 메누로 이동

# 기본가로 선택하기로 함
driver.switch_to.default_content()  # 좌석 선택 ifram에서 빠져 나옴
driver.switch_to.frame(driver.find_element(By.XPATH, "//div[@class='contL']/iframe[@id='ifrmBookStep']"))
driver.find_element(By.XPATH, "//tr[@id='PriceRow002']/td[@class='taL']/select[@name='SeatCount']")
option_value = "//option[@value='" +str(cnt_select) +  "']"
driver.find_element(By.XPATH, option_value).click()

# 다음단계 선택해서 4.배송선택/주문자확인으로 넘어가야 함
driver.switch_to.default_content()
driver.find_element(By.XPATH, "//p[@id='SmallNextBtn']/a[@id='SmallNextBtnLink']/img").click()

#step4 배송 선택/주문자 확인
