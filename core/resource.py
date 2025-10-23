from dataclasses import dataclass, field

@dataclass
class Resource:
    # debido a la clase dataclass se crea un constructor por defecto,
    # premitiendo que omitamos declararlo nosotros y asignarlo al atributo self
    id: str
    name: str
    co_requested: str
    use_plan: list = field(default_factory = list)
