from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_intent_name, is_request_type
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model.ui.link_account_card import LinkAccountCard
from ask_sdk_model.device import Device
from flask_ask_sdk.skill_adapter import SkillAdapter
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

sb = SkillBuilder()

@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):

    if is_production():
        file = "/home/sleepschedule/mysite/times.csv"
    else:
        file = "times.csv"
    with open(file, "a") as f:
        w = csv.writer(f)
        w.writerow([pendulum.now("America/Toronto").format("YYYY/MM/DD HH:mm:ss")])

    hour = pendulum.now("America/Toronto").hour
    if hour >= 17 and hour <= 3:
        speech_text = "goodnight"
    else:
        speech_text = "goodmorning"

    return build_response(handler_input, speech_text, "Sleep Schedule", end=True)

@sb.request_handler(can_handle_func=is_intent_name("TimeCancelIntent"))
def sleep_time_intent_handler(handler_input):

    speech_text = "Time cancelling feature is yet to be developed"
    return build_response(handler_input, speech_text, "Sleep Schedule")

@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    speech_text = "I track what time you went to sleep and wake up"
    return build_response(handler_input, speech_text, "Sleep Schedule", ask=True)

@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def help_intent_handler(handler_input):

    print(handler_input)
    speech_text = "Sorry, sleep schedule didn't get that."

    return build_response(handler_input, speech_text, "Sleep Schedule", ask=True)

@sb.request_handler(
    can_handle_func=lambda input:
        is_intent_name("AMAZON.CancelIntent")(input) or
        is_intent_name("AMAZON.StopIntent")(input))
def cancel_and_stop_intent_handler(handler_input):
    speech_text = "Goodbye!"

    return build_response(handler_input, speech_text, "Sleep Schedule", shouldEndSession=True)

@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    #any cleanup logic goes here
    return handler_input.response_builder.response

@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    # Log the exception
    print(exception)

    speech_text = "Sorry, I didn't get it. Can you please say it again?"
    return build_response(handler_input, speech_text, "Sleep Schedule", ask=True)

skill_adapter = SkillAdapter(
    skill=sb.create(), skill_id="amzn1.ask.skill.b134fcc6-c7e1-47f6-a1ac-46b2216f665a", app=app)

def build_response(input, text, card_title="", card_content=None, end=False, ask=False):
    """ Function to build responses """

    if not card_content:
        card_content = text
    input.response_builder.speak(text)
    input.response_builder.set_card(SimpleCard(card_title, card_content))
    input.response_builder.set_should_end_session(end)
    if ask:
        input.response_builder.ask(text)

    return input.response_builder.response

@app.route("/")
def sleepschedule():
    out = get_times()
    return render_template("sleepschedule.html", times=out[0], average=out[1], slope=out[2])

@app.route("/log", methods=["POST"])
def invoke_skill():
    print("IN")
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
