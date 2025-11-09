from core.events import Event
from core.resource import Resource
from core.worker import Worker
from core.data_saved_loader import Data_saved_loader


# Clase encargada de recibir y cargar los nuevos eventos para asegurarse de que no tengan conflictos y cumplan las restrincciones 
# antes de ser guardados 
class Events_Planificator:
    def __init__(self):
        pass

    # Metodo para a Agendar un evento Creado por el usuario
    @staticmethod
    def Agg_Event(list_event:list[Event], event: Event):
        if Events_Planificator._check_resources(event.personal_requested, event.workers) and Events_Planificator._there_is_specialist_in_charge(event) and Events_Planificator._check_resources(event.resources_requested, event.resources) and Events_Planificator._check_co_requested(event):
            valid = True
            for e in list_event:
                if (Events_Planificator._conflict_event_begin(e, event) 
                    or abs((event.begin - e.begin).seconds) < 3600) and Events_Planificator.compare_event_resources(e, event):
                    valid = False
                    break
            if valid:
                list_event.append(event)
                Data_saved_loader.append_(event, "events")

    # metodo que me dice si dos eventos tienen la misa fecha de inicio
    @staticmethod
    def _conflict_event_begin(event_1:Event, event_2:Event):
        if event_1.begin == event_2.begin: return True
        return False
    
    # metodo que me dice si dos eventos terminan a la misma vez
    @staticmethod
    def _conflict_event_end(event_1:Event, event_2:Event):
        if event_1.end == event_2.end : return True
        return False

    # Metodo que comprueba que los recursos asignados (workers y resources) sean los requeridos
    # Restriccion 1
    @staticmethod
    def _check_resources(dic: dict, lis: list) -> bool:
        valid = False
        if len(dic) == 0 or len(lis) == 0:
            return valid
        elif len(dic) > len(lis):
            return valid
        if isinstance(lis[0],Worker): 
            for d in dic.keys():
                count = 0
                for l in lis:
                    if d.lower() == l.specialty.lower():
                        count += 1
                if count == dic[d]:
                    valid = True
                if not valid:
                    break
        else:
            for d in dic.keys():
                count = 0
                for l in lis:
                    if d.lower() == l.name.lower():
                        count += 1
                if count == dic[d]:
                    valid = True
                if not valid:
                    break
        return valid
    #  metodo auxiliar para comprobar que entre los empleados se encuentre el 
    #  encargado del evento
    @staticmethod
    def _there_is_specialist_in_charge(event: Event):
        for w in event.workers:
            if event.specialist_in_charge.lower() == w.specialty:
                return True
        return False

    # metodo para agregar los Co-requisitos a un evento
    @staticmethod
    def add_resource(event:Event):
        aux_w = Data_saved_loader.load_file_info("personal")
        aux_r = Data_saved_loader.load_file_info("resources")   
        dic_w = event.personal_requested.copy()
        dic_r = event.resources_requested.copy()
        counter = len(event.workers)

        for w in aux_w:
            if w.specialty in event.personal_requested.keys() and dic_w[w.specialty] > 0:
                Events_Planificator._add_resource_to_event(event, w)
                if counter < len(event.workers):
                    counter = len(event.workers)
                    dic_w[w.specialty] -= 1
        counter = len(event.resources)
        for r in aux_r:
            if r.name in event.resources_requested.keys() and dic_r[r.name] > 0:
                Events_Planificator._add_resource_to_event(event, r)
                if counter < len(event.resources):
                    counter = len(event.resources)
                    dic_r[r.name] -= 1

    # Metodo auxiliar para agregar un recurso a un evento
    @staticmethod
    def _add_resource_to_event(event: Event, resource: Resource):
        if len(resource.use_plan) == 0 or abs((resource.use_plan[len(resource.use_plan) - 1].end.to - event.begin).total_seconds()) < 3600:
            if type(resource) == Worker:
                event.workers.append(resource)
            else:
                event.resources.append(resource)
            resource.use_plan.append(event)
            resource.use_plan.sort()

    # Compara los recursos y trabajadores entre dos eventos por el id y devuelve True si al menos un recurso 
    # de el 1er evento esta en el segundo
    @staticmethod
    def compare_event_resources(event_1: Event, event_2: Event) -> bool:
        ids_1 = Events_Planificator._get_ids(event_1.workers) + Events_Planificator._get_ids(event_1.resources)
        ids_2 = Events_Planificator._get_ids(event_2.workers) + Events_Planificator._get_ids(event_2.resources)

        for id in ids_1:
            if id in ids_2:
                return True            
        return False
    
    # Metodo para comprobar que los co-requicitos de los trabajadores esten en los recursos del evento
    @staticmethod
    def _check_co_requested(event: Event) -> bool:
        counter = 0
        for w in event.workers:
            for r in event.resources:
                if w.co_requested.lower() == r.name.lower():
                    counter += 1
        if counter == len(event.workers):
            return True
        return False
    
    # Obtiene los ids de una lista de Resource que reciba
    @staticmethod
    def _get_ids(elems: list[Resource]):
        ids = []
        for e in elems:
            ids.append(e.id)
        return ids