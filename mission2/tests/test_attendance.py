
import pytest
from mission2.attendance.service import AttendanceService

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
    assert res["alice"]==(50,"GOLD")
    assert res["bob"]==(30,"SILVER")

def test_unknown_weekday():
    svc = AttendanceService()
    with pytest.raises(ValueError):
        svc.record_attendance("x","Funday")
