
"""
import re
import requests
from bs4 import BeautifulSoup

url = "https://anime-world.in/?trembed=0&trid=1930&trtype=2"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Referer": "https://anime-world.in/",
}
s = requests.session()
with requests.session() as s:
    soup = BeautifulSoup(s.get(url).content, "html.parser")
    url2 = soup.iframe["src"]
    html_doc = s.get(url2, headers=headers).text
    link = re.search(r'file:".*?(http[^",]+)', html_doc).group(1)
    print(link)

    with open("file.mp4", "wb") as f:
        f.write(s.get(link, headers=headers, verify=False).content)

    print("Done.")
    link = "https://ndoodle.xyz/video/1fb2a1c37b18aa4611c3949d6148d0f8"
    with open("F:/stream_download/file.mp4", "wb") as f:
        f.write(s.get(link, verify=False).content)
"""
import glob

import requests
import time
import os
from natsort import natsorted

from moviepy.editor import VideoFileClip ,concatenate_videoclips


#

# url = "https://cdn7-ndoodle.xyz/cdn/down/5d548a1b558d5036878a3523ae9326af/Video/720p/720p_261.aaa"
#
# url = "https://ndoodle.xyz/subtitles/2021-4/반요야샤2기01.srt"
# https://ndoodle.xyz/subtitles/2021-4/반요야샤2기02.srt
# # download_file(path,url)
# # https://cdn15-ndoodle.xyz/cdn/down/5d548a1b558d5036878a3523ae9326af/Video/360p/360p_014.aaa
# # https://cdn12-ndoodle.xyz/cdn/down/5d548a1b558d5036878a3523ae9326af/Video/720p/720p_131.aaa

# "https://cdn1-catcdn.top/cdn/down/981b73978972e7699529b167e838a557/Video/720p/720p_015.aaa"
# # num = 131
# # num_pad = str(num).zfill(3)
# # orbit = num % 15 +1
# # https_form = "https://cdn" + str(orbit) + "-ndoodle.xyz/cdn/down/5d548a1b558d5036878a3523ae9326af/Video/720p/720p_" + num_pad + ".aaa"
# "https://ndoodle.xyz/subtitles/2021-4/반요야샤2기22ns.srt"
# middle_form = 'piggy.xyz/cdn/down/5cb3d92c6e991fa134676572ea7d03ea'
# num=1000
# orbit_num = 15
# init_num = 16

def make_download_url(num, middle_form,orbit_num = 15 ,init_num = 3):
    download_url = []
    head_dict = {'xdoodle': "cdn",
                 'nydoodle': "cdn",
                 'ndoodle' :"cdn",
                 'piggy'  : "cloud"
                 }
    for i in range(num):
        num_pad = str(i).zfill(3)
        orbit = str(i % orbit_num + init_num)
        https_form = "https://" + head_dict[middle_form.split('.')[0]]  +  str(orbit) + "-" + middle_form + "/Video/720p/720p_" + num_pad + ".aaa"
        download_url.append(https_form)
    return download_url
# path = path_root
# url = srt_file_dict[key]
def download_file(path,url,manual_file_name = ''):

    if url.split('.')[-1] == 'srt':
        if len(manual_file_name) == 0:
            fpath_downlaod = path + '/' + url.split('/')[-1]
        else:
            fpath_downlaod = path + '/'  + manual_file_name + '.srt'
    else:
        fpath_downlaod = path + '/' + url.split('/')[-1].replace('.','') + '.mp4'

    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    print(r)
    with open(fpath_downlaod, 'wb') as f:
        for chunk in r.iter_content(chunk_size=256):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    time.sleep(0.5)

    return fpath_downlaod

#
# path = 'F:/stream_download'
# download_url = make_download_url(338)
# for url in download_url:
#     download_file(path,url)
#     print(url, requests.get(url, stream=True))

