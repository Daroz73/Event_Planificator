from core.events import Event
from core.resource import Resource
from core.restriction import Restriction
from core.data_saved_loader import Data_saved_loader


# Clase encargada de recibir y cargar los nuevos eventos para asegurarse de que no tengan conflictos y cumplan las restrincciones 
# antes de ser guardados 
class Events_Planificator:
    def __init__(self, events:list[Event]):
        self.events:list[Event] = events
    
    def __repr__(self):
        return f"{self.events}"
    
    def hire_employee(emp):
        employees = Data_saved_loader.load_personal()
        if not Data_saved_loader.check_employee(emp,employees):
            Data_saved_loader.append_employee(emp, employees)
            print("El empleado fue contratado")
        else:
            print("El empleado ya se encuentra trabajando con nosotros")
    def dismiss_employee(emp):
        employees = Data_saved_loader.load_personal()
        Data_saved_loader.remove_employee(employees,emp["id"])