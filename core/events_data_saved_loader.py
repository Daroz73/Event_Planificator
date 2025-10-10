import json


# Clase encargada de cargar y guardar la info de los eventos 
class Event_data_saved_loader:
    def __init__(self):
        pass

    @staticmethod
    def load_personal():
        with open("data/personal.json", "r") as f:
            personal = json.load(f)
        return personal
    
    @staticmethod
    def load_doctors():
        with open("data/personal.json", "r") as f:
            doctors = json.load(f)["doctors"]
        return doctors

    @staticmethod
    def load_nurses():
        with open("data/personal.json", "r") as f:
            nurses = json.load(f)["nurses"]
        return nurses