#
# for num in range(1,25):
#     url = "https://ndoodle.xyz/subtitles/2021-4/반요야샤2기" + str(str(num).zfill(2)) + ".srt"
#     download_file(path,url)

def combine_videos_folder_to_one(folder_path,filename):
    L = []
    for root, dirs, files in os.walk(folder_path):
        # files.sort()
        files = natsorted(files)
        for file in files:

            if os.path.splitext(file)[1] == '.mp4':
                filePath = os.path.join(root, file)
                video = VideoFileClip(filePath)
                L.append(video)
                print(file)

    final_clip = concatenate_videoclips(L)
    final_clip.to_videofile(os.path.join(folder_path,filename +".mp4"), fps=60, remove_temp=False)
#
# folder_path = 'F:\stream_download'  # 'F:\stream_download'
# filename = 'banyo_yashahime_201'
# combine_videos_folder_to_one(folder_path,filename)

"""
ex) filename is  'banyo_yashahime_201'
    foldername is  'banyo_yashahime_201'
                    
"""

file_dict_bk = { #'banyo_yashahime_201': 'ndoodle.xyz/cdn/down/5d548a1b558d5036878a3523ae9326af',
              #'banyo_yashahime_202': 'catcdn.top/cdn/down/981b73978972e7699529b167e838a557',
              #'banyo_yashahime_203': 'ndoodle.xyz/cdn/down/92af8189e113a54cc43301d2af8dae48',
              'banyo_yashahime_204': 'ndoodle.xyz/cdn/down/280a93ca3444aac0c3f84ffbd3ba5890',
              'banyo_yashahime_205' : 'ndoodle.xyz/cdn/down/96afacf75ddeaa59c7b887f72d52cbc8',
              'banyo_yashahime_206' : 'ndoodle.xyz/cdn/down/63cfff796f50268176110261ba15b1e9',
              'banyo_yashahime_207' : 'ndoodle.xyz/cdn/down/a7d18497abf425c95ce90b756eec56c0',
              'banyo_yashahime_208' : 'ndoodle.xyz/cdn/down/5c34e4c4d0761118ec35191d236ecb31',
              'banyo_yashahime_209' : 'ndoodle.xyz/cdn/down/7d96b8304abb6dcabc607378af5daa76',
              'banyo_yashahime_210' : 'ndoodle.xyz/cdn/down/1ece543da3a8688a8af1937169bf6182',
              'banyo_yashahime_211' : 'ndoodle.xyz/cdn/down/942b1682d21ca0478a554b1f72223bc3',
              'banyo_yashahime_212' : 'ndoodle.xyz/cdn/down/2f693250959b7919af257e21ebd0f052',
              'banyo_yashahime_213' : 'ndoodle.xyz/cdn/down/f6d7d33733de94e11352d3cc92eba121',
              'banyo_yashahime_214' : 'ndoodle.xyz/cdn/down/f1e57aaf55c15b0d1d7587381e262d9f',
              'banyo_yashahime_215' : 'ndoodle.xyz/cdn/down/cdb6f70ffaa10a902a23281da3aa36ca',
              'banyo_yashahime_216' : 'ndoodle.xyz/cdn/down/8829b0d81904fbd3f4aea953d3cd90b7',
              'banyo_yashahime_217' : 'ndoodle.xyz/cdn/down/ce4d660c0162e17175ae1fb89939b324',
              'banyo_yashahime_218' : 'ndoodle.xyz/cdn/down/04f9aaa89a3d86fd7b09460dfb38d800',
              'banyo_yashahime_219' : 'ndoodle.xyz/cdn/down/15408bc0fc6a47b0ea719083f9c67eb0',
              'banyo_yashahime_220' : 'ndoodle.xyz/cdn/down/1b575444ee8ca3ad61811f6b191c8150',
              'banyo_yashahime_221' : 'ndoodle.xyz/cdn/down/8b9ecaf31f25cf744114c90a9e80cf76',
              'banyo_yashahime_222' : 'ndoodle.xyz/cdn/down/1182d8b5929d24ac5a7e78c5a5fde316',
              'banyo_yashahime_223' : 'ndoodle.xyz/cdn/down/1a9df5515335442315a11722e03de1ad',
              'banyo_yashahime_224' : 'ndoodle.xyz/cdn/down/e5cbb9df2cf7c6277b0c12f1e07743bd'
              }

