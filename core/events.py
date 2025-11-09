from dataclasses import dataclass, field
from datetime import datetime
from core.resource import Resource
from core.worker import Worker

@dataclass
class Event:
    id: str
    name: str
    personal_requested: dict
    resources_requested: dict
    specialist_in_charge: str
    begin: datetime
    end: datetime
    is_emergency: bool
    workers: list[Worker] = field(default_factory = list)
    resources: list[Resource] = field(default_factory = list)

    def show_details(self, *args) -> str:
        # diccionario con los valores de los posibles parametros a mostrar
        fields = {
            "id": lambda: f"id: {self.id}\n",
            "name": lambda: f"name: {self.name}\n",
            "personal_requested": lambda: "Personal solicitado:\n" + self._show_requested(self.personal_requested),
            "resources_requested": lambda: "Recursos solicitados:\n" + self._show_requested(self.resources_requested),
            "specialist_in_charge": lambda: f"Especialista a cargo: {self.specialist_in_charge}\n",
            "begin": lambda: f"Inicio: {self.begin}\n",
            "end": lambda: f"Fin: {self.end}\n",
            "is_emergency": lambda: f"Emergencia: {self.is_emergency}\n",
            "workers": lambda: "Workers:\n" + "".join([w.show_details() + "\n" for w in self.workers]),
            "resources": lambda: "Resources:\n" + "".join([r.show_details() + "\n" for r in self.resources]),
        }
        # si no hay argumentos los devolvemos todos
        if not args:
            return "".join([func() for func in fields.values()])
        # si se pasan argumentos solo mostras esos argumentos 
        details = ""
        for arg in args:
            k = arg.lower()
            if k in fields.keys():
                details += fields[arg]()
            else:
                details += "[Advertencia] El campo solicitado no existe\n"
        return details
    # funcion para mostrar los requested
    def _show_requested(self, requested: dict) -> str:
        return "".join([f"{key} : {value}\n" for key, value in requested.items()])