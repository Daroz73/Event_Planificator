from dataclasses import dataclass, field

@dataclass
class Resource:
    # debido a la clase dataclass se crea un constructor por defecto,
    # premitiendo que omitamos declararlo nosotros y asignarlo al atributo self
    id: str
    name: str
    co_requested: str
    use_plan: list[str] = field(default_factory = list)

    # funcion para mostrar los detalles de los resources
    def _show_details(self, *args) -> str:
        fields = {
            "id": lambda: f"id: {self.id}",
            "name": lambda: f"name: {self.name}",
            "co_requested": lambda: f"co_requested: {self.co_requested}",
            "use_plan": lambda: f"use plan:\n{self._show_use_plan()}"
        }
        details = ""
        if not args:
            return " ".join([func() for func in fields.values()])
        else:
            for ar in args:
                k = ar.lower()
                if k in fields.keys():
                    details += fields[k]
        return details
    # metodo para mostrar el plan de uso del recurso
    def _show_use_plan(self) -> str:
        return ["".join([f"id: {e.id} name: {e.name}\n" for e in self.use_plan])]