mp4_file_dict = { #'banyo_yashahime_201': 'ndoodle.xyz/cdn/down/5d548a1b558d5036878a3523ae9326af',
              #'banyo_yashahime_202': 'catcdn.top/cdn/down/981b73978972e7699529b167e838a557',
              #'banyo_yashahime_203': 'ndoodle.xyz/cdn/down/92af8189e113a54cc43301d2af8dae48',
              # 'party_people_kongmyeong_001': [13,3,'xdoodle.xyz/cdn/down/ead9853a64c5e34f323f5a0c6a51571e'],
              # 'party_people_kongmyeong_002': [13,3,'xdoodle.xyz/cdn/down/e83bb7b0da390abc1e2fcba261a7b787'],
              # 'party_people_kongmyeong_003-1': [15,1,'nydoodle.xyz/cdn/down/5cb3d92c6e991fa134676572ea7d03ea'],
              # 'party_people_kongmyeong_003-2': [15,16,'piggy.xyz/cdn/down/5cb3d92c6e991fa134676572ea7d03ea'],
              # 'party_people_kongmyeong_004-1': [15,1,'nydoodle.xyz/cdn/down/3159e87ec8a9d575e026471393f1d5b1'],
              # 'party_people_kongmyeong_004-2': [15,16,'piggy.xyz/cdn/down/3159e87ec8a9d575e026471393f1d5b1'],
              # 'party_people_kongmyeong_005': [13,3,'xdoodle.xyz/cdn/down/256fea8d6668715b850295fc1d04c200'],
              # 'party_people_kongmyeong_006': [15,1,'ndoodle.xyz/cdn/down/21dbba6f80379130d90c09fd5933af15'],
              # 'party_people_kongmyeong_007-1': [15,1,'nydoodle.xyz/cdn/down/bccb652ed2cdd4e5b3aa202861b585f2'],
              'party_people_kongmyeong_007-2': [15,16,'piggy.xyz/cdn/down/bccb652ed2cdd4e5b3aa202861b585f2'],
              'party_people_kongmyeong_008-1': [15,1,'nydoodle.xyz/cdn/down/6109d1f50dbb4d6bb876e62b4f460fbe'],
              'party_people_kongmyeong_008-2': [15,16,'piggy.xyz/cdn/down/6109d1f50dbb4d6bb876e62b4f460fbe'],
              'party_people_kongmyeong_009': [13,3,'xdoodle.xyz/cdn/down/4347cefc2bcfd20ef094e506924c85af'],
              'party_people_kongmyeong_010-1': [15,1,'nydoodle.xyz/cdn/down/f31753d1f499bec931e785402a1f4b9a'],
              'party_people_kongmyeong_010-2': [15,16,'piggy.xyz/cdn/down/f31753d1f499bec931e785402a1f4b9a'],
              'party_people_kongmyeong_011': [15,1,'ndoodle.xyz/cdn/down/82f4a521864268f9999bf387b7eff9a9'],
              'party_people_kongmyeong_012': [13,3,'xdoodle.xyz/cdn/down/0a31bd429bfcfb29922cc3e6f54a5cdb'],

              }
