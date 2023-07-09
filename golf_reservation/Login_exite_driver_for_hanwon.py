from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from web_crawling.Set_chromedriver import chromedriver_autorun
from web_crawling.Set_chromedriver import driverAct
from web_crawling.Close_all_pop_up_return_main import Close_all_pop_up_return_main
from util.pause import pause

def Login_exicte_driver_for_hanwon(info_login):
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
    member_type = info_login['member_type']
    elmt_id_lst = info_login['elmt_id_dict'][member_type]
    elmt_pw = info_login['elmt_pw_dict'][member_type]

    driver = driverAct(url)
    driver.get(loginpage)
    driver = Close_all_pop_up_return_main(driver)

    id_member_type_dict = {'cyber':'rdo_MemGu_C',
                           'honor':'rdo_MemGu_M',
                           'family':'rdo_MemGu_F' }

    id_member_type = driver.find_element(By.ID, id_member_type_dict[member_type])
    driver.execute_script("arguments[0].click();", id_member_type)

    if len(elmt_id_lst) > 0 and len(loginID.split('-')) > 0 and len(elmt_id_lst) == len(loginID.split('-')):

        for i, elmt_id in enumerate(elmt_id_lst):
            userId = driver.find_element(By.ID, elmt_id)
            userId.send_keys(loginID.split('-')[i])
    else:
        pass


    # password
    userPwd = driver.find_element(By.ID, elmt_pw)  # /html/body/div/div[5]/div/div/div/div[2]/div/form/div[1]/div[2]/input
    userPwd.send_keys(loginPW)
    userPwd.send_keys(Keys.ENTER)

    driver.implicitly_wait(1) #seconds
    "accept alert"
    wait = WebDriverWait(driver,10)
    alert_flag = wait.until(EC.alert_is_present())
    if alert_flag:
        driver.switch_to_alert().accept()
    else:
        pass

    driver.implicitly_wait(10)  # seconds
    driver = Close_all_pop_up_return_main(driver)

    return driver