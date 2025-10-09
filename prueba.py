from core.resource import Resource
from core.events import Event
from core.restriction import Restriction
from core.events_planificator import Events_Planificator

r = Resource("Q1", "Quirofano 1", "material", False, {})
# print(r)
m = Resource("M1", "Dr.Sanchez", "personal","especulo", False, {"specialty": "genecologo"})
m1 = Resource("M1", "Dr.Perez", "personal", "electro", False, {"specialty": "cardiologo"})
# print(m)
e = Event("e1", "Operacion de Corazon", 1, "cardiologo", (2025,10,10),(2025,10,11), False,[m,m1], [r])
# print(e)
re = Restriction()
print(re._there_is_only_specialist_in_charge(e))
ep = Events_Planificator([])
print(ep)