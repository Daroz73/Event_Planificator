from core.events import Event
from core.resource import Resource
from core.restriction import Restriction
from core.events_planificator import Events_Planificator
from core.data_saved_loader import Data_saved_loader


action = 0

while action != 3:
    print("Que accion desea realizar: ")
    print("1- Contratar empleado")
    print("2- Crear Evento")
    print("3- Despedir un empleado")
    print("4- exit")
    action = int(input())

    if(action == 1):
        id_emp = input("Introduzca el id: ")
        name_emp = input("Introduzca el name: ")
        co_requested = input("Intrpduce el co_requested: ")
        esp_emp = input("Introduzca la especialidad del empleado: ")
        new_emp = Resource(id_emp, name_emp,"personal", co_requested, False, {"specialty": esp_emp})
        Events_Planificator.hire_employee(new_emp)
        print(Data_saved_loader.load_file())
    elif action == 4:
        id = input("Introduzca el id o index del empleado que queire despedir: ")
        personal = Data_saved_loader.load_file()
        counter = 0
        for p in  personal:
            print(f"{counter}- {p}")
            counter += 1
        index = input()
        Data_saved_loader.remove_(personal,index)
        print(Data_saved_loader.load_file())
