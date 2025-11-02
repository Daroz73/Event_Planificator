import json
from datetime import datetime
from core.resource import Resource
from core.worker import Worker
from core.events import Event
 

# Clase encargada de cargar y guardar la info de los eventos 
class Data_saved_loader:
    def __init__(self):
        pass

    # metodo para devolver un lista de elementos cargados de un .json
    @staticmethod
    def load_file_info(file_name: str) -> list:
        aux_list = Data_saved_loader._load_file(file_name)
        lis = []
        if len(aux_list) > 0:
            for ele in aux_list:
                if file_name.lower() == "events":
                    lis.append(Data_saved_loader._format_json_to_event(ele))
                else:
                    lis.append(Data_saved_loader._format_json_to_resource(ele))
        return lis

    # Metodo para cargar la info de un archivo .json
    @staticmethod
    def _load_file(file_name:str):
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
    
    # metodo para agregar nuevos objetos al archivo .json
    @staticmethod
    def append_(element, list, file_name:str):
        new_elem = Data_saved_loader.format_to_json(element)
        list.append(new_elem)
        with open("data/"+f"{file_name}.json", "w", encoding="utf-8") as f:
            json.dump(list, f, indent=4, ensure_ascii=False)
            
    # Metodo para elminiar el ultimo objeto
    def pop_(elements, file_name:str):
        elements.pop_()
        with open("data/"+f"{file_name}.json", "w", encoding="utf-8") as f:
            json.dump(elements, f, indent=4, ensure_ascii=False)
    
    # metodo para remover un objeto
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
    def _format_resource_to_json(element: Resource):
        json_element = {
                "id":f"{element.id}",
                "name":f"{element.name}", 
                "co_requested":f"{element.co_requested}",
                "use_plan":[]
            }
        if element.isinstance(Worker):
            json_element["specialty"] = element.specialty
        for e in element.use_plan:
            json_element["use_plan"].append(Data_saved_loader._format_event_to_json(e))
        return json_element
    
    # metodo para convertir un event en un formato valido para un JSON
    def _format_event_to_json(event:Event):
        new_event = {
                "id" : f"{event.id}",
                "name" : f"{event.name}",
                "personal_requested" : event.personal_requested,
                "resources_requested": event.resources_requested,
                "specialist_in_charge": f"{event.specialist_in_charge}",
                "begin":f"{event.begin}",
                "end":f"{event.end}",
                "is_emergency":f"{event.is_emergency}",
                "workers":[],
                "resources":[]
            }
        for p in event.workers:
            new_event["workers"].append(Data_saved_loader._format_resource_to_json(p))
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

    # metodo para convertir un formato json a un Event
    @staticmethod
    def _format_json_to_event(event):
        return Event(
            id=event.get("id", ""),
            name=event.get("name",""),
            personal_requested=event.get("personal_requested",{}),
            resources_requested=event.get("resources_requested",{}),
            specialist_in_charge=event.get("specialist_in_charge","enfermero"),
            begin=Data_saved_loader._safe_parse_date(event.get("begin")), # convertir de string a datatime
            end=Data_saved_loader._safe_parse_date(event.get("end")), # convertir de string a datatime
            is_emergency=event.get("is_emergency", False),
            workers=Data_saved_loader._safe_parse_list(event.get("workers",[])),
            resources=Data_saved_loader._safe_parse_list(event.get("resources",[]))
            )
    
    # metodo auxiliar para asegurar que las listas de resources se carguen correctamente
    @staticmethod
    def _safe_parse_list(value) -> list[Resource]:
        lis = []
        if not value:
            return lis
        for val in value:
            lis.append(Data_saved_loader._format_json_to_resource(val))
        return lis

    # metodo auxiliar para garantizar que las fechas de los json se carguen como datetime
    @staticmethod
    def _safe_parse_date(value, default_date=datetime.now()) -> datetime:
        if not value:
            return default_date
        if isinstance(value, datetime):
            return value
        return datetime.fromisoformat(value)

    # metodo para convertir de formato json a Worker o Resource
    @staticmethod
    def _format_json_to_resource(element):
        if "specialty" in element.keys():
            return Worker (element.get("id",""),
                           element.get("name", ""),
                           element.get("co_requested", ""),
                           element.get("use_plan", []),
                           element.get("specialty", "enfermero"))
        
        return Resource(element.get("id",""),
                        element.get("name", ""),
                        element.get("co_requested", ""),
                        element.get("use_plan", []))