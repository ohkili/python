from selenium.webdriver.common.by import By
from web_crawling.Set_chromedriver import chromedriver_autorun
from web_crawling.Set_chromedriver import driverAct
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

    return driver

if __name__ == '__main__':
    pass