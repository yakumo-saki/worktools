from src.timer import Timer
from pprint import pprint
import typing

class PomoState:
    RUN = 'RUN'
    PAUSE = 'PAUSE'
    STOP = 'STOP'

class PomoType():    
    FOCUS = 'FOCUS'
    RELAX = 'RELAX'
    BREAK = 'BREAK'  # 4セット実施後は長い休憩
    NONE = 'NONE'    # 一度も開始していない初期状態
    
    MINUTE = 1
    FOCUS_SEC = 25 * MINUTE
    RELAX_SEC = 5 * MINUTE
    BREAK_SEC = 15 * MINUTE

class Pomodoro:

    def __init__(self) -> None:
        self.pomodoroSetsDone = 0
        self.timer = Timer()
        self.currentType = PomoType.NONE
        self.currentState = PomoState.STOP
        self.timerSecond = 0

    """
    時を進める。毎秒呼ばれることを想定している
    Returns:
        残り秒数。ただし -1 は pause 状態ではないことを示す
        100%の秒数
    """
    def tick(self) -> typing.Tuple[int, int]:
        left = self.timer.tick()
        if left == 0:
            self.pomodoroSetsDone = self.pomodoroSetsDone + 1
        
        if self.currentState == PomoState.RUN:
            return left, self.timerSecond
        
        return (-1, -1)

    def get_next(self) -> str:
        if self.currentType == PomoType.FOCUS:
            if self.pomodoroSetsDone >= 4:
                return PomoType.BREAK

            return PomoType.RELAX
        
        return PomoType.FOCUS

    def start(self, pomodoroType):
        if pomodoroType == PomoType.FOCUS:
            self.timerSecond = PomoType.FOCUS_SEC
        elif pomodoroType == PomoType.BREAK:
            self.timerSecond = PomoType.BREAK_SEC
        elif pomodoroType == PomoType.RELAX:
            self.timerSecond = PomoType.RELAX_SEC
        else:
            raise NotImplementedError(f"unknown pomoType {pomodoroType}")
        
        self.timer.start(self.timerSecond)
        self.currentType = pomodoroType
        self.currentState = PomoState.RUN

    def stop(self):
        self.currentState = PomoState.STOP
        self.timer.stop()

    def resume(self) -> int:
        self.timer.stop()
        if (self.currentState == PomoState.PAUSE):
            self.currentState = PomoState.RUN
            return self.secondsLeft
        
        return -1

    def pause(self) -> None:
        self.currentState = PomoState.PAUSE
        self.timer.stop()