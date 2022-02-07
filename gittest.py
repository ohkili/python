print('Hello, world')
print('I check local commit task')
print('I check local commit task2')
print('I check local commit task3')
print('I check local commit task4')

x = 0

bool(0)
bool((None))
bool([0])
bool((0))

print('a','b','c', sep='')
print('a' + 'b' + 'c')

for n in range(11):
    if(n%2) !=0:
        continue
    print(n, end=' ')

print('a'*2)

age =1
++age

g = (4,5,4,6)
h ={4,5,6,4}
g.append(66)

# 시스템 확인 하는 문구
from sys import platform
platform
platform
if platform == "linux" or platform == "linux2":
    print('linux')
elif platform == "darwin":
    print('osx') # mac
elif platform == "win32":
    print('windows')

# mac file finding and copying

import os
os.getcwd()
# os.listdir(path): return a list of then entries in the directory given by path
os.listdir(os.getcwd())

os.path.isfile('/Users/home/PycharmProjects/chromedriver')
os.path.isfile('')

'/Users/gwon-yonghwan/PycharmProjects/chromedriver'
'/Users/home/Downlodads'

import shutil
src_dir = '/Users/home/Downloads'
src_fname = 'chromedriver'
dst_dir = '/Users/home/PycharmProjects'
dst_fname = 'chromedriver2'
src = os.path.join(src_dir, src_fname)
dst = os.path.join(dst_dir, dst_fname)
shutil.copy(src, dst)
executable_path = '/Users/home/PycharmProjects/chromedriver2'



# telegram token
# Use this token to access the HTTP API:
# 2062294044:AAEzrGGPlV7C2C-9ZQ9Ji9QbTm7DoG8NgWw
# You will find it at t.me/tele_kili_bot.
# https://api.telegram.org/bot2062294044:AAEzrGGPlV7C2C-9ZQ9Ji9QbTm7DoG8NgWw/getUpdates
# {"ok":true,"result":[{"update_id":337864501,
# "message":{"message_id":3,"from":{"id":1926421781,"is_bot":false,"first_name":"ok","last_name":"kwon","language_code":"ko"},"chat":{"id":1926421781,"first_name":"ok","last_name":"kwon","type":"private"},"date":1635692289,"text":"/start","entities":[{"offset":0,"length":6,"type":"bot_command"}]}}]}
# https://api.telegram.org/bot2062294044:AAEzrGGPlV7C2C-9ZQ9Ji9QbTm7DoG8NgWw/sendMessage?chat_id=1926421781&text=hello

import telegram
telegram_token = "2062294044:AAEzrGGPlV7C2C-9ZQ9Ji9QbTm7DoG8NgWw"

telegram_chat_id = 1926421781

bot = telegram.Bot(token=telegram_token)

bot.sendMessage(chat_id=telegram_chat_id, text='메시지보내기')

import requests
from bs4 import BeautifulSoup
import os

# 웹 페이지를 가져온 뒤 Beautifulsoup 객체로 만든다.
response = requests.get('http://ipo-cc.co.kr/uss/umt/sub04_1.do#sub04_2')  # URL에 대한 응답 개체가 result로 나온다.
soup = BeautifulSoup(response.content, 'html.parser')
# http://ipo-cc.co.kr/uss/umt/sub04_1.do/
file_path = os.path.join( 'E:\\python','ipo_reserve_sub04_2.html')
with open(file_path,'w',encoding='utf-8') as html_file:
    # prettify the soup object and convert it into a string
    html_file.write(str(soup.prettify()))


# save-webpage.py

import urllib.request, urllib.error, urllib.parse

url = 'http://www.oldbaileyonline.org/browse.jsp?id=t17800628-33&div=t17800628-33'

response = urllib.request.urlopen(url)
webContent = response.read()

f = open('obo-t17800628-33.html', 'w')
f.write(webContent)
f.close

# htlml로 저장하기
import urllib.request
urllib.request.urlretrieve('http://ipo-cc.co.kr/uss/umt/sub04_1.do', 'webpage.html')


import requests
url = 'https://www.facebook.com/favicon.ico'


def tri(a,b):
    result = a * b +100

    return result

result = tri(2,3)
print(result)
result = a * b + 100
q =
print(q)
w = 23 * 34 +100
print(w)

qq = tri(30,40)
print(qq)
ww = tri(23,34)
print(ww)


