from core.events import Event
from core.resource import Resource
from core.restriction import Restriction

# Clase encargada de recibir y cargar los nuevos eventos para asegurarse de que no tengan conflictos y cumplan las restrincciones 
# antes de ser guardados 
class Events_Planificator:
    def __init__(self, events:list[Event]):
        self.events:list[Event] = events
    
    def __repr__(self):
        return f"{self.events}"
    