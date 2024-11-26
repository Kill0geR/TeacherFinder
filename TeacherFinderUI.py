import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask, render_template, request, redirect, url_for
from TeacherFinder import Finder


finder = Finder("Bashirufaw", "7nfScyThnzbd$")
app = Flask(__name__)
all_names = finder.get_all_dict()
all_data = finder.get_teacher_table()


def update_teacher_table():
    global all_data
    print("Aktualisiere die Lehrertabelle...")
    all_data = finder.get_teacher_table()
    print("Lehrertabelle erfolgreich aktualisiert.")


now = datetime.datetime.now()
next_midnight = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(days=1)

scheduler = BackgroundScheduler()
trigger = IntervalTrigger(hours=24, start_date=next_midnight, timezone="Europe/Vienna")
scheduler.add_job(update_teacher_table, trigger)
scheduler.start()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/find", methods=["POST"])
def find():
    teacher = request.form.get("input_string").strip().title()
    teacher_name = None

    try:
        sorted_lst = Finder.sort_time_table(list(set((all_data.get(teacher, [])))))  # Handle when teacher not found
        print(sorted_lst)
    except Exception as e:
        print(e)
        sorted_lst = None

    try:
        teacher_name = finder.get_all_dict().get(teacher, teacher)
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
