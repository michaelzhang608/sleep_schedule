import pendulum
import csv

def get_sleeps(file):

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

    return sleeps
