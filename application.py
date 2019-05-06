from flask_ask_sdk.skill_adapter import SkillAdapter
from ask_sdk_core.skill_builder import SkillBuilder
from flask import Flask, render_template, request
from numpy.polynomial.polynomial import polyfit
from utils import get_sleeps
import numpy as np
import subprocess
import pendulum
import csv
import os

# Flask setup
app = Flask(__name__)
skill_builder = SkillBuilder()
app.config['SECRET_KEY'] = "DefaultSecret"

skill_adapter = SkillAdapter(
    skill=skill_builder.create(), skill_id="amzn1.ask.skill.b134fcc6-c7e1-47f6-a1ac-46b2216f665a", app=app)

@app.route("/")
def sleepschedule():
    out = get_times()
    return render_template("sleepschedule.html", times=out[0], average=out[1], slope=out[2])

@app.route("/log")
def invoke_skill():
    return skill_adapter.dispatch_request()

def get_times():
    # Get sleeps
    if is_production():
        file = "/home/sleepschedule/mysite/times.csv"
    else:
        file = "times.csv"
    sleeps = get_sleeps(file)

    # Get 5 day average sleep time
    total = 0
    for i in range(-1, -6, -1):
        total += sleeps[i][3]
    average = pendulum.duration(minutes=total // 5).in_words()

    averages = []
    for i in range(len(sleeps)):
        count = 5
        total = 0
        for i2 in range(5):
            try:
                total += sleeps[i - i2][3]
            except:
                count -= 1
        d = pendulum.duration(minutes=total // count)
        averages.append(d.hours * 60 + d.minutes)

    sleeps = [sleeps[i] + [averages[i]] for i in range(len(sleeps))]

    # 5 Day line of best fit
    x = np.arange(len(sleeps[-5:]))
    y = [s[3] for s in sleeps[-5:]]
    b, m = polyfit(x, y, 1)
    y = m * x + b

    sleeps = sleeps[:-5] + [sleeps[-5:][i] + [y[i]] for i in range(5)]

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
