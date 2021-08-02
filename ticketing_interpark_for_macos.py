# 방식
# 1 화면 클릭 방식
# 2 html 입력 방식
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
os = {'mac':'mac',
      'win':'windows'}

os_option = os['win']
if os_option == 'mac':
    executable_path = '/usr/local/bin/chromedriver' # 크롬드라이버가 보안에 막혀서 크롬드라이버를 압축풀고 해당 폴더로 이동시켜주었다
elif os_option == 'windows':
    # executable_path = "C:\\Users\ohkil\\PycharmProjects\\chromedriver_win32\\chromedriver.exe"  # 크롬드라이버가 보안에 막혀서 크롬드라이버를 압축풀고 해당 폴더로 이동시켜주었다
    executable_path = "C:/Users\ohkil/PycharmProjects/chromedriver_win32/chromedriver.exe"  # 크롬드라이버가 보안에 막혀서 크롬드라이버를 압축풀고 해당 폴더로 이동시켜주었다

else:
    print('Check your OS type')


driver = webdriver.Chrome(executable_path = executable_path)
# driver.close()
# 사이즈조절
driver.set_window_size(1400, 1000)  # (가로, 세로)음
driver.get('https://ticket.interpark.com/Gate/TPLogin.asp') # 페이지 이동

driver.switch_to.frame(driver.find_element(By.XPATH, "//div[@class='leftLoginBox']/iframe[@title='login']"))
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
time.sleep(8)
# 팝업창 1개 일때
# driver.switch_to.window(driver.window_handles[1])
# driver.close()
# 팝업창이 여러개 일때 사용하는데 210801 현재 팝업 인지도 안되고 팝업 제거도 안됨, driver.window_handles는 인터넷 tab을 인지함 , 팝업이 tab으로 인식되지 않음
main = driver.window_handles
for handle in main:
    if handle != main[0]:   # main[0] means main
        driver.switch_to.window(handle)
        driver.close()


try:
    result = driver.switch_to.alert()
    print(result.text)

    # Alert 창 확인
    result.accept()
    # Alert 창 닫기
    result.dismiss()

except:
    "popup : nothing"

print(driver.window_handles)
# 예매안내 팝업 뜸 코로나 어쩌구 저쩌, 팝업 제거 안되면 예매하기 클릭 안됨

driver.find_element(By.XPATH, "//div[@class='popupTitle']/a")
driver.find_element(By.LINK_TEXT, '닫기')
popup = driver.find_element_by_class_name('popupTitle')
print(popup.tag_name)

print(popup.get_attribute('value'))
source = driver.page_source

driver.find_element(By.XPATH, "//div[@class='sideBtnWrap']/a").click() # 클릭까지 성공(210728)


# 연습
elements = driver.find_elements_by_xpath("//div[@class='popupWrap']/div[@class='popupFooter']/button[@class= 'popupCloseBtn is-bottomBtn']")
len(elements)
for element in elements:
    print(element.text)

elements = driver.find_elements_by_xpath("//div[@class='popupWrap']")
for element in elements:
    print(element.tag_name, element.parent, element.location, element.size ,element.get_attribute('class'),  element.text)



element.get_attribute('class')

