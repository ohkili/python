
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

import requests
import time
from moviepy.editor import *
import os
from natsort import natsorted

#

# url = "https://cdn7-ndoodle.xyz/cdn/down/5d548a1b558d5036878a3523ae9326af/Video/720p/720p_261.aaa"
#
# url = "https://ndoodle.xyz/subtitles/2021-4/반요야샤2기01.srt"
# https://ndoodle.xyz/subtitles/2021-4/반요야샤2기02.srt
# # download_file(path,url)
# # https://cdn15-ndoodle.xyz/cdn/down/5d548a1b558d5036878a3523ae9326af/Video/360p/360p_014.aaa
# # https://cdn12-ndoodle.xyz/cdn/down/5d548a1b558d5036878a3523ae9326af/Video/720p/720p_131.aaa

"https://cdn1-catcdn.top/cdn/down/981b73978972e7699529b167e838a557/Video/720p/720p_015.aaa"
# num = 131
# num_pad = str(num).zfill(3)
# orbit = num % 15 +1
# https_form = "https://cdn" + str(orbit) + "-ndoodle.xyz/cdn/down/5d548a1b558d5036878a3523ae9326af/Video/720p/720p_" + num_pad + ".aaa"
"https://ndoodle.xyz/subtitles/2021-4/반요야샤2기22ns.srt"




def make_download_url(num, middle_form):
    download_url = []
    for i in range(num):
        num_pad = str(i).zfill(3)
        orbit = i % 15 + 1
        https_form = "https://cdn" + str(
            orbit) + "-"   +middle_form + "/Video/720p/720p_" + num_pad + ".aaa"
        download_url.append(https_form)
    return download_url

def download_file(path,url):
    if url.split('.')[-1] == 'srt':
        local_filename = path + '/' + url.split('/')[-1]
    else:
        local_filename = path + '/' + url.split('/')[-1].replace('.','') + '.mp4'

    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    print(r)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=256):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    time.sleep(0.5)

    return local_filename

#
path = 'F:/stream_download'
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

file_dict = { #'banyo_yashahime_201': 'ndoodle.xyz/cdn/down/5d548a1b558d5036878a3523ae9326af',
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

# path = 'F:/stream_download'
# download_url = make_download_url(338)
# for url in download_url:
#     download_file(path,url)
#     print(url, requests.get(url, stream=True))

# url = "https://ndoodle.xyz/subtitles/2021-4/반요야샤2기22ns.srt"
# download_file(path,url)

for key in file_dict.keys():
    # key = list(file_dict.keys())[0]
    # print(key)
    # print(key, file_dict[key])

    path = 'F:/stream_download' + '/' + key
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)

    download_url = make_download_url(1000, file_dict[key])
    # for url in download_url:
    #     print(key,url)
    #     file_name = download_file(path, url)
    down_flag = True
    i = 0
    while (down_flag):
        url = download_url[i]
        file_name = download_file(path, url)
        if os.path.getsize(file_name) <1000:
            down_flag = False
            os.remove(file_name)
        else:
            pass
        i +=1
        print(key,file_dict[key],i, file_name)

# os.path.getsize('F:/stream_download/720p_000.aaa.mp4')
# import glob
# file_ls =glob.glob('F:/stream_download/' +'*.srt')
#
# for file in file_ls:
#     os.rename(file, file.replace('반요야샤2기','banyo_yashahime_2'))