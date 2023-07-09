from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from web_crawling.Set_chromedriver import chromedriver_autorun
from web_crawling.Set_chromedriver import driverAct
from web_crawling.Close_all_pop_up_return_main import Close_all_pop_up_return_main
from util.pause import pause
def Login_exicte_driver(info_login):
    """ example
       info_login_rivera = {'url'        : 'https://www.shinangolf.com/',
                  'loginPage'  : 'https://www.shinangolf.com/member/login',
                  'id'         : '??????',
                  'pw'         : '???????',
                  'elmt_id'    : 'memberId',
                  'elmt_pw'    : 'key'
                  }
       """
    url = info_login['url']
    loginpage = info_login['loginPage']
    loginID = info_login['id']
    loginPW = info_login['pw']
    elmt_id = info_login['elmt_id']
    elmt_pw = info_login['elmt_pw']

    driver = driverAct(url)
    driver.get(loginpage)

    # id
    userId = driver.find_element(By.ID, elmt_id)  # /html/body/div/div[5]/div/div/div/div[2]/div/form/div[1]/div[1]/input
    userId.send_keys(loginID)  # 로그인 할 계정 id

    # password
    userPwd = driver.find_element(By.ID, elmt_pw)  # /html/body/div/div[5]/div/div/div/div[2]/div/form/div[1]/div[2]/input
    userPwd.send_keys(loginPW)
    userPwd.send_keys(Keys.ENTER)

    driver.implicitly_wait(1)  # seconds
    "accept alert"
    wait = WebDriverWait(driver, 10)
    alert_flag = wait.until(EC.alert_is_present())
    if alert_flag:
        driver.switch_to_alert().accept()
    else:
        pass

    driver.implicitly_wait(10)  # seconds
    driver = Close_all_pop_up_return_main(driver)

    return driver

if __name__ == '__main__':
    pass