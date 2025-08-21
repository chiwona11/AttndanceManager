
import pytest, sys
from mission2.attendance.service import AttendanceService
from mission2.attendance.io import parse_lines, load_from_file


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


def test_removed_policy_and_main(tmp_path, capsys):
    p = tmp_path / "data.txt"
    lines = ["alice wednesday\n"]*10 + ["alice saturday\n"]*5 + ["alice sunday\n"]*5
    lines += ["bob monday\n"]*29 + ["bob tuesday\n"]
    lines += ["carol monday\n"]
    p.write_text("".join(lines), encoding="utf-8")

    sys.modules.pop("main", None)
    import mission2.main as main_mod
    rc = main_mod.main(str(p))
    out = capsys.readouterr().out
    assert rc == 0
    assert "NAME : alice, POINT : 70, GRADE : GOLD" in out
    assert "NAME : bob, POINT : 30, GRADE : SILVER" in out
    assert "NAME : carol, POINT : 1, GRADE : NORMAL" in out
    assert "Removed player" in out and "carol" in out

