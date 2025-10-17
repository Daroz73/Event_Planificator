from dataclasses import dataclass, field
from datetime import datetime
from core.resource import Resource

@dataclass
class Event:
    id: str
    name: str
    personal_requested: int
    specialist_in_charge: str
    begin: datetime
    end: datetime
    is_emergency: bool
    personal: list[dict] = field(default_factory = dict)
    resources: list[dict] = field(default_factory = dict)

    def __repr__(self):
        return f"Event: {self.name} begins in {self.begin} ends in {self.end}, is emergency {self.is_emergency}. Resources {self.resources} and Personal {self.personal}"
    