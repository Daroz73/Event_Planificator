from dataclasses import dataclass, field
from datetime import datetime
from core.resource import Resource
from core.worker import Worker

@dataclass
class Event:
    id: str
    name: str
    personal_requested: dict
    resources_requested: dict
    specialist_in_charge: str
    begin: datetime
    end: datetime
    is_emergency: bool
    workers: list[Worker] = field(default_factory = list)
    resources: list[Resource] = field(default_factory = list)