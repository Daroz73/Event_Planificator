from dataclasses import dataclass, field

@dataclass
class Resource:
    # debido a la clase dataclass se crea un constructor por defecto,
    # premitiendo que omitamos declararlo nosotros y asignarlo al atributo self
    id: str
    name: str
    type: str
    co_requested: str
    is_on_use: bool
    attributes: dict = field(default_factory = dict)

    def __repr__(self):
        return f"Recurso: name: {self.name}, type: {self.type}, attributes: {self.attributes}"
