import ast
import datetime
import random
import webuntis
from datetime import datetime as dt, timedelta
from webuntis.objects import ExamObject
from itertools import groupby
from operator import itemgetter
import BetterPrinting as bp


now = dt(dt.now().year, dt.now().month, dt.now().day)
tomorrow = now

# today = dt(dt.now().year, 9, 17)
# monday = today - timedelta(days=today.weekday())
# friday = monday + timedelta(days=4)


class Finder:
    def __init__(self, username, password, chosen_class=None):
        self.loggedin = False
        self.username = username
        self.password = password
        self.chosen_class = chosen_class
        self.s = self.login()
        self.teachertable = {}
        self.longName = {}

    def login(self):
        s = webuntis.Session(
            server='neilo.webuntis.com',
            username=self.username,
            password=self.password,
            school='borg-graz-monsbergergasse',
            useragent='WebUntis Test'
        )
        s.login()
        self.loggedin = True
        return s

    def logout(self):
        self.s.logout()

    def get_all_dict(self):
        get_lst = ast.literal_eval(str(self.s.teachers()))
        return {each["name"]: f"{each['foreName']} {each['longName']}" for each in get_lst for k, v in each.items()}

    def get_class_timetable(self, clas):
        classtimetable = []
        get_date = datetime.datetime.now().date()
        current_date = ".".join(".".join(str(get_date).split("-")).split(".")[::-1])
        for data in self.teachertable:
            if data["class"].lower() == clas.lower():
                if current_date in str(data["starttime"]).split(",")[0]:
                    classtimetable.append(data)

        return classtimetable

    def show_today_news(self):
        if self.chosen_class is None:
            raise Exception("Du musst eine Klasse eingeben!")
        get_class_lst = self.get_class_timetable(self.chosen_class)
        sorted_data = sorted(get_class_lst, key=lambda x: x['starttimeObj'])

        grouped_data = []
        for _, group in groupby(sorted_data, key=itemgetter('starttimeObj')):
            group_list = list(group)
            if len(group_list) > 1:
                grouped_data.append([tuple(group_list)])
            else:
                grouped_data.append([group_list[0]])

        print(f"Tagesbericht für den {today}")
        today_status = {None: "fällt nicht aus", "cancelled": "fällt aus", "irregular": "wird suppliert"}
        chosen_color = random.choice(["red", "blue", "green", "cyan", "yellow", "magenta"])
        for idx, item in enumerate(grouped_data):
            for each_item in item:
                if type(each_item) is tuple:
                    for every_list in each_item:
                        bp.color(
                            f"{idx + 1}. Stunde hat die {self.chosen_class}\n\nLehrer: {every_list['teacher']}\nStunde {today_status[every_list['code']]}\nFach: {every_list['subject']}\n{finder.make_underlines()}",
                            chosen_color)

                else:
                    bp.color(
                        f"{idx + 1}. Stunde hat die {self.chosen_class}\n\nLehrer: {each_item['teacher']}\nStunde {today_status[each_item['code']]}\nFach: {each_item['subject']}\n{finder.make_underlines()}",
                        chosen_color)

    def get_teacher_table(self):
        self.s.login()
        klassen = self.s.klassen()
        all_teachers = {}
        for klasse in klassen:
            cid = klasse.id
            clas = klassen.filter(id=cid)[0]
            tt = self.s.timetable_extended(klasse=clas, start=now, end=tomorrow)

            for stunde in tt:
                try:
                    if stunde.code != "cancelled":
                        if stunde.teachers[0].name in all_teachers:
                            all_teachers[stunde.teachers[0].name].append(f'{stunde.start.strftime("%H:%M")} - {stunde.end.strftime("%H:%M")} - {stunde.rooms[0].name} - {stunde.subjects[0].long_name.title()} - {clas.name}')
                        else:
                            all_teachers[stunde.teachers[0].name] = [f'{stunde.start.strftime("%H:%M")} - {stunde.end.strftime("%H:%M")} - {stunde.rooms[0].name} - {stunde.subjects[0].long_name.title()} - {clas.name}']

                except Exception as e:
                    pass

        return all_teachers

    def get_students(self):
        self.s.login()
        data = self.s.students()
        return data

    def get_long_name(self, short_name):
        self.get_all_dict()

        return self.longName[short_name.title()]

    def find_now(self, teacher):
        for data in self.teachertable:
            dif = data["starttimeObj"] - now
            if data["teacher"].lower() == teacher.lower() and timedelta(minutes=0) <= dif <= timedelta(minutes=49):
                if data["code"] == "cancelled":
                    return {"room": "The lesson is cancelled"}
                else:
                    return data

    @staticmethod
    def make_underlines():
        return "".join(["_" for _ in range(50)])

    @staticmethod
    def check_time_in_range(time_ranges):
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")

        for each_time in time_ranges:
            start_time, end_time, room = each_time.split(' - ')[0], each_time.split(' - ')[1], each_time.split(' - ')[2]
            if start_time <= current_time <= end_time:
                return {"room": room}

        return None

    @staticmethod
    def sort_time_table(time_table):
        with open("all_times.txt", "r+", encoding="utf-8") as file:
            get_time_table = [line.replace("\n", "") for line in file.readlines()]

        all_time_table = []
        for each_time in time_table:
            get_range = " ".join(each_time.split()[:3])
            if get_range in get_time_table:
                all_time_table.append((get_time_table.index(get_range) + 1, each_time))
        return sorted(all_time_table)


if __name__ == "__main__":
    choose_class = "9t"
    finder = Finder("Bashirufaw", "7nfScyThnzbd$", choose_class)
    finder.login()
    students = ast.literal_eval(str(finder.get_students()))
    print(students)
    for idx, each_student in enumerate(students):
        print(f"{idx} {each_student['foreName']} {each_student['longName']}")
    # teacher_rooms = finder.get_teacher_table()

