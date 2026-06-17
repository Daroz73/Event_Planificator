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
El programa le permite al usuario crear, eliminar, visualizar, ver detalles de los eventos, trabajadores y recursos que posee el dominio(Hospital), representados con las clases Domain.py, Event.py, Worker.py y Resource.py. La información se guarda permanentemente usando archivos .JSON a través de la clase Data_save_loader.py. El programa cuenta con un menú inteligente que facilita el completado de los nombres de recursos y especialidades médicas, además de tener una función ```def find_next_avialable_slot()``` que completa de automáticamente con una fecha viable para el evento que se este creando en función de la duración y los recursos necesitados, evitando un conflicto de fechas.

## Cómo lo diseñaste y por qué tomaste las decisiones que tomaste
El sistema fue diseñado siguiendo una estructura modular facilitando la escalavilidad del proyecto, cada clase y módulo tiene una tarea bien definida por ejemplo:
Cree las clases Event, Worker y Resource para representar las entidades más "básicas" del proyecto:
- **Event:** representa un evento, contiene toda la información de dicha entidad, fecha de inicio, fin, personal y recursos asignados entre otros.
- **Worker:** representa a un trabajador, contiene toda la información de este como una especialidad y un plan de uso(eventos en los que participa).
- **Resource:** representa un recurso material, contiene la información de este como su propio plan de uso(eventos en los que se usa) y especialista que pueden usarlo. En la gerarquía de herencia es el padre de Worker(tiene sentido teniendo en cuenta que un trabajador es un recurso humano).
Para el manejo y gestión de la información cree la clase Domain junto con otras clases  que son llamados por la misma para realizar tareas específicas.
- **Domain:** contiene la lógica central del sistema, es la conoce toda la información como eventos planificados, trabajadores y recursos, además de la búsqueda de huecos disponibles.
- **Events\_Planificator:** es llamada por  Domain para realizar la asignación de recursos y personal a los nuevos eventos que se quieren crear por el usuario.
- **Data\_saved\_loader:** es usada por Domain para gestionar la carga y guardado de información en archivos JSON, contiene todas las funciones necesarias para dichas tareas.
En la carpeta GUI se encuentrar todas los módulos encargados de la visualización de la información en la UI.
- **Create\_Utils:** contiene todos los métodos encargados de la creación de entidades(Eventos, Trabajadores, Recursos) desde la UI.
- **Creation\_Validate:** es la encargada de comprobar que la información que da el usuario desde la UI es válida antes de ver si la misma cumple las restricciones del dominio.
- **Delete_Utils:** es la encargada de eliminar la informacion visual de la UI.
- **Visual_Utils:** contiene las funciones encargadas de crear los elementos visuales para mostrar en la UI.

La modularización usada permite la reutilización del códico.

## Qué aprendiste durante el desarrollo:

Durante al desarrollo del proyecto aprendí como guardar información de manera permanente usando archivos .JSON. A crear proyectos escalables y código reutilizable, además de crear interfaces gráficas usando la librería Flet.

## Cómo se usa el programa

## 1: Crear un Evento

### Acción del usuario
1. Abrir **Events → Create Event**.
2. Introducir el nombre del evento.
3. Seleccionar el especialista responsable.
4. Definir fecha y hora de inicio y fin.
5. Añadir personal y recursos necesarios.
6. Pulsar **Create Event** y luego **Save**.

