from discordClient import GetTime
import pytest



def test_colonOneLine():
    assert GetTime("It is 3:30pm") == ["15", "30"]

def test_colonDoubleHourOneLine():
    assert GetTime("It is 11:30pm") == ["23", "30"]

def test_freedOnlyTime():
    assert GetTime("10pm") == ["22", "00"]

def test_freedColonTime():
    assert GetTime("5:00") == ["05", "00"]

def test_freedColonMerTime():
    assert GetTime("5:00am") == ["05", "00"]

def test_colonTwoLine():
    assert GetTime("It is 3:30 pm") == ["15", "30"]

def test_freedOneLine():
    assert GetTime("Let's Meet at 12pm") == ["00", "00"]

def test_freedTwoLine():
    assert GetTime("It is 9 am") == ["09", "00"]

def test_noTimeEasy():
    assert GetTime("It is super cool") == False

def test_freedPeriod():
    assert GetTime("It is 9 a.m") == ["09", "00"]

def test_freedDoublePeriod():
    assert GetTime("It is 9 a.m.") == ["09", "00"]

def test_noTimeHard():
    p = [
        "You are: a nice person"
        "This is Amazing",
        "this is a deliberate attempt pm",
        "Amazon.com"
        "He got 4 amputations"
    ]
    for phrase in p:
        assert GetTime(phrase) == False

