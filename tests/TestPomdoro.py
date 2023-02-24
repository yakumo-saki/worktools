from src.timer import *

def test_timer():
    pomo = Pomodoro()
    pomo.start(10)
    assert TimerState.STATE_START == pomo.state

    for i in range(10, 0):
        print(pomo.tick())
        assert i == pomo.tick

    assert TimerState.STATE_STOP == pomo.state