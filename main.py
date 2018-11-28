import configparser
import logging
from telegram.ext import Updater, CommandHandler
from telegram import UserProfilePhotos, File, ChatAction, ParseMode
from functools import wraps
from time import sleep
from PIL import Image
from shutil import copyfile
import os
welcome_message = '''
🍉🍉🍉🍉🍉🍉🍉🍉🍉🍉🍉🍉🍉 \n 
🌹 سلام \n \n \n✳️این ربات با همکاری امیرحسین گودرزی به عنوان برنامه نویس و امین خلیقی به عنوان گرافیست و به منظور احیای شب یلدا و بهتر شدن حال هممون برای یه مدت زمانی طراحی شده.

✳️ فقط کافیه که منتظر بمونین تا عکس پروفایل یلدایی خودتون توسط ربات آماده بشه و از اون توی شبکه‌های اجتماعی مختلف استفاده کنین.

✳️ همچنین این ربات متن باز بوده و سورس کد اون از طریق 🖥 [این لینک](https://github.com/numb95/yaldasho-bot) 🖥 در اختیار همه قرار داره.

✳️ ما رو به دوستاتون معرفی کنید: [یلدایی شو](https://t.me/yaldasho_bot)

'''

wait_message = '''
⭐️تصویر نمایه شما آماده شده است. ربات در حال ارسال آن به شماست.⭐️
'''


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(*args, **kwargs):
            bot, update = args
            bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(bot, update, **kwargs)
        return command_func
    
    return decorator


def image_merge(profile_picture):
    im = Image.open(profile_picture, 'r')
    size = 640, 640
    thumbnail = im.resize(size)
    yalda = Image.open('assets/yalda.png', 'r')
    thumbnail.paste(yalda, (0,0), yalda)
    thumbnail.save(profile_picture, "JPEG")

@send_action(ChatAction.UPLOAD_PHOTO)
def start(bot , update):
    bot.send_message(chat_id=update.message.chat_id, text= welcome_message,  parse_mode=ParseMode.MARKDOWN)
    profile_picture_id = bot.getUserProfilePhotos(update.message.chat_id, 0).photos[0][-1].file_id
    user_id = update.message.chat_id
    user_name = update.message.chat.username
    done_date = update.message.date
    profile_picture_file = bot.get_file(profile_picture_id)
    profile_picture_file.download('images/original/{}_@{}_{}_original.jpg'.format(done_date,user_id,user_name))
    copyfile('images/original/{}_@{}_{}_original.jpg'.format(done_date,user_id,user_name), 'images/edited/{}_@{}_{}_edited.jpg'.format(done_date,user_id,user_name))
    image_merge('images/edited/{}_@{}_{}_edited.jpg'.format(done_date,user_id,user_name))
    bot.send_message(chat_id=update.message.chat_id, text=wait_message)
    bot.send_photo(chat_id= update.message.chat_id, photo=open('images/edited/{}_@{}_{}_edited.jpg'.format(done_date,user_id,user_name), 'rb'))
    os.remove('images/edited/{}_@{}_{}_edited.jpg'.format(done_date,user_id,user_name))
    os.remove('images/original/{}_@{}_{}_original.jpg'.format(done_date,user_id,user_name))
def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(name)s - %(message)s', level=logging.INFO)
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config['app-conf']['token']
    updater = Updater(token=token)
    start_handler = CommandHandler ('start',start)
    updater.dispatcher.add_handler(start_handler)
    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()


