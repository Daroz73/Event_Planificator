from dataclasses import dataclass, field
from datetime import datetime, timedelta
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
        # ----------------------------------
        self.event_to_delete: set[str] = set()
        self.worker_to_delete: set[str] = set()
        self.resource_to_delete: set[str] = set()
        # -----------------------------------
        self.pending_events: list[Event] = []
        self.pending_workers: list[Worker] = []
        self.pending_resources: list[Resource] = []
        if len(Data_saved_loader.load_file_info("events")) > 0:
            self.events = Data_saved_loader.load_file_info("events")
        if len(Data_saved_loader.load_file_info("personal")) > 0:
            self.workers = Data_saved_loader.load_file_info("personal")
        if len(Data_saved_loader.load_file_info("resources")) > 0:
            self.resources = Data_saved_loader.load_file_info("resources")
    
    def rebuild_relations(self):
        events_map = {e.id: e for e in self.events}
        workers_map = {w.id: w for w in self.workers}
        resources_map = {r.id: r for r in self.resources}

        for e in self.events:
            e.workers = [workers_map[w_id] for w_id in e.workers if isinstance(w_id,str) and w_id in workers_map]
            e.resources = [resources_map[r_id] for r_id in e.resources if isinstance(r_id,str) and r_id in resources_map]
        for w in self.workers:
            w.use_plan = [events_map[e_id] for e_id in w.use_plan if isinstance(e_id,str) and e_id in events_map]
        for r in self.resources:
            r.use_plan = [events_map[e_id] for e_id in r.use_plan if isinstance(e_id,str) and e_id in events_map]
    
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
            self.pending_events.append(item)
        elif isinstance(item, Worker):
            self.pending_workers.append(item)
        else:
            self.pending_resources.append(item)

    # metodo que agenda un evento
    def _add_event(self, event:Event):
        Events_Planificator.add_resource(self.workers, self.resources, self.events, event)
        Events_Planificator.Agg_Event(self.workers, self.resources, self.events, event)
        self.events = self.list_("events")
    
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
    def remove_item(self, kind:str, item_id: str):
        if kind == "e" or kind == "event":
            Data_saved_loader.remove_(self.events, item_id, "events")
        if kind == "w" or kind == "worker":
            Data_saved_loader.remove_(self.workers, item_id, "personal")
        if kind == "r" or kind == "resource":
            Data_saved_loader.remove_(self.resources, item_id, "resources")
        # limpiar los set de objetos a eliminar
        self.event_to_delete.clear()
        self.worker_to_delete.clear()
        self.resource_to_delete.clear()
    
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
    
    # metodo para obtener un item especifico por su id
    def get_item(self, type:str, id:str) -> Event | Worker | Resource | None:
        if type.lower() == "e" or type.lower() == "event":
            for item in self.events:
                if item.id.lower() == id.lower():
                    return item
        elif type.lower() == "w" or type.lower() == "worker":
            for item in self.workers:
                if item.id.lower() == id.lower():
                    return item
        elif type.lower() == "r" or type.lower() == "resource":
            for item in self.resources:
                if item.id.lower() == id.lower():
                    return item
        return None
    
    # metodo para ordenar una lista de eventos por fecha de inicio==========================================
    def sorted_events_by_begin(slef, events_list:list[Event]) -> list[Event]:
        return sorted(events_list, key=lambda x: x.begin)
    
    # metodo para marcar los objetos que se quieren borrar 
    def mark_for_delete(self, kind:str, item_id:str):
        if kind == "e" or kind == "event":
            self.event_to_delete.add(item_id)
            self.events = [e for e in self.events if e.id not in self.event_to_delete]
        elif kind == "w" or kind == "worker":
            self.worker_to_delete.add(item_id)
            self.workers = [w for w in self.workers if w.id not in self.worker_to_delete]
        elif kind == "r" or kind == "resource":
            self.resource_to_delete.add(item_id)
            self.resources = [r for r in self.resources if r.id not in self.resource_to_delete]
    
    # metodo para guardar los eventos creados en las listas temporales antes de ser guardados en los json=====
    def save_pending(self):
        # Guardar Eventos
        for event in self.pending_events:
            Events_Planificator.add_resource(
                self.workers, self.resources, self.events, event
            )
            Events_Planificator.Agg_Event(
                self.workers, self.resources, self.events, event
            )
            self.events.append(event)
        self.persist_workers_and_resources()
        # Guardar worker
        for worker in self.pending_workers:
            Data_saved_loader.append_(worker, "personal")
            self.workers.append(worker)
        # Guardar resource
        for resource in self.pending_resources:
            Data_saved_loader.append_(resource, "resources")
            self.resources.append(resource)
        # limpiamos las listas
        self.pending_events.clear()
        self.pending_workers.clear()
        self.pending_resources.clear()
    
    # Metodo para salvar los elmentos eliminados en el json=============================================
    def persist_deletions(self):
        # actualizar las listas del domain quitando los elementos marcados para eliminar
        if len(self.event_to_delete) > 0:
            self.events = [e for e in self.events if e.id not in self.event_to_delete]
            copy_event = self.events.copy()
            for c_e in copy_event:
                c_e.workers = [w.id for w in c_e.workers]
                c_e.resources = [ r.id for r in c_e.resources]
            Data_saved_loader.update_all(copy_event, "events")
        if len(self.worker_to_delete) > 0:
            self.workers = [w for w in self.workers if w.id not in self.worker_to_delete]
            copy_worker = self.workers.copy()
            for c_w in copy_worker:
                c_w.use_plan = [e.id for e in c_w.use_plan]
            Data_saved_loader.update_all(copy_worker, "personal")
        if len(self.resource_to_delete) > 0:
            self.resources = [r for r in self.resources if r.id not in self.resource_to_delete]
            copy_resource = self.resources
            for c_r in copy_resource:
                c_r.use_plan = [e.id for e in c_r.use_plan]
            Data_saved_loader.update_all(c_r, "resources")
        # Limpiamos los set de objetos a eliminar
        self.event_to_delete.clear()
        self.worker_to_delete.clear()
        self.resource_to_delete.clear()

    # metodo para hacer que persistan los cambios de los trabajadores y recursos=======================
    def persist_workers_and_resources(self):
        if len(self.workers) > 0 and len(self.workers[0].use_plan) > 0 and isinstance(self.workers[0].use_plan[0], Event):
            copy_workes = self.workers.copy()
            for c_w in copy_workes:
                c_w.use_plan = [e.id if isinstance(e,Event) else e for e in c_w.use_plan]
            Data_saved_loader.update_all(copy_workes, "personal")
        else:
            Data_saved_loader.update_all(self.workers, "personal")
        if len(self.resources) > 0 and len(self.resources[0].use_plan) > 0 and isinstance(self.resources[0].use_plan[0], Event):
            copy_resource = self.workers.copy()
            for c_w in copy_resource:
                c_w.use_plan = [e.id if isinstance(e,Event) else e for e in c_w.use_plan]
            Data_saved_loader.update_all(copy_resource, "resources")
        else:
            Data_saved_loader.update_all(self.resources, "resources")

    # metodo que devuelve todas las especialidades posibles de los trabajadores=========================================
    def get_specialities(self) -> set[str]:
        return {"Alergología", "Algología", "Anestesiología", "Angiología", "Cardiología"
                , "Cirugía general", "Cirugía cardíaca", "Cirugía torácica", "Cirugía vascular"
                , "Cirugía oral y maxilofacial", "Cirugía plástica", "Cirugía pediátrica"
                , "Cirugía ortopédica y traumatología", "Coloproctología", "Dermatología"
                , "Endocrinología", "Estomatología", "Gastroenterología", "Geriatría", "Genética médica"
                , "Hematología", "Inmunología", "Enfermedades infecciosas", "Medicina interna"
                , "Medicina de emergencia", "Medicina familiar", "Medicina física y rehabilitación"
                , "Medicina nuclear", "Nefrología", "Neonatología", "Neumología", "Neurología"
                , "Neurocirugía", "Obstetricia", "Ginecología", "Oftalmología", "Oncología"
                , "Otorrinolaringología", "Pediatría", "Psiquiatría", "Psicología clínica", "Radiología"
                , "Reumatología", "Urología", "Análisis clínicos", "Anatomía patológica", "Bioquímica clínica"
                , "Microbiología y parasitología", "Neurofisiología clínica", "Farmacología clínica"
                , "Rehabilitación", "Fisioterapia", "Odontología", "Emergenciología","Enfermería","Chofer"
                }
    
    def get_resources(self):
        return {
        "jeringas","recetas","espéculo","guantes desechables","mascarillas","batas desechables","gasas estériles",
        "vendas","agujas desechables","pinzas hemostáticas","tijeras quirúrgicas","portaagujas","bisturí","laptop",
        "hojas de bisturí","antisépticos","soluciones desinfectantes","esparadrapos","apósitos","ambú","collarín cervical",
        "termómetros","estetoscopios","tensiómetros","pulsioxímetros","desfibriladores","lapiceros",
        "concentradores de oxígeno","máquinas de succión","bolsas de esterilización","máquinas de rayos X",
        "escáneres de resonancia magnética","tomógrafos computarizados (TAC)","ecógrafos","máquinas de electrocardiograma (ECG)",
        "monitores multiparamétricos","desfibriladores","ventiladores mecánicos","bombas de infusión",
        "máquinas de diálisis","máquinas de anestesia","mesas quirúrgicas","lámparas quirúrgicas","esterilizadores",
        "concentradores de oxígeno","máquinas de succión","pulsioxímetros","termómetros digitales","glucómetros",
        "incubadoras neonatales","bilirrubinómetros","equipos de visualización de venas","sillas de ruedas",
        "camas hospitalarias","ambulancias","equipos de transporte de pacientes","centrifugas para análisis de muestras",
        "analizadores bioquímicos","Microscopios","Espectrómetros","Quirófano"
        }
    
    # ============================================================================================================
    
    # funcion para optener las especialesdades que pueden utilizar un x recurso
    def get_specialities_by_resource(self) -> dict[str,set[str]]:
        return {
            "jeringas": {"all"},
            "recetas": {"all"},
            "guantes desechables": {"all"},
            "mascarillas": {"all"},
            "batas desechables": {"all"},
            "gasas estériles": {"all"},
            "vendas": {"all"},
            "agujas desechables": {"all"},
            "antisépticos": {"all"},
            "soluciones desinfectantes": {"all"},
            "esparadrapos": {"all"},
            "apósitos": {"all"},
            "termómetros": {"all"},
            "termómetros digitales": {"all"},
            "lapiceros": {"all"},
            "estetoscopios": {
                "Medicina interna", "Cardiología", "Neumología",
                "Medicina familiar", "Pediatría", "Geriatría",
                "Medicina de emergencia", "Enfermería"
            },
            "tensiómetros": {"all"},
            "pulsioxímetros": {
                "Medicina interna", "Neumología", "Cardiología",
                "Medicina de emergencia", "Anestesiología", "Enfermería"
            },
            "glucómetros": {
                "Endocrinología", "Medicina interna",
                "Medicina familiar", "Enfermería"
            },
            "espéculo": {"Ginecología", "Obstetricia"},
            "incubadoras neonatales": {"Neonatología"},
            "bilirrubinómetros": {"Neonatología", "Pediatría"},
            "pinzas hemostáticas": {
                "Cirugía general", "Cirugía cardíaca", "Cirugía torácica",
                "Cirugía vascular", "Cirugía pediátrica",
                "Cirugía ortopédica y traumatología",
                "Neurocirugía"
            },
            "tijeras quirúrgicas": {
                "Cirugía general", "Cirugía plástica",
                "Cirugía pediátrica", "Neurocirugía"
            },
            "portaagujas": {
                "Cirugía general", "Cirugía plástica",
                "Cirugía pediátrica", "Neurocirugía"
            },
            "bisturí": {
                "Cirugía general", "Cirugía plástica",
                "Cirugía pediátrica", "Neurocirugía"
            },
            "hojas de bisturí": {
                "Cirugía general", "Cirugía plástica",
                "Cirugía pediátrica", "Neurocirugía"
            },
            "mesas quirúrgicas": {
                "Cirugía general", "Cirugía cardíaca",
                "Cirugía torácica", "Neurocirugía"
            },
            "lámparas quirúrgicas": {
                "Cirugía general", "Cirugía cardíaca",
                "Cirugía torácica", "Neurocirugía"
            },
            "Quirófano": {
                "Cirugía general", "Cirugía cardíaca", "Cirugía torácica",
                "Cirugía vascular", "Neurocirugía",
                "Cirugía pediátrica", "Cirugía plástica"
            },
            "ambú": {
                "Anestesiología", "Medicina de emergencia", "Enfermería"
            },
            "ventiladores mecánicos": {
                "Anestesiología", "Neumología",
                "Medicina de emergencia", "Medicina interna"
            },
            "máquinas de anestesia": {"Anestesiología"},
            "bombas de infusión": {
                "Anestesiología", "Medicina interna",
                "Neonatología", "Enfermería"
            },
            "concentradores de oxígeno": {
                "Neumología", "Medicina interna",
                "Medicina de emergencia", "Enfermería"
            },
            "máquinas de succión": {
                "Anestesiología", "Medicina de emergencia", "Enfermería"
            },
            "desfibriladores": {
                "Cardiología", "Medicina de emergencia"
            },
            "máquinas de electrocardiograma (ECG)": {
                "Cardiología", "Medicina interna"
            },
            "monitores multiparamétricos": {
                "Cardiología", "Anestesiología",
                "Medicina de emergencia"
            },
            "máquinas de rayos X": {"Radiología"},
            "escáneres de resonancia magnética": {"Radiología"},
            "tomógrafos computarizados (TAC)": {"Radiología"},
            "ecógrafos": {"Radiología", "Ginecología", "Obstetricia"},
            "centrifugas para análisis de muestras": {
                "Análisis clínicos", "Bioquímica clínica"
            },
            "analizadores bioquímicos": {"Bioquímica clínica"},
            "Microscopios": {
                "Microbiología y parasitología",
                "Anatomía patológica", "Análisis clínicos"
            },
            "Espectrómetros": {"Bioquímica clínica"},
            "sillas de ruedas": {"all"},
            "camas hospitalarias": {"all"},
            "equipos de transporte de pacientes": {
                "Medicina de emergencia", "Enfermería"
            },
            "ambulancias": {
                "Emergenciología", "Chofer"
            },
            "bolsas de esterilización": {"Enfermería"},
            "esterilizadores": {"Enfermería"}
        }
    # ====================================================================================================
    
    # Funcion para buscar huecos
    def find_next_avialable_slot(self, personal_req:dict, resource_req:dict, duration:timedelta,step_minutes: int = 15) ->tuple[datetime, datetime]:
        
        current_start = datetime.now().replace(second=0, microsecond=0)
        
        events = sorted(self.events, key=lambda e: e.begin)

        while True:
            candidate_end = current_start + duration

            conflict = False

            for e in events:
                if e.end <= current_start or e.begin >= candidate_end:
                    continue
                for role, qty in personal_req.items():
                    if role in e.personal_requested:
                        conflict = True
                        break
                for res, qty in resource_req.items():
                    if res in e.resources_requested:
                        conflict = True
                        break
                if conflict:
                    break
            if not conflict:
                return current_start, candidate_end
            current_start += timedelta(minutes=step_minutes)
    # ===================================================================================================
    
    # funcion para detectar el solapamiento de errores
    def _overlaps(start1, end1, start2, end2):
        # True si los intervalos se solapan en el tiempo
        return start1 < end2 and start2 < end1
    
    # funcion para validar si un hueco es valido
    def _is_valid_slot(self, start:datetime, end:datetime, personal_req:dict[str, int], resources_req:dict[str,int]):
        for e in self.events:
            # revisamos conflicto de fechas
            if not self._overlaps(start, end, e.begin, e.end):
                continue
            # revisamos conflicto de personal
            for role, needed in personal_req.items():
                used = e.personal_requested.get(role, 0)
                if used >= needed:
                    return False
            # revisamos conflicto de recursos
            for res, needed in resources_req.items():
                used = e.resources_requested.get(res, 0)
                if used >= needed:
                    return False
        return True 
    
    # metodo para obtener un diccionario de recursos y especialidades con la cantidad disponible=============
    def get_count(self, kind:str) -> dict[str, int]:
        data:dict[str,int] = {}
        if kind.lower() == "w":
            for w in self.workers:
                if w.specialty in data:
                    data[w.specialty] += 1
                else:
                    data[w.specialty] = 1
        elif kind.lower() == "r":
            for r in self.resources:
                if r.name in data:
                    data[r.name] += 1
                else:
                    data[r.name] = 1
        return data