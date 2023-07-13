# 파이썬 소스코드
from pytube import YouTube
# import moviepy.editor as mp
import requests
import glob
# import urllib
import ssl
import os, sys
import numpy as np
import time

# 라이브러리 가져오기

# 1 키워드 검색을 통해 검색된 리스트중에서 조회수 구독 다운로드 등 지표가 높은 항목을 우선 수위 정렬
# 2 저장할 폴더 지정
# 3 저장 파알 이름 형태 지정
# 4 파일 형태 변경 mp4 --> mp3
# 5 1개 파일에 여러 음악이 들어있을때 음원을 분리하여 저장

#ssl  문제 해결 코드
# url = 'https://www.youtube.com/watch?v=lIKmm-G7YVQ'
# requests.get(url)
#
# ssl._create_default_https_context = ssl._create_unverified_context
# yt = YouTube(url)
#
# # 동영상 링크를 이용해 YouTube 객체 생성
#
# print("영상 제목 : ", yt.title)
#
# print("영상 길이 : ", yt.length)
#
# print("영상 평점 : ", yt.rating)
#
# print("영상 썸네일 링크 : ", yt.thumbnail_url)
#
# print("영상 조회수 : ", yt.views)
#
# print("영상 설명 : ", yt.description)
#
# yt_streams = yt.streams
# # YouTube 객체인 yt에서 stream 객체를 생성
#
# print("다운가능한 영상 상세 정보 :")
# for i, stream in enumerate(yt_streams.all()):
#     print(i, " : ", stream)
#
# #audio file streams all searching
# print(i, " : ", stream)
# for i, stream in enumerate(yt.streams.filter(only_audio=True).all()):
#     print(i, " : ", stream)
#
# #audio file highest download & file name  change to mp3
# cwd = os.getcwd()
# down_path = cwd + '/'+  'result_file'
# yt.streams.filter(only_audio=True,file_extension='mp4').order_by('abr').desc().first().download(down_path)
# yt_title = yt.streams.filter(only_audio=True,file_extension='mp4').order_by('abr').desc().first().title.replace(',','')
# file_name = os.path.join( down_path ,yt_title+'.mp4')
# file_name = file_name.replace('|','')
# # file_name = os.path.join(down_path,'[Playlist] 도깨비 OST 전곡 모음 (Goblin OST)  Full Album.mp4')
# file_name_re =  file_name.split('.')[0] +'.mp3'
# # file_name_re = os.path.join( down_path ,'song_100' +'.mp3')
# os.rename(file_name,file_name_re )
# os.path.isfile(file_name_re)
#
from difflib import SequenceMatcher
"""
str1 = 'abc'
str2 = 'abc'

ratio = SequenceMatcher(None, str1, str2).ratio()
print(ratio)
"""

def youtube_downloader_mp3(url, download_path=''):

    #ssl  문제 해결 코드

    requests.get(url)
    try:
        yt = YouTube(url)
    except Exception as e:
        print(e)
        yt = YouTube(url, use_oauth = True, allow_oauth_cache = True)

    # 동영상 링크를 이용해 YouTube 객체 생성

    print("영상 제목 : ", yt.title)
    print("영상 길이 : ", yt.length)
    print("영상 평점 : ", yt.rating)
    print("영상 썸네일 링크 : ", yt.thumbnail_url)
    print("영상 조회수 : ", yt.views)
    print("영상 설명 : ", yt.description)
    try:
        yt_streams = yt.streams
    except:
        # ssl  문제 해결 코드
        ssl._create_default_https_context = ssl._create_unverified_context
        yt_streams = yt.streams

    # YouTube 객체인 yt에서 stream 객체를 생성

    print("다운가능한 영상 상세 정보 :")
    for i, stream in enumerate(yt_streams.all()):
        print(i, " : ", stream)

    #audio file streams all searching
    print(i, " : ", stream)
    for i, stream in enumerate(yt.streams.filter(only_audio=True).all()):
        print(i, " : ", stream)

    #audio file highest download & file name  change to mp3
    if len(download_path)> 0:
        down_path = download_path
    else:
        cwd = os.getcwd()
        down_path = cwd + '/'+  'result_file'
    if os.path.exists(down_path):
        pass
    else:
        os.makedirs(down_path)
    yt.streams.filter(only_audio=True,file_extension='mp4').order_by('abr').desc().first().download(down_path)
    yt_title = yt.streams.filter(only_audio=True,file_extension='mp4').order_by('abr').desc().first().title.replace(',','')

    file_ls = glob.glob(down_path +'/*.mp4')
    ratio_ls = []

    for file in file_ls:
        ratio = SequenceMatcher(None, yt_title, file).ratio()
        ratio_ls.append(ratio)
        print(ratio,file)

    search_no = np.argmax(ratio_ls)
    search_file = file_ls[search_no]
    # search_file = search_file.split('.mp4')[0].replace('.','') + '.mp4'
    # search_file = search_file.replace('|','').replace('!','').replace('*','')
    renamed_file = search_file.replace('.mp4','.mp3')
    os.rename(search_file,renamed_file)
    if os.path.isfile(renamed_file) is True:
        print('File down load is succeed:',renamed_file )


