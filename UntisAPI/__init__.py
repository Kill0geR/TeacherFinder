import webuntis
from datetime import datetime
import ast


def login(username, password):
    try:
        s = webuntis.Session(
            server='neilo.webuntis.com',
            username=username,
            password=password,
            school='borg-graz-monsbergergasse',
            useragent='WebUntis Test'
        )
        s.login()
        return s
    except NameError:
        raise Exception('Du musst Webuntis herunterladen du Hund\nAlso `pip install webuntis`')


def get_9t_lessons(username, password):
    s = login(username, password)
    klassen = s.klassen()
    all_lessons = {}
    latin_french = {}
    long_names = {'GWB': 'Geographie', 'PUP': 'Philosophie', 'INW': 'Internet Working', 'BIU': 'Biologie', 'BSPK': 'Turnen', 'R': 'Religion'}
    for klasse in klassen:
        cid = klasse.id
        clas = klassen.filter(id=cid)[0]
        now = datetime(datetime.now().year, 9, 16)
        tt = s.timetable_extended(klasse=clas, start=now, end=now)

        for stunde in tt:
            try:
                if clas.name == "9t" and stunde.code != "cancelled":
                    short_name = stunde.subjects[0].name
                    if stunde.end.strftime("%H:%M") not in all_lessons:
                        all_lessons[stunde.end.strftime("%H:%M")] = [stunde.teachers[0].name, stunde.rooms[0].name, stunde.subjects[0].long_name.title() if short_name not in long_names else long_names[short_name]]
                    else: latin_french[stunde.end.strftime("%H:%M")] = [stunde.teachers[0].name, stunde.rooms[0].name, stunde.subjects[0].long_name.title() if short_name not in long_names else long_names[short_name]]
            except Exception as e:
                print(e)

    return dict(sorted(all_lessons.items())), latin_french


def get_all_teachers(username, password):
    with open("all_teacher_genders.txt", "r") as f:
        teachers_gender = f.readlines()

    s = login(username, password)
    get_lst = ast.literal_eval(str(s.teachers()))
    all_teachers = {each["name"]: [each['longName'], " ".join(teachers_gender[idx].split()[1:])] for idx, each in enumerate(get_lst) for k, v in each.items()}
    return all_teachers
