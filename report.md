# Sistema de Planificación Inteligente de Eventos 

**Título del proyecto:** Sistema de Planificación Inteligente de Eventos
**Autor:** Dayan Rodríguez Pérez
**Grupo:** C-121
**Carrera:** Ciencias de la Computación
**Institución:** Universidad de La Habana
**Asignatura:** Programación

## Resumen
El presente proyecto consiste en el desarrollo de un sistema de planificación de eventos capaz de gestionar de forma inteligente la asignación de personal y recursos médicos, evitando conflictos de horarios y violaciones de restricciones. El sistema permite crear eventos, validar su viabilidad, asignar automáticamente trabajadores y recursos disponibles, y buscar el próximo intervalo de tiempo libre en función de los recursos necesitados y una duración dada. Además, incorpora persistencia de datos mediante archivos JSON y una interfaz gráfica interactiva que facilita la gestión de la información.

## Introducción
La planificación de eventos en entornos donde intervienen múltiples recursos y personal especializado es un problema complejo, especialmente cuando se deben respetar restricciones de disponibilidad y evitar solapamientos. En contextos como el sector de la salud, una mala planificación puede generar conflictos, retrasos o un uso ineficiente de los recursos.

Este proyecto surge con el objetivo de ofrecer una solución software que permita gestionar de manera organizada y automática la creación de eventos, asignando correctamente trabajadores y recursos según su disponibilidad y especialidad, y garantizando la consistencia de la información almacenada.

## Que hace el programa: 
El programa le permite al usuario crear, eliminar, visualizar, ver detalles de los eventos, trabajadores y recursos que posee el dominio(Hospital), representados con las clases Domain.py, Event.py, Worker.py y Resource.py. La información se guarda permanentemente usando archivos .JSON a través de la clase Data_save_loader.py. El programa cuenta con un menú inteligente que facilita el completado de los nombres de recursos y especialidades médicas, además de tener una función "def find_next_avialable_slot()" que completa de automáticamente con una fecha viable para el evento que se este creando en función de la duración y los recursos necesitados, evitando un conflicto de fechas.

## Cómo lo diseñaste y por qué tomaste las decisiones que tomaste
El sistema fue diseñado siguiendo una estructura modular facilitando la escalavilidad del proyecto, cada clase y módulo tiene una tarea bien definida por ejemplo:
- **Event:** representa un evento con fecha de inicio, fin, personal y recursos asignados.
- **Worker:** representa a un trabajador con una especialidad y un plan de uso.
- **Resource:** representa un recurso material con su propio plan de uso.
- **Domain:** contiene la lógica central del sistema, incluyendo la búsqueda de huecos disponibles.
- **Events\_Planificator:** se encarga de la asignación de recursos y personal a los eventos.
- **Data\_saved\_loader:** gestiona la carga y guardado de información en archivos JSON.

Además esto permite la reutilización del códico.

## Qué aprendiste durante el desarrollo:

Durante al desarrollo del proyecto aprendí como guardar información de manera permanente usando archivos .JSON. A crear proyectos escalables y código reutilizable, además de crear interfaces gráficas usando la librería Flet.

## Cómo se usa el programa (con ejemplos)

## Ejemplo 1: Crear un Evento

### Acción del usuario
1. Abrir **Events → Create Event**.
2. Introducir el nombre del evento.
3. Seleccionar el especialista responsable.
4. Definir fecha y hora de inicio y fin.
5. Añadir personal y recursos necesarios.
6. Pulsar **Create Event** y luego **Save**.

### Código responsable

```python
create_event_btn = ft.ElevatedButton(
    "Create Event",
    on_click=lambda e, ctr=specialist_in_charge:
        Create_Utils._create_event(
            page,
            ctr,
            dom,
            event_name.value,
            specialist_in_charge.value,
            b_y.value,
            b_m.value,
            b_d.value,
            b_h.value,
            b_min.value,
            e_y.value,
            e_m.value,
            e_d.value,
            e_h.value,
            e_min.value,
            is_emergency.value,
            Create_Utils._get_values_from_column(personal_col),
            Create_Utils._get_values_from_column(resource_col),
            save_event_btn
        )
)
```

## Ejemplo 2: Buscar una fecha valída para un evento

### Acción del usuario
1. Abrir **Events → Create Event**.
2. Introducir la duracíon del evento y los recursos necesarios para este.
3. Click en el **Find Slot**.

```python
def find_next_avialable_slot(
                self, personal_req:dict, 
                resource_req:dict, 
                duration:timedelta,
                step_minutes: int = 15) ->tuple[datetime, datetime]:
    current_start = datetime.now().replace(second=0, microsecond=0)
        
        events = sorted(self.events, key=lambda e: e.begin)

        while True:
            candidate_end = current_start + duration

            conflict = False

            for e in events:
                if e.end <= current_start or e.begin >= candidate_end:
                    continue
                for role, qty in personal_req.items():
                    if role in e.personal_requested:
                        conflict = True
                        break
                for res, qty in resource_req.items():
                    if res in e.resources_requested:
                        conflict = True
                        break
                if conflict:
                    break
            if not conflict:
                return current_start, candidate_end
            current_start += timedelta(minutes=step_minutes)            
```

## Ejemplo 3: Eliminar eventos con fecha de finalización menor que la fecha actual de forma automatica

```python
def update_events(self):
        now = datetime.now()
        if len(self.events) > 0:
            for e in list(self.events): # trabajamos con una copia de self.events para evitar problemas al eliminar elementos mientras iteramos
                if (e.end - now).total_seconds() <= 0:
                    self.event_to_delete.add(e.id)
            self.persist_deletions()
```

## Dificultades que encontraste y cómo las resolviste

1. Guardado y Consulta de la informcion creando bucles recursivos:
En principio los eventos tenían una lista de trabajadores y recursos, los que estan asignados al evento, y estos a su vez tenían una lista de eventos, el plan de uso de cada uno, entonces al guardar un evento en un JSON se creaba un diccionario donde un de sus valores era una lista de trabajadores, estos tenían una lista de eventos donde uno de ellos es el evento mencionado anteriormente, que tiene anidado el trabajador, lo cual creaba un bucle infinito. La solución de este problema fue sustituir la lista de eventos, trabajadores, recursos, por listas de str en los JSON donde se almacenaban los ids de los eventos, trabajadores y recursos. premitiendo guardar la referencia de cada elemento para recontrir el evento, trabajador, recurso una vez sea cargado del JSON.