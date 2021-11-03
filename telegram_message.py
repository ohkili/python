

# telegram token
# Use this token to access the HTTP API:
# 2062294044:AAEzrGGPlV7C2C-9ZQ9Ji9QbTm7DoG8NgWw
# You will find it at t.me/tele_kili_bot.
# https://api.telegram.org/bot2062294044:AAEzrGGPlV7C2C-9ZQ9Ji9QbTm7DoG8NgWw/getUpdates
{"ok":true,"result":[{"update_id":337864501,
"message":{"message_id":3,"from":{"id":1926421781,"is_bot":false,"first_name":"ok","last_name":"kwon","language_code":"ko"},"chat":{"id":1926421781,"first_name":"ok","last_name":"kwon","type":"private"},"date":1635692289,"text":"/start","entities":[{"offset":0,"length":6,"type":"bot_command"}]}}]}
# https://api.telegram.org/bot2062294044:AAEzrGGPlV7C2C-9ZQ9Ji9QbTm7DoG8NgWw/sendMessage?chat_id=1926421781&text=hello

import telegram
import os
import glob
telegram_token = "2062294044:AAEzrGGPlV7C2C-9ZQ9Ji9QbTm7DoG8NgWw"

telegram_chat_id = 1926421781

bot = telegram.Bot(token=telegram_token)

# text 보내기
bot.sendMessage(chat_id=telegram_chat_id, text='hello world')
# image 보내기 image url
photo_url ="https://telegram.org/img/t_logo.png"
bot.sendPhoto(chat_id=telegram_chat_id, photo = photo_url, caption = 'telegrm logo')
# hyperlink 보내기
# 미리보기 기능 off ==>  disable_web_page_preview= True
# []안에 문자는 제목으로 전송되고, ()안에 hyperlink 넣어주면 됨
bot.send_message(chat_id=telegram_chat_id, text="[naver 증권](https://finance.naver.com)",parse_mode='Markdown', disable_web_page_preview= False)

# image 보내기 image file
os.getcwd()
glob.glob('E:\\python\\' + '*.jpg')
photo_file = 'E:\\python\\주행기록.jpg'
bot.sendPhoto(chat_id=telegram_chat_id, photo = open(photo_file,'rb'), caption = '카니발 주행기록')

def telegram_message(content ='Hello world', content_type = 'text', description = 'description'  ):
    telegram_token = "2062294044:AAEzrGGPlV7C2C-9ZQ9Ji9QbTm7DoG8NgWw"
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
        bot.sendPhoto(chat_id=telegram_chat_id, photo=open(content, 'rb'),  caption=description)
    elif content_type == 'hyperlink':
        # []안에 문자는 제목으로 전송되고, ()안에 hyperlink 넣어주면 됨
        #  example is "[naver 증권](https://finance.naver.com)"
        content_hyperlink =  "[" + description + "](" + content + ")"
        bot.send_message(chat_id=telegram_chat_id, text= content_hyperlink, parse_mode='Markdown', disable_web_page_preview=False)
    else :
        print('You must choice content_type as text, imgUrl, imgFile, hyperlink')


telegram_message()