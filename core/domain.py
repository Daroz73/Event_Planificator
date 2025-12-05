from dataclasses import dataclass, field
from datetime import datetime
from core.resource import Resource
from core.worker import Worker
from core.events import Event
from core.events_planificator import Events_Planificator
from core.data_saved_loader import Data_saved_loader

# Clase central que se va a encargar de hacer todos los llamados necesarios para la gestion de operaciones 
# tanto internas como introducidas por el usuario
class Domain:
    def __init__(self):
        self.events: list[Event] = []
        self.workers: list[Worker] = []
        self.resources: list[Resource] = []
        if len(Data_saved_loader.load_file_info("events")) > 0:
            self.events = Data_saved_loader.load_file_info("events")
        if len(Data_saved_loader.load_file_info("personal")) > 0:
            self.workers = Data_saved_loader.load_file_info("personal")
        if len(Data_saved_loader.load_file_info("resources")) > 0:
            self.resources = Data_saved_loader.load_file_info("resources")
    
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
    # metodo para guardar permanetemete cualqueir elemento creado
    def add(self, item: Event | Worker | Resource):
        if isinstance(item, Event):
            self._add_event(item)
        elif isinstance(item, Worker):
            Data_saved_loader.append_(item, "personal")
            self.workers = Data_saved_loader.load_file_info("personal")
        else:
            Data_saved_loader.append_(item, "resources")
            self.resources = Data_saved_loader.load_file_info("resources")
    # metodo que agenda un evento
    def _add_event(self, event:Event):
        Events_Planificator.Agg_Event(self.events, event)
    # metodo para listar los eventos
    def list_(self, string:str) -> list[Event]:
        if string.lower() == "events":
            return Data_saved_loader.load_file_info("events")
        if string.lower() == "worker":
            return Data_saved_loader.load_file_info("personal")
        if string.lower() == "resource":
            return Data_saved_loader.load_file_info("resources")
        return []
    # metodo para eliminar un evento
    def remove_event(self, event_id: str):
        Data_saved_loader.remove_(self.events, event_id, "events")
        self.events = Data_saved_loader.load_file_info("events")
    # metodo para mostrar detalles de un event | resource | worker
    def show_details(self, id: str, *args):
        if id : 
            if "e" in id:
                for e in self.events:
                    if e.id.lower() == id.lower():
                        return e.show_details(*args)
            return "El id introducido no corresponde a ningun evento"
    # Ids Generator 
    def ids_generator(self, type:str) -> str:
        # Conjunto de los ids existentes para buscar con mayor rapidez
        existing_ids = set()
        if type.lower() == "e" or type.lower() == "event":
            prefix = "e"
            existing_ids = {item.id for item in self.events}
        elif type.lower() == "w" or type.lower() == "worker":
            prefix = "w"
            existing_ids = {item.id for item in self.workers}
        elif type.lower() == "r" or type.lower() == "resource":
            prefix = "r"
            existing_ids = {item.id for item in self.resources}
        else:
            raise ValueError("Tipo de ID no reconocido.")
        
        # Counter que nos ayudara a buscar el siguiente id disponible
        counter = 1
        found_id = False 
        new_id = ""
        while not found_id:
            new_id = f"{prefix}{counter}"
            if new_id not in existing_ids:
                found_id = True
            else:
                counter += 1
        return new_id