srt_file_dict = { #'banyo_yashahime_201': 'ndoodle.xyz/cdn/down/5d548a1b558d5036878a3523ae9326af',
              #'banyo_yashahime_202': 'catcdn.top/cdn/down/981b73978972e7699529b167e838a557',
              #'banyo_yashahime_203': 'ndoodle.xyz/cdn/down/92af8189e113a54cc43301d2af8dae48',
              'party_people_kongmyeong_001': 'https://crazypatutu.com/subtitles/2022-2/%ED%8C%8C%EB%A6%AC%ED%94%BC%EA%B3%B5%EB%AA%8501.srt',
              'party_people_kongmyeong_002': 'https://crazypatutu.com/subtitles/2022-2/%ED%8C%8C%EB%A6%AC%ED%94%BC%EA%B3%B5%EB%AA%8502.srt',
              'party_people_kongmyeong_003': 'https://crazypatutu.com/subtitles/2022-2/%ED%8C%8C%EB%A6%AC%ED%94%BC%EA%B3%B5%EB%AA%8503.srt',
              'party_people_kongmyeong_004': 'https://crazypatutu.com/subtitles/2022-2/%ED%8C%8C%EB%A6%AC%ED%94%BC%EA%B3%B5%EB%AA%8504.srt',
              'party_people_kongmyeong_005': 'https://crazypatutu.com/subtitles/2022-2/%ED%8C%8C%EB%A6%AC%ED%94%BC%EA%B3%B5%EB%AA%8505.srt',
              'party_people_kongmyeong_006': 'https://crazypatutu.com/subtitles/2022-2/%ED%8C%8C%EB%A6%AC%ED%94%BC%EA%B3%B5%EB%AA%8506.srt',
              'party_people_kongmyeong_007': 'https://crazypatutu.com/subtitles/2022-2/%ED%8C%8C%EB%A6%AC%ED%94%BC%EA%B3%B5%EB%AA%8507.srt',
              'party_people_kongmyeong_008': 'https://crazypatutu.com/subtitles/2022-2/%ED%8C%8C%EB%A6%AC%ED%94%BC%EA%B3%B5%EB%AA%8508.srt',
              'party_people_kongmyeong_009': 'https://crazypatutu.com/subtitles/2022-2/%ED%8C%8C%EB%A6%AC%ED%94%BC%EA%B3%B5%EB%AA%8509.srt',
              'party_people_kongmyeong_010': 'https://crazypatutu.com/subtitles/2022-2/%ED%8C%8C%EB%A6%AC%ED%94%BC%EA%B3%B5%EB%AA%8510.srt',
              'party_people_kongmyeong_011': 'https://crazypatutu.com/subtitles/2022-2/%ED%8C%8C%EB%A6%AC%ED%94%BC%EA%B3%B5%EB%AA%8511.srt',
              'party_people_kongmyeong_012': 'https://crazypatutu.com/subtitles/2022-2/%ED%8C%8C%EB%A6%AC%ED%94%BC%EA%B3%B5%EB%AA%8512.srt'
              }



# path = 'F:/stream_download'
# download_url = make_download_url(338)
# for url in download_url:
#     download_file(path,url)
#     print(url, requests.get(url, stream=True))

# url = "https://ndoodle.xyz/subtitles/2021-4/반요야샤2기22ns.srt"
# download_file(path,url)
def main ():
    path_root = 'F:/stream_download'
    # path =  'F:/stream_download'
    "Download script files"
    for i, key in enumerate(srt_file_dict.keys()):
        # key = list(mp4_file_dict.keys())[0]
        path_root_download = os.path.join(path_root, key)
        os.makedirs(path_root_download, exist_ok=True)
        fpath_download = download_file(path_root_download, srt_file_dict[key], manual_file_name=key)
        print('srt',i, '/', len(srt_file_dict.keys()) ,fpath_download)
    "Download video files"
    for key in mp4_file_dict.keys():
        # key = list(mp4_file_dict.keys())[1]
        # print(key)
        # print(key, mp4_file_dict[key])

        path_root_download = os.path.join(path_root ,key)
        os.makedirs(path_root_download, exist_ok=True)

        download_url = make_download_url(1000, mp4_file_dict[key][2],orbit_num= mp4_file_dict[key][0], init_num = mp4_file_dict[key][1])
        # for url in download_url:
        #     print(key,url)
        #     file_name = download_file(path, url)
        down_flag = True
        i = 0
        while (i <= len(download_url)):
            try:

                url = download_url[i]
                fpath_download = download_file(path_root_download, url)
                time.sleep(0.1)
                try:
                    if os.path.getsize(fpath_download) < 10000:

                        print('Fail to donwlaod', key, mp4_file_dict[key], i, fpath_download)
                        os.remove(fpath_download)
                    else:
                        print('Success to donwlaod',key,mp4_file_dict[key],i, fpath_download)
                except:
                    print('Fail to donwlaod', key, mp4_file_dict[key], i, fpath_download)

            except Exception as e:
                print(e)
                print('Fail to donwlaod',key, mp4_file_dict[key], i ,'/', len(download_url))
            i += 1


