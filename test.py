data = ['07:50 – 08:40', '08:45 – 09:35', '09:40 – 10:30', '10:45 – 11:35', '11:35 – 12:25', '12:25 – 13:15', '13:20 – 14:10', '14:10 – 15:00', '15:00 – 15:50', '15:50 – 16:40', '16:40 – 17:30', '17:30 – 18:20']
times = ['11:35 - 12:25 - 147', '12:25 - 13:15 - 139', '08:45 - 09:35 - 233', '10:45 - 11:35 - 131']

for each_time in times:
    get_range = " ".join(each_time.split()[:3])
    print(get_range)
    if get_range in data:
        print("hah")
