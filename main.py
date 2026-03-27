#библиотеки
import threading
import json
#СВОи файлы
import report 
import bot

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

errors_flag = 0
def alarm(rep):
    global errors_flag
    if errors_flag <= 0:
        print(rep)
        bot.alarm(rep)
        
        errors_flag = config["scan"]["time_betwin_alarm_m"]
    else:
        errors_flag -=1

checker_thread = threading.Thread(target=report.scaning, daemon=True)
def main(): 
    checker_thread.start()
    bot.run()

if __name__ == "__main__":
    main()
    