def main2 ():
    path_root = 'F:/stream_download'
    "Download script files"

    "Download video files"
    for key in mp4_file_dict.keys():

        path_root_download = os.path.join(path_root ,key)
        os.makedirs(path_root_download, exist_ok=True)

        combine_videos_folder_to_one(path_root_download, key)
def main3 ():
    path_root = 'F:/stream_download'
    for key in mp4_file_dict.keys():
        # key = list(mp4_file_dict.keys())[0]
        # print(key)
        # print(key, mp4_file_dict[key])

        path_root_download = os.path.join(path_root, key)
        os.makedirs(path_root_download, exist_ok=True)

        download_url = make_download_url(1000, mp4_file_dict[key][1], init_num=mp4_file_dict[key][0])

        target_video_fpath_lst = [ f.split('/')[-1].replace('\\','/') for f in download_url]
        # target_video_fpath_lst[0]
        downloaded_video_fpath_lst = glob.glob(os.path.join(path_root_download) + '/*.mp4')
        downloaded_video_fpath_lst = [f.replace('\\','/').replace('aaa.mp4','.aaa').split('/')[-1]         for f in  downloaded_video_fpath_lst]
        # downloaded_video_fpath_lst[0]
        redownload_video_fpath_lst = download_url.copy()
        redownload_video_fpath_lst[0]
        downloaded_video_fpath_lst[0]
        for i ,fpath_down in enumerate(downloaded_video_fpath_lst):
            for j, fpath_redown in enumerate(downloaded_video_fpath_lst):
                try:
                    if redownload_video_fpath_lst[j].find(downloaded_video_fpath_lst[i])>=0:
                       redownload_video_fpath_lst.remove(redownload_video_fpath_lst[j])
                    else:
                        pass
                except:
                    pass
        redownload_video_fpath_lst
        down_flag = True
        i = 0
        while (down_flag):
            try:

                url = redownload_video_fpath_lst[i]
                fpath_download = download_file(path_root_download, url)
                time.sleep(0.1)
                if os.path.getsize(fpath_download) < 1000:
                    down_flag = False
                    os.remove(fpath_download)
                else:
                    pass

                print('Success to downlaod', key, mp4_file_dict[key], i, fpath_download)
            except Exception as e:
                print(e)
                print('Fail to downlaod', key, mp4_file_dict[key], i)
            i += 1

def Check_download(path_root = 'F:/stream_download',folder_name = 'party_people_kongmyeong_007'):
    try:

        file_lst = glob.glob(path_root + '/' + folder_name +'/*.mp4')
        file_lst.sort()
        check_flag =   ( len(file_lst) == (int(file_lst[-1].replace('\\','/').split('/')[-1].split('.')[0].split('_')[-1][:3])+1))
        print(check_flag, folder_name)
    except Exception as e:
        check_flag = 'error'
        print(e)

    return check_flag


if __name__ == '__main__':
    # 007,008,009,10,12 fail
    main()
    Check_download(path_root='F:/stream_download', folder_name='party_people_kongmyeong_012')