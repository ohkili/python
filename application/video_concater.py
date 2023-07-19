
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
import math

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
                print(filePath)

    final_clip = concatenate_videoclips(L)
    final_clip.to_videofile(os.path.join(folder_path,filename +".mp4"), fps=60, remove_temp=False)
#


"""
ex) filename is  'banyo_yashahime_201'
    foldername is  'banyo_yashahime_201'
"""
def main():
    path_root = 'F:\stream_download/'


    mp4_file_dict = {
         # 'party_people_kongmyeong_001': [13,3,'xdoodle.xyz/cdn/down/ead9853a64c5e34f323f5a0c6a51571e'],
         # 'party_people_kongmyeong_002': [13,3,'xdoodle.xyz/cdn/down/e83bb7b0da390abc1e2fcba261a7b787'],
         # 'party_people_kongmyeong_003': [13,3,''],
         # 'party_people_kongmyeong_004': [13,3,''],
         'party_people_kongmyeong_005': [13,3,'xdoodle.xyz/cdn/down/256fea8d6668715b850295fc1d04c200'],
         'party_people_kongmyeong_006': [15,1,'ndoodle.xyz/cdn/down/21dbba6f80379130d90c09fd5933af15'],
         'party_people_kongmyeong_007': [15,1,'ndoodle.xyz/cdn/down/21dbba6f80379130d90c09fd5933af15'],
         'party_people_kongmyeong_008': [15,1,'ndoodle.xyz/cdn/down/21dbba6f80379130d90c09fd5933af15'],
         'party_people_kongmyeong_009': [15,1,'ndoodle.xyz/cdn/down/21dbba6f80379130d90c09fd5933af15'],
         'party_people_kongmyeong_010': [15,1,'ndoodle.xyz/cdn/down/21dbba6f80379130d90c09fd5933af15'],
         'party_people_kongmyeong_011': [15,1,'ndoodle.xyz/cdn/down/21dbba6f80379130d90c09fd5933af15'],
         'party_people_kongmyeong_012': [15,1,'ndoodle.xyz/cdn/down/82f4a521864268f9999bf387b7eff9a9']
    }


    for key in mp4_file_dict.keys():
        folder_path = os.path.join(path_root, key)  # 'F:\stream_download'
        filename = key
        fpath_mp4 = os.path.join(folder_path, key + '.mp4')
        if os.path.exists(fpath_mp4):
            print('This file was already been.: ',fpath_mp4)
        else:
            print(folder_path,key)
            combine_videos_folder_to_one(folder_path, filename)
if __name__ == '__main__':
    main()
