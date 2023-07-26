import platform
from selenium import webdriver
import chromedriver_autoinstaller
from web_crawling.Telegram_message import telegram_message

def chromedriver_autorun():

    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  #크롬드라이버 버전 확인

    try:
        driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')
    except:

        chromedriver_autoinstaller.install(True)
        driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')

    driver.implicitly_wait(10)
    return driver

# driver 초기화 하고 url 들어가는 함수, os가 윈도우인지, mac인지 구분하고 chrome driver가 저장된 위치를 명시하였으므로 개인 환경에 맞게 적절히 셋팅 필요
def driverAct(url):
    os_ver = platform.system()
    plaform_ver = platform.platform()

    if os_ver == 'Darwin' and plaform_ver == 'Darwin-19.6.0-x86_64-i386-64bit':
        executable_path = '/Users/gwon-yonghwan/PycharmProjects/chromedriver'
        # '/Users/home/PycharmProjects/chromedriver'   # '/usr/local/bin/chromedriver'  # 크롬드라이버가 보안에 막혀서 크롬드라이버를 압축풀고 해당 폴더로 이동시켜주었다
        'driver activation for mac os'
        driver = webdriver.Chrome(executable_path=executable_path)
    elif os_ver == 'Darwin' and plaform_ver == 'macOS-10.16-x86_64-i386-64bit':
        executable_path = '/Users/home/PycharmProjects/chromedriver'
        'driver activation for mac os'
        driver = webdriver.Chrome(executable_path=executable_path)

    elif os_ver == 'Windows' and plaform_ver == 'Windows-10-10.0.19041-SP0':
        # executable_path = "C:\\Users\ohkil\\PycharmProjects\\chromedriver_win32\\chromedriver.exe"  # 크롬드라이버가 보안에 막혀서 크롬드라이버를 압축풀고 해당 폴더로 이동시켜주었다
        # executable_path = "C:/Users\ohkil/PycharmProjects/chromedriver_win32/chromedriver.exe"  # 크롬드라이버가 보안에 막혀서 크롬드라이버를 압축풀고 해당 폴더로 이동시켜주었다
        'driver activation for windows pc'
        driver = chromedriver_autorun()
    else:
        print('Check your OS type')
        telegram_message('Check your chrome driver path or version.')

    driver.set_window_size(1600, 1000)  # (가로, 세로)음
    driver.get(url)
    return driver

