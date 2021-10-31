

# telegram token
# Use this token to access the HTTP API:
# 2062294044:AAEzrGGPlV7C2C-9ZQ9Ji9QbTm7DoG8NgWw
# You will find it at t.me/tele_kili_bot.
# https://api.telegram.org/bot2062294044:AAEzrGGPlV7C2C-9ZQ9Ji9QbTm7DoG8NgWw/getUpdates
{"ok":true,"result":[{"update_id":337864501,
"message":{"message_id":3,"from":{"id":1926421781,"is_bot":false,"first_name":"ok","last_name":"kwon","language_code":"ko"},"chat":{"id":1926421781,"first_name":"ok","last_name":"kwon","type":"private"},"date":1635692289,"text":"/start","entities":[{"offset":0,"length":6,"type":"bot_command"}]}}]}
# https://api.telegram.org/bot2062294044:AAEzrGGPlV7C2C-9ZQ9Ji9QbTm7DoG8NgWw/sendMessage?chat_id=1926421781&text=hello

import telegram
telegram_token = "2062294044:AAEzrGGPlV7C2C-9ZQ9Ji9QbTm7DoG8NgWw"

telegram_chat_id = 1926421781

bot = telegram.Bot(token=telegram_token)

bot.sendMessage(chat_id=telegram_chat_id, text='hello world')
