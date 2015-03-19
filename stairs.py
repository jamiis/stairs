from pymongo import MongoClient
from datetime import datetime

conn = MongoClient()
db = conn.stairs.stairs

def get_seconds(mod):
    msg = "how {0}? (fmt: X:XX)".format(mod)
    mins,secs = raw_input(msg).split(":")
    return float(mins)*60 + float(secs)

if __name__ == "__main__":
    run = {
        "date": None,
        "sets": [],
        "breaks": [],
    }

    # date and time of run
    run_time = datetime.now()
    hour, minute = raw_input("what time was your run? (fmt: 23:59)").split(":")
    run_time = run_time.replace(hour=int(hour), minute=int(minute))
    if raw_input("was your run today? [y/n]") == "n":
        day = int(raw_input("what day was your run? (fmt: 31)"))
        run_time = run_time.replace(day=day)
    run["date"] = run_time

    # sets, length and time
    set_ = 1
    while True:
        run["sets"].append({
            "flights": int(raw_input("how many flights on set {0}?".format(set_))),
            "time": get_seconds("fast"),
        })
        if raw_input("more sets? [y/n]") == "n":
            break
        set_ += 1

    # breaks, time
    break_ = 1
    while True:
        print "break: {0}".format(break_)
        run["breaks"].append({
            "time": get_seconds("long"),
        })
        if raw_input("more breaks? [y/n]") == "n":
            break
        break_ += 1

    print run
    if raw_input("look okay?") == "n":
        print "dammit! start over amigo"
    else:
        db.insert(run)    
        print "wow! run such hard!"

    conn.close()
