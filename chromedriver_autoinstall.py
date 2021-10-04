from selenium import webdriver
import chromedriver_autoinstaller
import time
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  #크롬드라이버 버전 확인

try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')

driver.implicitly_wait(10)
driver.get("https://somjang.tistory.com") # 사용 샘플
time.sleep(3.0) # 3초가 유지
driver.close() # driver close close만 하면 driver가 살아 있음
driver.quit() # driver 종료