**Notas:**
1. El paso 4 puede ser sustituido haciendo lo siguiente, se introduce el tiempo de duración del evento junto con el personal y recursos que este requiere y se pulsa en el botón find slot y automáticamente el programa buscara el próximo hueco disponible más cercano común a todos los trabajadores y recursos necesarios para el evento(esta forma de crear el evento evita la solapación de fechas y que el usuario tenga que buscar manuamente dicho hueco). El función funciona de la siguiente manera, recibe un diccionario con los que indica los especialistas y la cantidad requerida, otro con los recursos y la cantidad requerida, la diración del evento y el intervalo de búsqueda(tiempo que se aumentara cada posible candidato de fecha de inicio si no es viable). El primer candidato de búsqueda es la fecha actual, se eliminan los segundos y milisigundos para trabajar solo con y/m/d, se ordenan los eventos por fecha de inicio para mayor eficiencia, evitando revisar un evento que comienza dentro de un mes y despues revisar uno que ocurrira la semana siguiente, elegimos el primer posible candidato posible de fecha de finalización, el cual es nuestro condidato de inicio incrementado en la duración del evento. Luego vamos a revisar si la pareja de candidatos de inicio y final que elegimos son válidos. Para saber si nuestra pareja de fechas de inicio y final son válidos hacemos lo siguiente, pasamos por los eventos que tenemos guardados y vemos si la fecha de fin de dicho evento es menor o igual que el inicio de nuestra pareja de candidatos o si su fecha de inicio es su fehca de inicio es mayor que la de final de nuestra pareja, en caso afirmativo pasamos al siguiente evento porque el evento actual no da problemas de solapamiento de fechas, en caso contrario vemos si alguno de nuestros trabajadores o recursos esta asignado a dicho evento, si no lo están nuestra pareja candidata es válida si no, pasamos a la siguiente pareja de fechas. 
### Código responsable
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
2. Por defecto se muestra un campo para mostrar agregar un especialista y un recurso para el evento para el evento, en caso de desear solicitar más trabajadores o recursos para el mismo se debe dar en el botón de "+" que aparece al lado de la cantidad solicitada de dicho especialista para el evento.
3. **Posibles Errores(en la creación de los eventos):**
- *1.La fecha de inicio tiene que ser menor que la de final*
- *2.Entre los especialistas solicitados para el evento no puede faltar el especialista encargado(no se puede realizar una operación sin un cirujano)*
- *3.El evento tiene que tener los recursos y especialistas capaces de usar estos recursos, por ejemplo:
una ginecólogo no puede hacer un ultrasonido sin la máquina de ultrasonido.*
- *4. Entre los especialistas asignados al evento tiene que haber uno que sea igual al especialista encargado asignado.*
- *5.En caso de cumplir con lo mencionado anteriormente puede que dentro de los trabajadores guardados no se encuentren los necesarios para el evento, caso análogo para los recursos guardados, en dicho caso no se creara el evento.*

**Observaciones:**
1. *Se pueden crear todos los eventos que desee el usuario(siempre que cumplan las restricciones), una vez quede satisfecho hace click en el botón de saved que aparecera a partir de crear el primer evento y se guardaran permanentemente todos los eventos válidos creados. Esto funciona guardando todos los eventos que va creando el usuario en una lista temporal hasta que se haga click en guardar, el objetivo de esta implementación es optimizar la eficiencia al guardar la información porque los JSON tienen un fucnionamiento ineficiente cuando se quiere guardar, eliminar o actualizar la informacion de estos ya que hay que sacar todos los elementos que tienen guardados realizar la operacion deseada y volverlos a guardar todos, con las listas temporales hacemos que este proceso se pueda realizar una sola vez para todos los eventos, trabajadores o recursos que se quieran guardar mejorando considerablemente la eficiencia.*

## Crear Workers|Resources:
1. Abir **Workers|Resources → Add Worker|By Resource**
2. Completar los campos que aparecen.
3. Click en el botón de guardar que aparecera una vez creado el primer worker | resource

**Observaciones:**
1. *El recurso utilizado por el especialista que se cree tiene que ser uno que sepa usar, ejemplo: no se puede crear un ambulanciero y aseginarle como recurso un electro. Esto es análogo para los recursos, ejemplo: no se puede crear una ambulancia y asginarle que la manejara un cirujano.*


## Visualización de Eventos, Worker, Resource:

### Acción del usuario
1. Abrir **Events|Worker|Resources → View Events|Worker|Resource**.

### Visualización de los detalles de Eventos:
1. Abrir **Events → View Events**.
2. Hacer click en los tres puntos en vertical que aparecen en la esquina inferior derecha de las postales que se muestran una vez realizdo el paso anterior 
3. Click en **View details**

### Visualización del plan de uso de Trabajadores|Recursos:
1. Abrir **Worker|Resources → View Worker|Resource**.
2. Hacer click en los tres puntos en vertical que aparecen en la esquina inferior derecha de las postales que se muestran una vez realizdo el paso anterior 
3. Click en **View use plan**

### Eliminación de Eventos|Trabajadores|Recursos
1. Abrir **Events|Worker|Resources → View Events|Worker|Resource**.
2. Hacer click en los tres puntos en vertical que aparecen en la esquina inferior derecha de las postales que se muestran una vez realizdo el paso anterior 
3. Click en **Delete Event|Worker|Resource**


