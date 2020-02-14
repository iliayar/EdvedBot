#!/usr/bin/python

import os
import threading
import datetime
import sqlite3
import telegram
import logging
from telegram.ext import Updater, CommandHandler

from getImage import getImage


REQUEST_KWARGS = {
    'proxy_url':'socks5://127.0.0.1:9050',
    'urllib3_proxy_kwargs':{}
}

TOKEN = os.environ.get("TOKEN")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)



updater = Updater(token=TOKEN, request_kwargs=REQUEST_KWARGS)



def sched_event():

    now = datetime.datetime.now()
    if(now.minute == 0 ):
        conn = sqlite3.connect('eded.db')

        c = conn.cursor()

        for row in c.execute('SELECT * FROM users'):
            try:
                updater.bot.send_photo(row[0], photo=getImage())
            except:
                delete_user(row[0],c)
        conn.commit()
        conn.close()
    t = threading.Timer(60, sched_event)
    t.start()

def start(bot,update):
    bot.send_message(chat_id=update.message.chat_id,text='Your\'e now subscribed on EDED')
    bot.send_photo(chat_id=update.message.chat_id,photo=open('./img.png','rb'))

    conn = sqlite3.connect('eded.db')

    c = conn.cursor()
    try:
        c.execute('INSERT INTO users(id) VALUES (?)', (update.effective_user.id,) )
        print ('User join: ' + update.effective_user.username)
    except:
        pass

    conn.commit()
    conn.close()

def delete_user(user_id, c):
    c.execute('DELETE FROM users WHERE id='+ str(user_id))

def stop(bot,update):
    conn = sqlite3.connect('eded.db')

    c = conn.cursor()
    delete_user(update.effective_user.id, c)

    conn.commit()
    conn.close()

def interval_msg(bot,update):
    try :
        pass
    except:
        pass



stop_handler = CommandHandler('stop', stop)
start_handler = CommandHandler('start',start)
updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(stop_handler)

updater.start_polling()

t = threading.Timer(1,sched_event)
t.start()
