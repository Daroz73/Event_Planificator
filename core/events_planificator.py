from core.events import Event
from core.resource import Resource
from core.worker import Worker
from core.data_saved_loader import Data_saved_loader


# Clase encargada de recibir y cargar los nuevos eventos para asegurarse de que no tengan conflictos y cumplan las restrincciones 
# antes de ser guardados 
class Events_Planificator:
    # Metodo para a Agendar un evento Creado por el usuario
    @staticmethod
    def Agg_Event(workers:list[Worker], resources:list[Resource], events:list[Event], event: Event):
        if (Events_Planificator._check_resources(workers, resources, event.personal_requested, event.workers) 
            and Events_Planificator._there_is_specialist_in_charge(workers, event) 
            and Events_Planificator._check_resources(workers, resources, event.resources_requested, event.resources) 
            and Events_Planificator._check_co_requested(workers, resources, event)
        ): 
            for e in events:
                if ((Events_Planificator.conflict_event_begin(e, event) 
                    or abs((event.begin - e.begin).seconds) < 3600) 
                    and Events_Planificator.compare_event_resources(e, event)
                ):
                   return False
            
            events.append(event)
            Data_saved_loader.append_(event, "events")
            return True
        return False

    # metodo que me dice si dos eventos tienen la misa fecha de inicio
    @staticmethod
    def conflict_event_begin(event_1:Event, event_2:Event):
        if event_1.begin == event_2.begin: return True
        return False
    
    # metodo que me dice si dos eventos terminan a la misma vez
    @staticmethod
    def conflict_event_end(event_1:Event, event_2:Event):
        if event_1.end == event_2.end : return True
        return False

    # Metodo que comprueba que los recursos asignados (workers y resources) sean los requeridos
    # Restriccion 1
    @staticmethod
    def _check_resources(workers:list[Worker], resources:list[Resource], dic: dict, ids: list[str]) -> bool:
        if not dic or not ids:
            return False

        objs = []
        for id in ids:
            for w in workers:
                if w.id.lower() == id.lower():
                    objs.append(w)
            for r in resources:
                if r.id.lower() == id.lower():
                    objs.append(r)

        if len(objs) < sum(dic.values()):
            return False

        for key, required in dic.items():
            count = 0
            for o in objs:
                if isinstance(o, Worker) and o.specialty.lower() == key.lower():
                    count += 1
                elif isinstance(o, Resource) and o.name.lower() == key.lower():
                    count += 1
            if count < required:
                return False    
        return True
    #  metodo auxiliar para comprobar que entre los empleados se encuentre el 
    #  encargado del evento
    @staticmethod
    def _there_is_specialist_in_charge(workers:list[Worker], event: Event):
        for wid in event.workers:
            for w in workers:
                if w.id.lower() == wid and event.specialist_in_charge.lower() == w.specialty.lower():
                    return True
        return False

    # metodo para agregar los Co-requisitos a un evento
    @staticmethod
    def add_resource(workers:list[Worker], resources:list[Resource], events:list[Event], event:Event):  
        dic_w = event.personal_requested.copy()
        dic_r = event.resources_requested.copy()

        for w in workers:
            if w.specialty in dic_w.keys() and dic_w[w.specialty] > 0 and w.co_requested in dic_r.keys() and dic_r[w.co_requested] > 0:
                Events_Planificator._add_resource_to_event(event, w, events)
                dic_w[w.specialty] -= 1
        counter = len(event.resources)
        for r in resources:
            if r.name in dic_r.keys() and dic_r[r.name] > 0:
                Events_Planificator._add_resource_to_event(event, r, events)
                dic_r[r.name] -= 1
        if any(v > 0 for v in dic_w.values()) or any(v > 0 for v in dic_r.values()):
            return False
        return True
    # Metodo auxiliar para agregar un recurso a un evento
    @staticmethod
    def _add_resource_to_event(event: Event, resource: Resource|Worker, events:list[Event]):
        if not resource.use_plan:
            if isinstance(resource, Worker):
                event.workers.append(resource.id)
            else:
                event.resources.append(resource.id)
            resource.use_plan.append(event.id)
            return 
        last_event_id = resource.use_plan[-1].end
        last_event = next((e for e in events if e.id == last_event_id), None)
        if last_event is None:
            return
        if abs((event.begin - last_event.end).total_seconds()) >= 3600:
            if isinstance(resource, Worker):
                event.workers.append(resource.id)
            else:
                event.resources.append(resource.id)
        resource.use_plan.append(event.id)

    # Compara los recursos y trabajadores entre dos eventos por el id y devuelve True si al menos un recurso 
    # de el 1er evento esta en el segundo
    @staticmethod
    def compare_event_resources(event_1: Event, event_2: Event) -> bool:
        return bool(set(event_1.workers + event_1.resources) & set(event_2.workers + event_2.resources))
    
    # Metodo para comprobar que los co-requicitos de los trabajadores esten en los recursos del evento
    @staticmethod
    def _check_co_requested(workers:list[Worker], resource:list[Resource], event: Event) -> bool:
        for wid in event.workers:
            wk = next((w for w in workers if w.id.lower() == wid.lower()), None)
            found = False
            for rid in event.resources:
                rs = next((r for r in resource if r.id.lower() == rid.lower()), None)
                if wk.co_requested.lower() == rs.name.lower():
                    found = True
                    break
            if not found:
                return False
        return True
    
    # Obtiene los ids de una lista de Resource que reciba
    @staticmethod
    def _get_ids(elems: list[Resource]):
        ids = []
        for e in elems:
            ids.append(e.id)
        return ids