## Eliminar eventos con fecha de finalización menor que la fecha actual de forma automáticamente:
El programa ejecuta constantemente la función siguiente:
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
De los principales desafíos encontrados durante el desarrollo del proyecto estuvo relacionado con la persistencia de la información de los eventos, trabajadores y recursos. Inicialmente, el modelo de datos fue diseñado de forma completamente relacional:
    - Cada Evento contenía una lista de los trabajadores asignados y una lista de los recursos utilizados.
    - Cada Worker contenía una lista de eventos denominada use_plan, donde se almacenaban todos los eventos en los que participaba.
    - Cada Resource también contenía una lista de eventos llamada use_plan, donde se almacenaban los eventos que utilizaban dicho recurso.
Este diseño funcionaba correctamente mientras la información permanecía en memoria, pero generaba un problema importante al intentar serializar los objetos a formato JSON.

Por ejemplo, un evento podía contener un trabajador:
    Evento E1
    └── Worker W1
A su vez, ese trabajador contenía una referencia al mismo evento:
    Worker W1
    └── Evento E1
Cuando el sistema intentaba guardar el evento, el serializador recorría todos sus atributos y encontraba el trabajador. Posteriormente intentaba guardar el trabajador y encontraba nuevamente el evento. El proceso se repetía indefinidamente:
    Evento → Worker → Evento → Worker → Evento → ...
Este fenómeno se conoce como referencia circular o bucle recursivo infinito, y provoca errores de serialización o un crecimiento infinito de la estructura que se intenta guardar.
Para resolver este problema se decidió aplicar una estrategia similar a la utilizada en bases de datos relacionales: almacenar únicamente los identificadores de los objetos relacionados.
En lugar de guardar un objeto completo:
```JSON 
    event.workers_assigned = [
        worker_1,
        worker_2
    ]
    ```
se almacena únicamente:
```JSON
    event.workers_assigned = [
        "w1",
        "w2"
    ]
```
De forma análoga, los trabajadores y recursos no almacenan objetos ```Event``` dentro de su atributo ```use_plan```, sino únicamente los identificadores de dichos eventos:
```JSON
    worker.use_plan = [
        "e1",
        "e3",
        "e7"
    ]
```
```JSON
    resource.use_plan = [
    "e2",
    "e4",
    "e8"
]
```
Gracias a esta decisión, los archivos JSON contienen únicamente tipos de datos simples como cadenas de texto, listas y diccionarios, evitando completamente los problemas de serialización.

## Proceso de reconstrucción de relaciones:
El hecho de almacenar únicamente identificadores implica que, al cargar la información desde los archivos JSON, las relaciones entre eventos, trabajadores y recursos deben reconstruirse nuevamente en memoria.

Para ello se implementó el método:
```python
    def rebuild_relations(self):
        events_map = {e.id: e for e in self.events}
        workers_map = {w.id: w for w in self.workers}
        resources_map = {r.id: r for r in self.resources}

        for e in self.events:
            e.workers = [workers_map[w_id] for w_id in e.workers if isinstance(w_id,str) and w_id in workers_map]
            e.resources = [resources_map[r_id] for r_id in e.resources if isinstance(r_id,str) and r_id in resources_map]
        for w in self.workers:
            w.use_plan = [events_map[e_id] for e_id in w.use_plan if isinstance(e_id,str) and e_id in events_map]
        for r in self.resources:
            r.use_plan = [events_map[e_id] for e_id in r.use_plan if isinstance(e_id,str) and e_id in events_map]
```
## Ventajas de esta solución

La estrategia de almacenar identificadores y reconstruir las relaciones durante la carga proporciona varias ventajas:
1. Evita referencias circulares.
2. Permite serializar fácilmente la información en formato JSON.
3. Reduce significativamente el tamaño de los archivos almacenados.
4. Facilita la eliminación y modificación de eventos.
5. Mantiene la consistencia de las relaciones entre entidades.
6. Simplifica la persistencia de datos.
7. Permite reconstruir completamente el estado del sistema al iniciar la aplicación.

Gracias a esta solución fue posible mantener una estructura orientada a objetos en memoria mientras se utiliza un formato de almacenamiento simple y eficiente para la persistencia de la información.