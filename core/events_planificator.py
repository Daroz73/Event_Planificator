from core.events import Event
from core.resource import Resource
from core.restriction import Restriction
from core.data_saved_loader import Data_saved_loader


# Clase encargada de recibir y cargar los nuevos eventos para asegurarse de que no tengan conflictos y cumplan las restrincciones 
# antes de ser guardados 
class Events_Planificator:
    def __init__(self):
        pass
    
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

    # metodo que verifica si el evento cumple el co-requisito de cada recurso
    # @staticmethod
    # def _check_co_requested(event:Event):
    #     for p in event.personal:
    #         for i in range(len(event.personal)):
    #             if p["id"] != event.personal[i]["id"] and p.co_requested == event.personal[i]["name"]:
    #                 return True
    #         for j in range