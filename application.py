from flask import Flask, render_template, request
from numpy.polynomial.polynomial import polyfit
import numpy as np
import os
import subprocess
import pendulum
import csv

# Flask setup
app = Flask(__name__)
app.config['SECRET_KEY'] = "DefaultSecret"

@app.route("/")
def sleepschedule():
    out = get_times()
    return render_template("sleepschedule.html", times=out[0], average=out[1], slope=out[2])

def get_times():
    if is_production():
        file = "/home/sleepschedule/mysite/times.csv"
    else:
        file = "times.csv"

    with open(file, "r") as f:
        r = csv.reader(f)
        times = []
        for line in r:
            times.append(line[0])

    # Remove impair value if present
    if len(times) % 2 != 0:
        times = times[:len(times)-1]

    nights = []
    mornings = []
    for i, t in enumerate(times):
        if i % 2 == 0:
            nights.append(pendulum.from_format(t, "YYYY/MM/DD HH:mm:ss", tz="America/Toronto"))
        else:
            mornings.append(pendulum.from_format(t, "YYYY/MM/DD HH:mm:ss", tz="America/Toronto"))

    sleeps = []
    for i in range(len(mornings)):
        sleep_mins = nights[i].diff(mornings[i]).in_minutes()
        sleep_hours = nights[i].diff(mornings[i]).in_hours()

        extra_mins = sleep_mins - sleep_hours * 60
        formatted_sleep_time = f"{sleep_hours} hours {extra_mins} mins"

        sleeps.append([mornings[i].format("YYYY/MM/DD"), nights[i].format("YYYY/MM/DD HH:mm:ss"), mornings[i].format("YYYY/MM/DD HH:mm:ss"), sleep_mins, formatted_sleep_time])

    # Get 5 day average sleep time
    total = 0
    for i in range(-1, -5, -1):
        total += sleeps[i][3]
    average = pendulum.duration(minutes=total // 5).in_words()


    # Line of best fit
    x = np.arange(len(sleeps))
    y = [s[3] for s in sleeps]
    b, m = polyfit(x, y, 1)

    y = m * x + b

    sleeps = [sleeps[i] + [y[i]] for i in range(len(sleeps))]
    slope = int(m)
    if slope >= 0:
        slope = "+" + str(slope)
    else:
        slope = str(slope)
    return [sleeps, average, slope]

@app.route("/add", methods=["POST"])
def add():
    if is_production():
        file = "/home/sleepschedule/mysite/times.csv"
    else:
        file = "times.csv"
    with open(file, "a") as f:
        w = csv.writer(f)
        w.writerow([pendulum.now("America/Toronto").format("YYYY/MM/DD HH:mm:ss")])
    return "Success"

# Check if in production
def is_production():
    root_url = request.url_root
    developer_url = 'http://127.0.0.1:5000/'
    return root_url != developer_url

# Run Flask if file is interpreted
if __name__ == "__main__":
    os.environ["FLASK_APP"] = "application.py"

    try:
        current = subprocess.check_output(["lsof", "-t", "-i:5000"])
        current = max(current.decode("utf-8").split("\n"))
        print(f"kill {current}")
        os.system(f"kill {current}")
    except:
        pass
    os.system("flask run")
