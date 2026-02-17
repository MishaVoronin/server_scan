#библиотеки
import telebot
import time
import json
import datetime
#СВОи файлы
import report

#конфиг
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
#бот 
bot = telebot.TeleBot(config["bot"]["token"],threaded=False, skip_pending=True)

#start
@bot.message_handler(commands=["start"])
def start(mess):
    if mess.from_user.id in config["bot"]["admins"]:
        messeg = f"""Привет, это бот для отслеживания состояния сервера. Если какой-то параметр превысит лимит, он отправит сообщение об этом всем админам. Ты можешь посмотреть состояние сервера по команде /report"""
        bot.send_message(mess.from_user.id,messeg)
def rep_w(rep):
    report_str = f""
    for c in rep.keys():
        flag = False
        c_rep = rep[c]["rep"]
        c_lim = rep[c]["lim"]
        for k in c_lim.keys():
            if c_rep[k]>=c_lim[k]:
                flag = True
        report_str += f"{'✅' if not flag else '‼️'}{c}:\n"
        for k in c_rep.keys():
            report_str +=f" {k}:{c_rep[k]}\n"
    return report_str

@bot.message_handler(commands=["report"])
def repot_comand(mess):
    if mess.from_user.id in config["bot"]["admins"]:
        report_list = rep_w(report.report())
        #я допилю красивое отображение
        print(report_list)
        bot.send_message(mess.from_user.id,report_list)

def alarm(rep):
    for admin_id in config["bot"]["admins"]:
        bot.send_message(admin_id,rep_w(rep))
def run():
    print("Bot is running")
    bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)

