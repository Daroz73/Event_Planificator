import json
from core.resource import Resource
from core.events import Event

# Clase encargada de cargar y guardar la info de los eventos 
class Data_saved_loader:
    def __init__(self):
        pass

    # Metodo para cargar todo el personal del hospital
    @staticmethod
    def load_file(file_name:str):
        with open("data/"+f"{file_name}.json", "r", encoding="utf-8") as f:
            info = json.load(f)
        return info

    # Revisa si el empleado recibido esta ya registrado en el hospital
    @staticmethod
    def check_elements_by_id(elem, elements):
        for e in elements:
            if e.id == elem["id"]:
                return True
        return False
    
    # metodo para agregar nuevos empleados al archivo .json
    @staticmethod
    def append_(element, list, file_name:str):
        new_elem = Data_saved_loader.format_to_json(element)
        list.append(new_elem)
        with open("data/"+f"{file_name}.json", "w", encoding="utf-8") as f:
            json.dump(list, f, indent=4, ensure_ascii=False)
            
    # Metodo para elminiar el ultimo empleado
    def pop_(elements, file_name:str):
        elements.pop_()
        with open("data/"+f"{file_name}.json", "w", encoding="utf-8") as f:
            json.dump(elements, f, indent=4, ensure_ascii=False)
    
    # metodo para remover un empleado
    def remove_(elements, ident: int | str, file_name):
        aux_elems = []
        if type(ident) == int and 0 <= ident < len(elements):
            for i in range(ident):
                aux_elems.append(elements[i])
            for i in range(ident+1, len(elements)):
                aux_elems.append(elements[i])
            with open("data/"+f"{file_name}.json", "w", encoding="utf-8") as f:
                json.dump(aux_elems, f, indent=4, ensure_ascii=False)
        elif type(ident) == str:
            for emp in elements:
                if emp["id"] != ident:
                    aux_elems.append(emp) 
            with open("data/"+f"{file_name}.json", "w", encoding="utf-8") as f:
                json.dump(aux_elems, f, indent=4, ensure_ascii=False)
    
    # metodo para convertir un Resource en un dicionario para poder almacenarlo en un JSON
    def _format_resource_to_json(element):
        json_element = {
                "id":f"{element.id}",
                "name":f"{element.name}", 
                "type":f"{element.type}",
                "co_requested":f"{element.co_requested}",
                "is_on_use":f"{element.is_on_use}",
                "attributes":{}
            }
        for k in element.attributes.keys():
            json_element["attributes"][k] = element.attributes[k]
        return json_element
    
    # metodo para convertir un event en un formato valido para un JSON
    def _format_event_to_json(event):
        new_event = {
                "id" : f"{event.id}",
                "name" : f"{event.name}",
                "personal_requested" : f"{event.personal_requested}",
                "specialist_in_charge": f"{event.specialist_in_charge}",
                "begin":f"{event.begin}",
                "end":f"{event.end}",
                "is_emergency":f"{event.is_emergency}",
                "personal":[],
                "resources":[]
            }
        for p in event.personal:
            new_event["personal"].append(Data_saved_loader._format_resource_to_json(p))
        for r in event.resources:
            new_event["resources"].append(Data_saved_loader._format_resource_to_json(r))
        return new_event
    
    # metodo para convertir un Objeto(event, resource) en un formato valido para almacenarlo en un JSON
    def format_to_json(element):
        new_elem = None
        if type(element) == Resource:
            new_elem = Data_saved_loader._format_resource_to_json(element)
        else:
            new_elem = Data_saved_loader._format_event_to_json(element)
        return new_elem
