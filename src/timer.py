import datetime

from logging import getLogger
logger = getLogger(__name__)

class TimerState:
    STATE_RUN = 'RUN'
    STATE_STOP = 'STOP'

class Timer:
    """
    Timerクラス。毎秒Tickが呼ばれる事により秒が進むようにしていたが、
    メニューバーを触っている間、rumps.Timerが止まってしまうので時刻を見るようにした。
    """

    def __init__(self) -> None:
        self.endUnixtime = 0
        self.state = TimerState.STATE_STOP

    def tick(self) -> int:
        """
        時を進める。毎秒呼ばれることを想定している
        Returns:
            残り秒数。ただし -1 は残り秒数がN/Aな状態（=タイマーが動いていない）
        """

        if self.state != TimerState.STATE_RUN:
            return -1

        unixtime = self.get_timestamp()
        left = self.endUnixtime - unixtime
        if left <= 0:
            self.state = TimerState.STATE_STOP
            return 0

        return left

    def start(self, second: int) -> None:
        self.state = TimerState.STATE_RUN
        
        self.endUnixtime = self.get_timestamp() + second

    def stop(self) -> None:
        self.state = TimerState.STATE_STOP

    def get_timestamp(self) -> int:
        return int(datetime.datetime.now().timestamp())