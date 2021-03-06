import pandas as pd
from bs4 import BeautifulSoup
import schedule
import time
import os
import json
import requests
# to get code_
#
# 위 참고 사이트를 보면 REST API를 사용하여 엑세스 토큰을 발급 받기 위해선 사용자 코드(code)를
# 먼저 얻어야한다. code를 발급받는 방법은 다음과 같다.
# 1. 브라우저를 통해 developers.kakao.com에 로그인
# 2. 아래 URL을 자신에 맞게 수정 후, 브라우저에 URL 입력
# kauth.kakao.com / oauth / authorize?client_id = {RESTAPIKEY} & redirect_uri = {Redirecturl} & response_type = code
# 3. 위 URL을 입력하여 연결된 페이지의 URL을 확인해보면, ~~~~~code = xxxxxxxxxxxxxxxxxxxxxxxxxx 와 같이 나옴.
#    code 뒤의 값을 복사하여 사용하면 됨. 다음 코드는 REST API를 사용하여 Access Token을 발급받는다.
# (아래 코드에서 사용되는 code값은 위 과정에서 얻은 code값을 아래 코드에 적용하여 코드를 완성)

# https://kauth.kakao.com/oauth/authorize?client_id=22644bd965c28d381ea875a9dde9e2d1&redirect_uri=https://localhost:3000&response_type=code&scope=talk_message
# https://localhost:3000/?code=TqTfv_rWYM2XJvMHJZPfjWrPgCvUNIEUrMare5oJzX_UtNARO67IlfHJaW4HKSCdnl6O3Ao9c5sAAAF8KA1TEw
REST_API_KEY ='22644bd965c28d381ea875a9dde9e2d1'
# 카카오톡 메시지 API에서 code를 생성하기 위하여 1회만 시행, 다시 시도하면 에러 남, 위에 to get code_ 재시행 필요
initial_time = 0
if initial_time == 1:

    url = "https://kauth.kakao.com/oauth/token"
    Redirect_URI = "https://localhost:3000"
    code_ = 'MiLGUgPQwy34PYv5z5IOc2o2vyn0Mj92lvKDkq_iwywicmJubX0PTCVY7cP6Vb5Lz9xOHgo9dBEAAAF81jp7Yw'
    data = {
        "grant_type" : "authorization_code",
        "client_id" : REST_API_KEY,
        "redirect_url" : Redirect_URI,
        "code" : code_
    }
    response = requests.post(url, data=data)
    tokens = response.json()
    print(tokens)

    access_token = tokens['access_token']
    refresh_token = tokens['refresh_token']
elif initial_time != 0:
    print('find refresh token')
# refresh_token is borrow
refresh_token = '2hZcRLD01s1Rl0qEA0BhnenFH1om0rtTNimYSgo9cuoAAAF81jvBOA'
#==========
# 카카오톡 메시지 API
# rest api key와 refresth token을 이용하여 access token 갱신
def access_token_mkr(REST_API_KEY,refresh_token):
    url = "https://kauth.kakao.com/oauth/token"

    data = {
        "grant_type": "refresh_token",
        "client_id": REST_API_KEY,
        "refresh_token": refresh_token
    }
    response = requests.post(url, data=data)
    tokens2 = response.json()
    print(tokens2)

    access_token = tokens2['access_token']
    return access_token

def kakao_message(data, access_token):
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    # access_token = 'pnvTjrwWOlNoRrFHo5IEfDco_Mi9Kf7R-vC_TQorDNMAAAF8IfKFow'  # tokens['access_token']

    # 사용자 토큰
    headers = {
        "Authorization": "Bearer " + access_token}

    data = {
        "template_object": json.dumps({"object_type": "text",
                                   "text": str(data),
                                       "link": {
                                           "web_url": "www.naver.com"
                                       }
                                       })
    }

    response = requests.post(url, headers=headers, data=data)
    print(response.status_code)
    if response.json().get('result_code') == 0:
        print('메시지를 성공적으로 보냈습니다.')
    else:
        print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))


token = access_token_mkr(REST_API_KEY,refresh_token)

kakao_message(token, token)
