from flask import Flask, render_template, request
import os
import subprocess
import pendulum
import csv

# Flask setup
app = Flask(__name__)
app.config['SECRET_KEY'] = "DefaultSecret"

@app.route("/")
def sleepschedule():
    if is_production():
        file = "/home/sleepschedule/mysite/times.csv"
    else:
        file = "times.csv"

    with open(file, "r") as f:
        r = csv.reader(f)
        out = []
        for line in r:
            out.append(line)
    return render_template("sleepschedule.html", times=out)

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
