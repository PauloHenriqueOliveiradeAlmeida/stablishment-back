import time


class Timestamp:
    def __init__(self, timestamp: float | None = None) -> None:
        if timestamp is None:
            self.__timestamp = time.time()
            return
        self.__timestamp = timestamp

    @property
    def raw_value(self) -> float:
        return self.__timestamp

    @property
    def formatted_value(self) -> str:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.__timestamp))
