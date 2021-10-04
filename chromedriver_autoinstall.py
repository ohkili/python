from selenium import webdriver as wd
import chromedriver_autoinstaller
import time
path = chromedriver_autoinstaller.install()
driver = wd.Chrome(path)
driver.get("https://somjang.tistory.com")
time.sleep(3.0)
driver.close()
driver.quit()
