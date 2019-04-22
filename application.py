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
    return render_template("sleepschedule.html")

@app.route("/add", methods=["POST"])
def add():
    with open("times.csv", "a") as f:
        w = csv.writer(f)
        w.writerow([pendulum.now("America/Toronto").format("YYYY/MM/DD HH:mm:ss")])
    return "HI"

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
