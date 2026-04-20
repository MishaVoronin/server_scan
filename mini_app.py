from flask import Flask, render_template
import psutil
import time
import json
from datetime import datetime




def TIME_scanner():

    now = datetime.now()
    return{
            "date": now.strftime("%d.%m"),
            "time": now.strftime("%H.%M.%S")
    }

def NET_scanner():
    start = psutil.net_io_counters()
    time.sleep(1) 
    end = psutil.net_io_counters()
    return {
        "download_byts/s": end.bytes_recv - start.bytes_recv,
        "upload_byts/s"  : end.bytes_sent - start.bytes_sent}

def report():
    with open('config.json', 'r', encoding='utf-8') as f:
        conf = json.load(f)
    rep = {
        "TIME":TIME_scanner(),
        "CPU" :{
            "rep":{"percentage":psutil.cpu_percent(interval=1)},
            "lim":conf["limits"]["CPU"]
        },
        "MEM" :{
            "rep":{"percentage": psutil.virtual_memory().percent},
            "lim":conf["limits"]["MEM"]
        },
        "NET" :{
            "rep":NET_scanner(),
            "lim":conf["limits"]["NET"]
        }
    }




app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/data')
def get_data():
    return report()

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080, debug=False)