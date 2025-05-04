from uuid import uuid4


class Guid:
    def __init__(self, value: str | None = None):
        if value:
            self.__value = value
            return
        self.__value = uuid4()

    @property
    def value(self):
        return str(self.__value)
