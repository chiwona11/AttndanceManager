
import pytest
from mission2.attendance.service import AttendanceService
from mission2.attendance.io import parse_lines


def test_record_and_finalize():
    svc = AttendanceService()
    for _ in range(10):  # 10*3 = 30
        svc.record_attendance("alice","wednesday")
    for _ in range(10):  # 10*2 = 20 -> total 50 => GOLD
        svc.record_attendance("alice","saturday")
    for _ in range(30):  # 30*1 = 30 => SILVER
        svc.record_attendance("bob","monday")
    svc.finalize()
    res = {n:(p,g) for n,p,g in svc.results()}
    assert res["alice"]==(70,"GOLD")
    assert res["bob"]==(30,"SILVER")

def test_unknown_weekday():
    svc = AttendanceService()
    with pytest.raises(ValueError):
        svc.record_attendance("x","Funday")

def test_strategy_calc_and_points():
    svc = AttendanceService()
    svc.record_attendance("alice","wednesday") # +3
    svc.record_attendance("alice","sunday")    # +2
    svc.record_attendance("alice","monday")    # +1 => total 6
    svc.finalize()
    res = dict((n,(p,g)) for n,p,g in svc.results())
    assert res["alice"]==(6,"NORMAL")

def test_parse_lines():
    data = ["alice monday\n","badline\n"," bob   sunday "]
    assert list(parse_lines(data)) == [("alice","monday"),("bob","sunday")]

def test_bonus_and_grade():
    svc = AttendanceService()
    for _ in range(10): svc.record_attendance("alice","wednesday")  # 30
    for _ in range(5):
        svc.record_attendance("alice","saturday") # +10
        svc.record_attendance("alice","sunday")   # +10 -> 50 before bonus
    svc.finalize()  # +20 bonus
    res = dict((n,(p,g)) for n,p,g in svc.results())
    assert res["alice"]==(70,"GOLD")