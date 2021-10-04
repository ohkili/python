from selenium import webdriver
import chromedriver_autoinstaller
import time

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
#    0) 주요 골프자 리스트 마에스트로, 리베라,소노펠리체,
#    1) log in id/pw ,
#    2) 예약 날짜 시간 선택 조건으로 날짜대, 시간 대  고를수 있어야 하고, 시간대를 고르렴 가능한 시간중  몇번째를 고를지 옵션 필요
#    3)각 골프장 예약 오프되는 시간대 db로 저장 및 관리
# 2. 알림 메세지
#    1) 취소 가능일 전 미리 취소 여부 알람 메세지
#    2) 동반자에게 미리 알리기
# 3. 양도 기능
#    1) 예약 시간 양도 관련 내가 취소 즉시 다른 사람이 예약 가능하도록 변경 기능
#