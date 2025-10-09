from core.events import Event
from core.resource import Resource

# Pendientes
# Crear una restriccion para que un evento tenga asignado un solo especialista
class Restriction:
    def __init__(self):
        pass
    
    def right_resource(self, event):
        pass

    # Comprueba que se encuentre el co-requisito de cada recurso
    def check_resource_co_requested(self, event):
        return self._check_personal_co_requested(event) and self._check_resources_co_requested(event)
    
    def __check_personal_co_requested(self, event):
        pass

    def _check_resources_co_requested(self, event):
        pass

    # Chequea que el evento tenga especialisra encargado
    def _there_is_specialist_in_charge(self, event):
        for people in event.personal:
            if people.attributes["specialty"] == event.specialist_in_charge: return True
        return False
    
    # Comprueba si el evento posee un solo especialista encargado
    def _there_is_only_specialist_in_charge(slef, event):
        counter = 0
        for people in event.personal:
            if people.attributes["specialty"] == event.specialist_in_charge:
                counter += 1
        if counter == 1: return True
        return False
    
    # Comprueba si hay recursos
    def _there_is_resource(slef, event):
        return len(event.personal) == event.personal_requested and 0 < len(event.resources) 