def youtube_downloader(url, download_path='',mp3=True, cnt = 100, use_oauth = True, allow_oauth_cache = True):

    # "mp3 False means mp4, True means mp3"
    # use_oauth = True, allow_oauth_cache = True  solve authentication
    # if age restriction error , class YouTube's __main.py
    # def bypass_age_gate(self):  ==> change  from client=ANDROID_EMBED  to client='ANDROID'

    #ssl  문제 해결 코드

    requests.get(url)

    yt = YouTube(url, use_oauth = use_oauth, allow_oauth_cache = allow_oauth_cache)

    while cnt > 0:
        try:
            title = yt.title
            break
        except:
            print("Failed to get name. Retrying... : ",cnt)
            time.sleep(1)
            yt = YouTube(url)
            cnt -= 1
            continue

    if len(title) < 0:
        title = 'unknown'



    # 동영상 링크를 이용해 YouTube 객체 생성

    print("영상 제목 : ", title)
    print("영상 길이 : ", yt.length)
    print("영상 평점 : ", yt.rating)
    print("영상 썸네일 링크 : ", yt.thumbnail_url)
    print("영상 조회수 : ", yt.views)
    print("영상 설명 : ", yt.description)
    try:
        yt_streams = yt.streams
    except:
        # ssl  문제 해결 코드
        ssl._create_default_https_context = ssl._create_unverified_context
        yt_streams = yt.streams

    # YouTube 객체인 yt에서 stream 객체를 생성

    print("다운가능한 영상 상세 정보 :")
    for i, stream in enumerate(yt_streams.all()):
        print(i, " : ", stream)

    #audio file streams all searching
    print(i, " : ", stream)
    for i, stream in enumerate(yt.streams.filter(only_audio=True).all()):
        print(i, " : ", stream)
    # video file streams all searching
    print(i, " : ", stream)
    for i, stream in enumerate(yt.streams.filter(only_audio=False).all()):
        print(i, " : ", stream)

    #audio file highest download & file name  change to mp3
    if len(download_path)> 0:
        down_path = download_path
    else:
        cwd = os.getcwd()
        down_path = cwd + '/'+  'result_file'
    if os.path.exists(down_path):
        pass
    else:
        os.makedirs(down_path)
    # file type selection
    if mp3 :
        yt.streams.filter(only_audio=True,file_extension='mp4').order_by('abr').desc().first().download(down_path)
        yt_title = yt.streams.filter(only_audio=True,file_extension='mp4').order_by('abr').desc().first().title.replace(',','')
    else:
        yt.streams.filter(only_audio=False, file_extension='mp4').order_by('abr').desc().first().download(down_path)
        yt_title = yt.streams.filter(only_audio=False, file_extension='mp4').order_by('abr').desc().first().title.replace(',', '')
    # file name extension type selection
    if mp3 :

        file_ls = glob.glob(down_path +'/*.mp4')
        ratio_ls = []

        for file in file_ls:
            ratio = SequenceMatcher(None, yt_title, file).ratio()
            ratio_ls.append(ratio)
            print(ratio,file)

        search_no = np.argmax(ratio_ls)
        search_file = file_ls[search_no]
        # search_file = search_file.split('.mp4')[0].replace('.','') + '.mp4'
        # search_file = search_file.replace('|','').replace('!','').replace('*','')
        renamed_file = search_file.replace('.mp4','.mp3')
        os.rename(search_file,renamed_file)
        if os.path.isfile(renamed_file) is True:
            print('File down load is succeed:',renamed_file )
    else:
        print('File down load is succeed:', yt_title)


if __name__ == '__main__':

    download_path = 'Y:/youtube_ext'
    url ='https://www.youtube.com/watch?v=-NvqMPnatig'

    youtube_downloader(url, download_path , mp3 = True, cnt=1000, use_oauth = True, allow_oauth_cache = True)
