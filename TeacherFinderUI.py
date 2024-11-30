import datetime
import json
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask, render_template, request, redirect, url_for
from TeacherFinder import Finder


def new_data(new_data_stream):
    with open("data.json", 'r+') as file:
        file_data = json.load(file)
        if file_data["current_data"]: file_data["current_data"][0] = new_data_stream
        else: file_data["current_data"].append(new_data_stream)

        file.seek(0)
        json.dump(file_data, file, indent=4)


def update_teacher_table():
    print("Aktualisiere die Lehrertabelle...")
    get_new_data = finder.get_teacher_table()
    new_data(get_new_data)
    print("Lehrertabelle erfolgreich aktualisiert.")


finder = Finder("Bashirufaw", "7nfScyThnzbd$")
all_names = finder.get_all_dict()
get_data = finder.get_teacher_table()
new_data(get_data)


now = datetime.datetime.now()
next_midnight = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(days=1)

scheduler = BackgroundScheduler()
trigger = IntervalTrigger(hours=24, start_date=next_midnight, timezone="Europe/Vienna")
scheduler.add_job(update_teacher_table, trigger)
scheduler.start()

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/find", methods=["POST"])
def find():
    teacher = request.form.get("input_string").strip().title()
    teacher_name = None

    with open("data.json", 'r+') as file:
        all_data = json.load(file)["current_data"][0]

    try:
        sorted_lst = Finder.sort_time_table(list(set((all_data.get(teacher, [])))))
        print(sorted_lst)
    except Exception as e:
        print(e)
        sorted_lst = None

    try:
        teacher_name = all_names[teacher.title()]
        output = finder.check_time_in_range(all_data.get(teacher, []))
        room = output["room"] if output else "Die Lehrperson hat derzeit keinen Unterricht"

    except Exception as e:
        print(e)
        room = "Die Lehrperson hat derzeit keinen Unterricht"
        teacher_name = teacher_name if teacher_name else "None"

    return render_template("index.html", teacher=teacher_name, room=room, sorted_lst=sorted_lst)


@app.route("/redirect_home")
def redirect_home():
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run("0.0.0.0", debug=True)

finder.logout()
