from core.resource import Resource
from core.events import Event
from core.worker import Worker
from core.events_planificator import Events_Planificator
from core.data_saved_loader import Data_saved_loader
from datetime import datetime, timedelta
from core.domain import Domain


workers = [
    Worker("M1", "Yoly Sanchez","especulo", [], "ginecologo"),
    Worker("M2", "Dayan Rodriguez", "laptop", [], "biomedico"),
    Worker("M3", "Darian Rodriguez", "electro", [],"cardiologo"),
    Worker("E4", "Loraimis Villavicencio", "microscopio", [], "enfermero"),
    Worker("E5", "Ana Carla", "geringua", [], "enfermero"),
    Worker("E6", "Daniela", "duragina", [], "enfermero"),
    Worker("M7", "Ernesto Castillo", "cuchilla", [], "cirujano"),
    Worker("M8", "Barbaro Fuentes", "martillo", [], "ortopedico"),
    Worker("E9", "Alejandra Vazques", "lapicero", [], "enfermero"),
    Worker("E10", "Elber Galarga", "recetas", [], "enfermero"),
]

resources = [
    Resource("R1", "cuchilla", "cirujano"),
    Resource("R2", "Sala de cirugía 2", "Sala"),
    Resource("R3", "lapicero", "Equipo"),
    Resource("R4", "Ecógrafo portátil", "Equipo"),
    Resource("R5", "Ambulancia 1", "Vehículo"),
    Resource("R6", "Ambulancia 2", "Vehículo"),
    Resource("R7", "Monitor cardíaco", "Equipo"),
    Resource("R8", "Sala de recuperación", "Sala"),
    Resource("R9", "Ventilador mecánico", "Equipo"),
    Resource("R10", "recetas", "Sala"),
    Resource("Q1", "Quirofano", "enfermero",{})
]

events = [
    Event("E1", "Cirugía de apendicitis", {"cirujano": 1, "enfermero": 2}, {"Quirofano":1, "anestesia":4, "cuchilla":8, "lapicero":2 ,"recetas":2}, "cirujano",
          datetime.now(), datetime.now() + timedelta(hours=2), False, [workers[6], workers[8], workers[9]], [resources[0], resources[2], resources[9]]),
    Event("E2", "Parto programado", [["Dra. García", "enfermera 2"]], [["R2", "R8"]], "Dra. García",
          datetime.now() + timedelta(hours=3), datetime.now() + timedelta(hours=6), False, [], [resources[1], resources[7]]),
    Event("E3", "Traslado de paciente crítico", [["Paramédico 1", "Paramédico 2"]], [["R5"]], "Dr. Méndez",
          datetime.now(), datetime.now() + timedelta(hours=1), True, [], [resources[4]]),
    Event("E4", "Cirugía cardíaca", [["Dr. Pérez", "enfermera 3"]], [["R10", "R7"]], "Dr. Pérez",
          datetime.now() + timedelta(days=1), datetime.now() + timedelta(days=1, hours=5), False, [], [resources[9], resources[6]]),
    Event("E5", "Ecografía abdominal", [["Técnico 1"]], [["R4"]], "Dr. Ruiz",
          datetime.now() + timedelta(hours=2), datetime.now() + timedelta(hours=3), False, [], [resources[3]]),
    Event("E6", "Examen de rayos X", [["Técnico 2"]], [["R3"]], "Dr. Ruiz",
          datetime.now() + timedelta(hours=4), datetime.now() + timedelta(hours=5), False, [], [resources[2]]),
    Event("E7", "Emergencia UCI", [["Dr. Soto", "enfermera 4"]], [["R9", "R8"]], "Dr. Soto",
          datetime.now() + timedelta(hours=1), datetime.now() + timedelta(hours=4), True, [], [resources[8], resources[7]]),
    Event("E8", "Cirugía ortopédica", [["Dr. Lara", "enfermera 5"]], [["R1", "R10"]], "Dr. Lara",
          datetime.now() + timedelta(days=2), datetime.now() + timedelta(days=2, hours=6), False, [], [resources[0], resources[9]]),
    Event("E9", "Consulta externa", [["Dr. Gómez"]], [["R8"]], "Dr. Gómez",
          datetime.now() + timedelta(hours=8), datetime.now() + timedelta(hours=9), False, [], [resources[7]]),
    Event("E10", "Prueba de ventilador", [["Técnico 3"]], [["R9"]], "Dr. Ramos",
          datetime.now() + timedelta(hours=5), datetime.now() + timedelta(hours=6), False, [], [resources[8]]),
]

dom = Domain()
new_ev = Event("E2", "Chequeo", { "enfermero": 2}, {"Quirofano":1,}, "enfermero",
          datetime.now(), datetime.now() + timedelta(hours=6), False, [workers[6], workers[8], workers[9]], [resources[10], resources[0], resources[2], resources[9]])
dom.add_event(new_ev)
for e in dom.events:
      print(e.name)
print(" ")
# dom.remove_event("e2")
# for e in dom.events:
#       print(e.name)
print(dom.show_details("e2","name","workers"))