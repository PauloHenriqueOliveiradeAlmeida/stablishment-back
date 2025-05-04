from abc import ABC
from app.shared.domain.value_objects.guid import Guid


class BaseEntity(ABC):
    def __init__(self, id: str | None = None) -> None:
        if id:
            self.id = Guid(id)
            return
        self.id = Guid()

    def to_dict(self):
        return {"id": self.id.value}
