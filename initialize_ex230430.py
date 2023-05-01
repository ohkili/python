import uuid
import re
import os
import telegram
import datetime

# REST_API_KEY and refresh_token is borrow
REST_API_KEY ='22644bd965c28d381ea875a9dde9e2d1'
refresh_token = '2hZcRLD01s1Rl0qEA0BhnenFH1om0rtTNimYSgo9cuoAAAF81jvBOA'


def Telegram_message(content='Hello world', content_type='text', description='description'):
    telegram_token = "5011897744:AAFvwnQrdllp09gz2Iy_XD6SONWy1-jQuNM"
    telegram_chat_id = 1926421781
    bot = telegram.Bot(token=telegram_token)


    # Bottom is telegram bot manual
    """ 
    # text 보내기
    bot.sendMessage(chat_id=telegram_chat_id, text='hello world')
    # image 보내기 image url
    photo_url = "https://telegram.org/img/t_logo.png"
    bot.sendPhoto(chat_id=telegram_chat_id, photo=photo_url, caption='telegrm logo')
    # hyperlink 보내기
    # 미리보기 기능 off ==>  disable_web_page_preview= True
    # []안에 문자는 제목으로 전송되고, ()안에 hyperlink 넣어주면 됨
    bot.send_message(chat_id=telegram_chat_id, text="[naver 증권](https://finance.naver.com)", parse_mode='Markdown',
                     disable_web_page_preview=False)

    # image 보내기 image file
    # os.getcwd()
    # glob.glob('E:\\python\\' + '*.jpg')
    photo_file = 'E:\\python\\주행기록.jpg'
    bot.sendPhoto(chat_id=telegram_chat_id, photo=open(photo_file, 'rb'), caption='카니발 주행기록') 
    """

    if content_type == 'text':
        # example is 'hello world'
        bot.sendMessage(chat_id=telegram_chat_id, text=content)
    elif content_type == 'imgUrl':
        # example is  "https://telegram.org/img/t_logo.png"
        bot.sendPhoto(chat_id=telegram_chat_id, photo=content, caption=description)
    elif content_type == 'imgFile':
        # example is 'E:\\python\\주행기록.jpg'
        bot.sendPhoto(chat_id=telegram_chat_id, photo=open(content, 'rb'), caption=description)
    elif content_type == 'hyperlink':
        # []안에 문자는 제목으로 전송되고, ()안에 hyperlink 넣어주면 됨
        #  example is "[naver 증권](https://finance.naver.com)"
        content_hyperlink = "[" + description + "](" + content + ")"
        bot.send_message(chat_id=telegram_chat_id, text=content_hyperlink, parse_mode='Markdown',
                         disable_web_page_preview=False)
    else:
        print('You must choice content_type as text, imgUrl, imgFile, hyperlink')

def Timer(end_time = '2023-04-20'):
    date_now = datetime.datetime.now().strftime('%Y-%m-%d')
    if date_now <= end_time:
        time_flag = True
    else:
        time_flag = False
    return time_flag

def Find_macaddress(folder_name):
    mac_address = ''.join(re.findall('..', '%012x' % uuid.getnode())).upper()
    # print(mac_address)
    os.makedirs(folder_name, exist_ok=True)
    computer_name = os.environ['COMPUTERNAME']

    return mac_address


def Set_codebook():
    enc_dict = {"A": "01", "B": "02", "C": "03", "D": "04", "E": "05", "F": "06", "G": "07", "H": "08", "I": "09",
                 "J": "10", "K": "11",
                 "L": "12", "M": "13", "N": "14", "O": "15", "P": "16", "Q": "17", "R": "18", "S": "19", "T": "20",
                 "U": "21", "V": "22",
                 "W": "23", "X": "24", "Y": "25", "Z": "26",
                 "0": "90", "1": "91", "2": "92", "3": "93", "4": "94", "5": "95", "6": "96", "7": "97", "8": "98",
                 "9": "99"
                 }
    dec_dict = {}
    for key in enc_dict.keys():
        dec_dict[enc_dict[key]] = key

    return enc_dict, dec_dict

def encrypt(msg, enc_dict, option = 'shift'):

    enc_book = []
    for s in msg:
        enc_book.append(enc_dict[s])
    msg_encrypt = ''.join(enc_book)
    return msg_encrypt

def decrypt(msg, dec_dict,option = 'shift'):
    dec_book = []
    msg_ls = []

    while (len(msg)):
        word = msg[:2]
        msg_ls.append(word)
        msg = msg[2:]

    for s in msg_ls:
        dec_book.append(dec_dict[s])

    msg_decrypt = ''.join(dec_book)
    return msg_decrypt


if __name__ == '__main__':


    root_folder = 'C:/project_estimate_from_dwg'
    folder_list = [root_folder,
                   os.path.join(root_folder, 'caddwg_final_csv'),
                   os.path.join(root_folder, 'caddwg_original_folder'),
                   os.path.join(root_folder, 'caddwg_temp_csv'),
                   os.path.join(root_folder, 'script_file'),
                   ]
    computer_name = os.environ['COMPUTERNAME']
    i = 0
    for folder in folder_list:
        os.makedirs(folder, exist_ok=True)
        message = str(i)+ ') '+ 'Folder is made: ' + folder + ' from '+ computer_name + ' at ' + datetime.datetime.now().strftime('%Y-%m-%d')
        message = message.replace('\\','/')
        if Timer():
            Telegram_message(content= message, content_type='text', description='description')
        else:
            pass
        i +=1
    mac_address = Find_macaddress(root_folder)

    enc_dict, _ = Set_codebook()
    serial_key = encrypt(mac_address,enc_dict)
    if Timer():
        message_macaddress = (
            str(i)+ ') ' + mac_address + ' from ' + computer_name + ' at ' + datetime.datetime.now().strftime('%Y-%m-%d'))
        Telegram_message(content=message_macaddress, content_type='text', description='description')
        i +=1
        message_serial_key = (
            str(i) + ')' + serial_key + ' from ' + computer_name + ' at ' + datetime.datetime.now().strftime('%Y-%m-%d'))
        Telegram_message(content=message_serial_key, content_type='text', description='description')
    else:
        pass
    with open(os.path.join(root_folder, "serial_key.txt"), 'w') as file:
        file.write('')



