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
            "time": now.strftime("%H.%M")
    }
@charkt(name="CPU")
def CPU_scanner():
    usage = psutil.cpu_percent(interval=1)
    return {"percentage used":usage}

@charkt(name="MEM")
def MEM_scanner():
    MEM = psutil.virtual_memory()
    return {
        "total": round(MEM.total / (1024 ** 3), 2),
        "available": round(MEM.available / (1024 ** 3), 2),
        "used": round(MEM.used / (1024 ** 3), 2),
        "percentage used": MEM.percent
    }


def report():
    with open('limits.json', 'r', encoding='utf-8') as f:
        limits = json.load(f)
    report_dict = {}
    for c in funcs.keys():
        report_dict[c] = {}
        report_dict[c]["rep"] = funcs[c]()
        report_dict[c]["lim"] = limits[c] if c in limits.keys() else {}
    return report_dict



def scaning():
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    while True:
        flag = False
        rep = report()
        for c in rep.keys():
            c_rep = rep[c]["rep"]
            c_lim = rep[c]["lim"]
            for k in c_lim.keys():
                if c_rep[k]>=c_lim[k]:
                    flag = True
        if flag:
            import main
            main.alarm(rep)            
        time.sleep(config["time_between_scans"])




