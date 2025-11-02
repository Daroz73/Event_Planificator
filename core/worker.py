from dataclasses import dataclass
from core.resource import Resource

@dataclass
class Worker(Resource):
   specialty: str = "enfermero"
