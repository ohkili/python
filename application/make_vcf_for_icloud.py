import time
import os
import pandas as pd
import chardet



def make_contact_info(name,phone_number, note):

    yymmdd = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    hhmmss = time.strftime('%I:%M:%S', time.localtime(time.time()))
    str1 = "BEGIN:VCARD" + '\n'
    str2 = "VERSION:3.0"+ '\n'
    str3 = "PRODID:-//Apple Inc.//iOS 14.6//EN"+ '\n'
    str4 = "N:;" + name + ";;;" + '\n'
    str5 = "FN:" + name  + '\n'
    str6 = "NICKNAME:" + '\n'
    str7 = "TEL;type=CELL;type=VOICE;type=pref:"  + phone_number +    '\n'
    str8 = "NOTE:" +  note + '\n'
    str9 = "REV:" + yymmdd + "T" + hhmmss + "Z" + '\n'
    str10 = "END:VCARD" + '\n'

    str_list = [str1,str2,str3,str4,str5,str6,str7,str8,str9,str10]

    return str_list

"download tel number file"
"make vcf"
"each vcf merging"
"upload vcf file"

inputfilepath = 'V:/정보/골함사/골함사명부_2023.xlsx'
outputiflepath = 'V:/정보/골함사/contacts.vcf'
df = pd.read_excel(inputfilepath)

if __name__ == '__main__':

    with open(outputiflepath, 'w+',encoding='utf-8') as vcf_file:
        for i in range(len(df)):
            name = df.loc[i]['성명'] + '_' + df.loc[i]['그룹명']
            phone_number = df.loc[i]['전화번호'].replace('-','')
            note = df.loc[i]['그룹명']
            str_list = make_contact_info(name,phone_number,note)
            vcf_file.writelines(str_list)

        vcf_file.close()
else:
    pass


"""
BEGIN:VCARD
VERSION:3.0
PRODID:-//Apple Inc.//iOS 14.6//EN
N:;서철모/68/시범호반;;;
FN:서철모/68/시범호반
item1.TEL;type=pref:010-4163-2240
NOTE:골프를 함께하는 사람들(동탄2)
REV:2020-11-24T23:27:53Z
END:VCARD

import vcf
path = "V:/정보/골함사/iCloud vCards (10).vcf"
rawdata = open(path, 'rb').read()
result = chardet.detect(rawdata)
enc = result['encoding']
"""