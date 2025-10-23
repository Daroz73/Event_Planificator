from dataclasses import dataclass, field
from datetime import datetime
from core.resource import Resource
from core.events import Event
from core.events_planificator import Events_Planificator
from core.data_saved_loader import Data_saved_loader

# @dataclass
class Domain:
    events: list[Event]
    
    # funcion que actualiza los eventos y elimina los que ya hayan pasado
    # @staticmethod
    def update_events(self):
        for e in self.events:
            if (e.end - datetime.now()).total_seconds() == 0:
                for w, r in e.workers, e.resources:
                    w.use_plan.remove(e)
                    r.use_plan.remove(e)
                self.events.remove(e)
    
    # metodo que agenda un evento
    def add_event(self, event:Event):
        Events_Planificator.Agg_Event(self.events, event)