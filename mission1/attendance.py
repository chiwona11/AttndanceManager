attendance_info = {}
id_cnt = 0

# dat[사용자ID][요일]
attendance_weekday_point = [[0] * 7 for _ in range(100)]
attendance_points = [0] * 100
attendance_grade = [0] * 100
attendance_name = [''] * 100
wednesday_attendance = [0] * 100
weekend_attendance = [0] * 100
grade_desc = {0: 'NORMAL', 1: 'GOLD', 2: 'SILVER'}


def calc_attendance_point(name, weekday):
    global id_cnt

    if name not in attendance_info:
        id_cnt += 1
        attendance_info[name] = id_cnt
        attendance_name[id_cnt] = name

    add_point, index = calc_daily_point(attendance_info[name], weekday)

    attendance_weekday_point[attendance_info[name]][index] += 1
    attendance_points[attendance_info[name]] += add_point


def calc_daily_point(attendance_id, weekday):
    add_point = 0
    weekday_index = 0
    if weekday == "monday":
        weekday_index = 0
        add_point += 1
    elif weekday == "tuesday":
        weekday_index = 1
        add_point += 1
    elif weekday == "wednesday":
        weekday_index = 2
        add_point += 3
        wednesday_attendance[attendance_id] += 1
    elif weekday == "thursday":
        weekday_index = 3
        add_point += 1
    elif weekday == "friday":
        weekday_index = 4
        add_point += 1
    elif weekday == "saturday":
        weekday_index = 5
        add_point += 2
        weekend_attendance[attendance_id] += 1
    elif weekday == "sunday":
        weekday_index = 6
        add_point += 2
        weekend_attendance[attendance_id] += 1
    return add_point, weekday_index


def main():
    try:
        get_attendance_table()

        for i in range(1, id_cnt + 1):
            calc_bonus_point(i)
            calc_grade(i)
            print(f"NAME : {attendance_name[i]}, POINT : {attendance_points[i]}, GRADE : {grade_desc[attendance_grade[i]]}")

        print("\nRemoved player")
        print("==============")
        check_removed_player()

    except Exception:
        print("계산에 실패했습니다.")


def check_removed_player():
    for i in range(1, id_cnt + 1):
        if attendance_grade[i] not in (1, 2) and wednesday_attendance[i] == 0 and weekend_attendance[i] == 0:
            print(attendance_name[i])


def calc_grade(i):
    if attendance_points[i] >= 50:
        attendance_grade[i] = 1
    elif attendance_points[i] >= 30:
        attendance_grade[i] = 2
    else:
        attendance_grade[i] = 0


def calc_bonus_point(i):
    if attendance_weekday_point[i][2] > 9:
        attendance_points[i] += 10
    if attendance_weekday_point[i][5] + attendance_weekday_point[i][6] > 9:
        attendance_points[i] += 10


def get_attendance_table():
    try:
        with open("attendance_weekday_500.txt", encoding='utf-8') as f:
            for _ in range(500):
                line = f.readline()
                if not line:
                    break
                parts = line.strip().split()
                if len(parts) == 2:
                    calc_attendance_point(parts[0], parts[1])
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")


if __name__ == "__main__":
    main()
