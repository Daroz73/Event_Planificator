from dataclasses import dataclass
from core.resource import Resource

@dataclass
class Worker(Resource):
   specialty: str = "enfermero"

   # metodo para mostrar los detalles del worker
   def show_details(self, *args) -> str:
      details = ""
      details += super()._show_details(*args)
      if "specialty" in args:
         details += f"specialty: {self.specialty}"
      return details