from core.resource import Resource
from core.events import Event
from core.restriction import Restriction
from core.events_planificator import Events_Planificator
from core.data_saved_loader import Data_saved_loader

# r = Resource("Q1", "Quirofano 1", "material", False, {})
# # print(r)
m = Resource("m1", "Dr.Sanchez", "personal","especulo", False, {"specialty": "genecologo"})
# m1 = Resource("M1", "Dr.Perez", "personal", "electro", False, {"specialty": "cardiologo"})
# # print(m)
# e = Event("e1", "Operacion de Corazon", 1, "cardiologo", (2025,10,10),(2025,10,11), False,[m,m1], [r])
# # print(e)
# re = Restriction()
# # print(re._there_is_only_specialist_in_charge(e))
# ep = Events_Planificator([])
# # print(ep)

# personal = Data_saved_loader.load_nurses()
# # print(personal)
# n1 = Resource(personal[0]["id"], personal[0]["name"], personal[0]["type"], personal[0]["co_requested"], personal[0]["is_on_use"], personal[0]["attributes"])
# # print(n1)
# print()

# Data_saved_loader.append_employee(m)
# personal = Data_saved_loader.load_personal()
# print(personal)
# for p in personal["personal"]:
    # print(p["id"])
# print(Data_saved_loader.append_employee(m))
# Data_saved_loader.append_resource(m, Data_saved_loader.load_resources())
Data_saved_loader.remove_resource(Data_saved_loader.load_resources(),0)
print(Data_saved_loader.load_resources())