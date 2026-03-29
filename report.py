import psutil
import time
import json
from datetime import datetime



funcs = {}

def charkt(name=None):
    def decorator(func):
        funcs[name] = func
        return func
    return decorator

@charkt(name = "TIME")
def TIME_scanner():

    now = datetime.now()
    return{
            "date": now.strftime("%d.%m"),
            "time": now.strftime("%H.%M.%S")
    }
@charkt(name="CPU")
def CPU_scanner():
    usage = psutil.cpu_percent(interval=1)
    return {"percentage":usage}

@charkt(name="MEM")
def MEM_scanner():
    MEM = psutil.virtual_memory()
    return {"percentage": MEM.percent}

@charkt(name="NWS")
def NWS_scanner():
    # Получаем начальные показания
    start = psutil.net_io_counters()
    time.sleep(1) 
    # Получаем конечные показания
    end = psutil.net_io_counters()
    
    # Правильно вычисляем разницу в байтах (конечное - начальное)
    bytes_recv = end.bytes_recv - start.bytes_recv
    bytes_sent = end.bytes_sent - start.bytes_sent
    
    # Переводим в Мбит/с (байты * 8 / 1_000_000)
    download_mbps = (bytes_recv * 8) / 1_000_000
    upload_mbps = (bytes_sent * 8) / 1_000_000
    
    with open('config.json', 'r', encoding='utf-8') as f:
        conf = json.load(f)

    # Защита от отрицательных значений (на случай, если счетчики сбросились)
    download_mbps = max(0, download_mbps)
    upload_mbps = max(0, upload_mbps)
    
    # Получаем максимальные скорости
    max_download = conf["scan"].get("max_download_spid", 100)
    max_upload = conf["scan"].get("max_upload_spid", 100)
    
    # Вычисляем проценты, ограничиваем 100%
    download_percent = min((download_mbps / max_download * 100), 100)
    upload_percent = min((upload_mbps / max_upload * 100), 100)
    
    return {
        "download_percent": round(download_percent, 1),
        "upload_percent": round(upload_percent, 1)
    }

def report():
    with open('config.json', 'r', encoding='utf-8') as f:
        conf = json.load(f)
    limits = conf["limits"]
    report_dict = {}
    for c in funcs.keys():
        report_dict[c] = {}
        report_dict[c]["rep"] = funcs[c]()
        report_dict[c]["lim"] = limits[c] if c in limits.keys() else {}
    return report_dict
