from mission2.attendance.service import AttendanceService
from mission2.attendance.io import load_from_file


def main(filepath: str = "attendance_weekday_500.txt") -> int:
    svc = AttendanceService()
    try:
        for name, weekday in load_from_file(filepath):
            svc.record_attendance(name, weekday)
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
        return 1

    svc.finalize()
    for name, points, grade in svc.results():
        print(f"NAME : {name}, POINT : {points}, GRADE : {grade}")
    print("\nRemoved player")
    print("==============")
    for name in svc.removed_players():
        print(name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
