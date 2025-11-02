from dataclasses import dataclass, field
from datetime import datetime
from core.resource import Resource
from core.events import Event
from core.events_planificator import Events_Planificator
from core.data_saved_loader import Data_saved_loader

# Clase central que se va a encargar de hacer todos los llamados necesarios para la gestion de operaciones 
# tanto internas como introducidas por el usuario
class Domain:
    def __init__(self):
        self.events: list[Event] = []
        if len(Data_saved_loader.load_file_info("events")) > 0:
            self.events = Data_saved_loader.load_file_info("events")
    
    # funcion que actualiza los eventos y elimina los que ya hayan pasado
    def update_events(self):
        now = datetime.now()
        for e in self.events[:]: # trabajamos con una copia de self.events para evitar problemas al eliminar elementos mientras iteramos
            if (e.end - now).total_seconds() <= 0:
                for w in e.workers :
                    w.use_plan.remove(e)
                for r in e.resources :
                    r.use_plan.remove(e)
                self.events.remove(e)
    
    # metodo que agenda un evento
    def add_event(self, event:Event):
        Events_Planificator.Agg_Event(self.events, event)