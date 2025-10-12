import json


# Clase encargada de cargar y guardar la info de los eventos 
class Data_saved_loader:
    def __init__(self):
        pass

    # Metodo para cargar todo el personal del hospital
    @staticmethod
    def load_personal():
        with open("data/personal.json", "r", encoding="utf-8") as f:
            personal = json.load(f)
        return personal

    @staticmethod
    def load_resources():
        with open("data/resources.json", "r", encoding="utf-8") as f:
            resources = json.load(f)
        return resources
    
    # Revisa si el empleado recibido esta ya registrado en el hospital
    @staticmethod
    def check_employee(emp, employees):
        for em in employees:
            if emp.id == em["id"]:
                return True
        return False
    
    # metodo para agregar nuevos empleados al archivo .json
    @staticmethod
    def append_employee(emp,employees):
        new_emp = {
            "id":f"{emp.id}",
            "name":f"{emp.name}", 
            "type":"personal",
            "co_requested":f"{emp.co_requested}",
            "is_on_use":f"{emp.is_on_use}",
            "attributes":{}
        }
        for k in emp.attributes.keys():
            new_emp["attributes"][k] = emp.attributes[k]
        employees.append(new_emp)
        with open("data/personal.json", "w", encoding="utf-8") as f:
            json.dump(employees, f, indent=4, ensure_ascii=False)
        
    # metodo para agregar nuevos recursos al archivo .json
    @staticmethod
    def append_resource(re, resources):
        new_re = {
            "id":f"{re.id}",
            "name":f"{re.name}",
            "type":"material",
            "co_requested":f"{re.co_requested}",
            "is_on_use":f"{re.is_on_use}",
            "attributes":{}
        }
        for k in re.attributes.keys():
            new_re["attributes"][k] = re.attributes[k]
        
        resources["resources"].append(new_re)

        with open("data/resources.json", "w", encoding="utf-8") as f:
            json.dump(resources, f, indent=4, ensure_ascii=False)

    # Metodo para elminiar el ultimo empleado
    def pop_employee(employees):
        employees.pop()
        with open("data/personal.json", "w", encoding="utf-8") as f:
            json.dump(employees, f, indent=4, ensure_ascii=False)
    
    # metodo para remover un empleado
    def remove_employee(employees, index: int | str):
        aux_employees = []
        if type(index) == int and 0 <= index < len(employees):
            for i in range(index):
                aux_employees.append(employees[i])
            for i in range(index+1, len(employees)):
                aux_employees.append(employees[i])
            with open("data/personal.json", "w", encoding="utf-8") as f:
                json.dump(aux_employees, f, indent=4, ensure_ascii=False)
        elif type(index) == str:
            for emp in employees:
                if emp["id"] != index:
                    aux_employees.append(emp) 
            with open("data/personal.json", "w", encoding="utf-8") as f:
                json.dump(aux_employees, f, indent=4, ensure_ascii=False)
        
    # metodo para eliminar el ultimo recurso
    def pop_resource(employees):
        employees.pop()
        with open("data/resources.json", "w", encoding="utf-8") as f:
            json.dump(employees, f, indent=4, ensure_ascii=False)

    # metodo para remover un recurso
    def remove_resource(resources, index: int | str):
        aux_resources = []
        if type(index) == int and 0 <= index < len(resources):
            for i in range(index):
                aux_resources.append(resources[i])
            for i in range(index+1, len(resources)):
                aux_resources.append(resources[i])
            with open("data/resources.json", "w", encoding="utf-8") as f:
                json.dump(aux_resources, f, indent=4, ensure_ascii=False)
        elif type(index) == str:
            for emp in resources:
                if emp["id"] != index:
                    aux_resources.append(emp)
            with open("data/resources.json", "w", encoding="utf-8") as f:
                json.dump(aux_resources, f, indent=4, ensure_ascii=False)