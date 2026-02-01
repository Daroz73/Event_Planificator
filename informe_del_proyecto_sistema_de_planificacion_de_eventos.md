# Sistema de Planificación Inteligente de Eventos 

**Título del proyecto:** Sistema de Planificación Inteligente de Eventos
**Autor:** Dayan Rodríguez Pérez
**Carrera:** Ciencias de la Computación
**Institución:** Universidad de La Habana
**Asignatura:** Programación

## Resumen
El presente proyecto consiste en el desarrollo de un sistema de planificación de eventos capaz de gestionar de forma inteligente la asignación de personal y recursos médicos, evitando conflictos de horarios y violaciones de restricciones. El sistema permite crear eventos, validar su viabilidad, asignar automáticamente trabajadores y recursos disponibles, y buscar el próximo intervalo de tiempo libre en función de una duración dada. Además, incorpora persistencia de datos mediante archivos JSON y una interfaz gráfica interactiva que facilita la gestión de la información. El proyecto destaca por su enfoque modular, su lógica de validación y su algoritmo de búsqueda automática de huecos.

## Introducción
La planificación de eventos en entornos donde intervienen múltiples recursos y personal especializado es un problema complejo, especialmente cuando se deben respetar restricciones de disponibilidad y evitar solapamientos. En contextos como el sector de la salud, una mala planificación puede generar conflictos, retrasos o un uso ineficiente de los recursos.

Este proyecto surge con el objetivo de ofrecer una solución software que permita gestionar de manera organizada y automática la creación de eventos, asignando correctamente trabajadores y recursos según su disponibilidad y especialidad, y garantizando la consistencia de la información almacenada.

## Objetivos
Desarrollar un sistema que permita planificar eventos de forma inteligente, asignando personal y recursos disponibles sin conflictos de horario.

## Descripción General del Sistema
El sistema es una aplicación de escritorio desarrollada en Python que permite al usuario crear y gestionar eventos. Cada evento puede requerir un conjunto específico de trabajadores (según su especialidad) y recursos materiales. El sistema se encarga de verificar la disponibilidad de estos elementos y de asignarlos automáticamente cuando sea posible.

La información se organiza en dominios bien definidos y se mantiene sincronizada entre la lógica del negocio y los archivos de persistencia.

## Análisis del Problema
La planificación manual de eventos presenta varios problemas:

- Dificultad para comprobar la disponibilidad de trabajadores y recursos.
- Alta probabilidad de solapamientos de horarios.
- Falta de una visión global del uso de los recursos.
- Errores al actualizar la información de forma manual.

El sistema propuesto aborda estos problemas mediante validaciones automáticas, control de planes de uso (use\_plan) y un modelo centralizado de planificación.

## Diseño del Sistema
El sistema se diseñó siguiendo un enfoque modular. Entre las principales clases se encuentran:

- **Event:** representa un evento con fecha de inicio, fin, personal y recursos asignados.
- **Worker:** representa a un trabajador con una especialidad y un plan de uso.
- **Resource:** representa un recurso material con su propio plan de uso.
- **Domain:** contiene la lógica central del sistema, incluyendo la búsqueda de huecos disponibles.
- **Events\_Planificator:** se encarga de la asignación de recursos y personal a los eventos.
- **Data\_saved\_loader:** gestiona la carga y guardado de información en archivos JSON.

Cada componente tiene responsabilidades bien definidas, lo que facilita el mantenimiento y la extensibilidad del sistema.

## Implementación
El sistema fue implementado en Python, utilizando programación orientada a objetos. La interfaz gráfica se desarrolló con la librería Flet, permitiendo una interacción dinámica con el usuario.

Se implementaron métodos clave como:

- Asignación automática de recursos y trabajadores a eventos.
- Actualización de los planes de uso (use\_plan).
- Guardado y carga de información en formato JSON.
- Búsqueda del próximo intervalo de tiempo disponible según una duración dada.

## Funcionalidades Principales
- Creación y eliminación de eventos.
- Asignación automática de personal según especialidad.
- Asignación de recursos materiales.
- Validación de conflictos de horario.
- Búsqueda automática de huecos disponibles.
- Persistencia de datos.
- Interfaz gráfica interactiva.

## Elementos Innovadores e Interesantes
Uno de los elementos más relevantes del proyecto es el algoritmo de búsqueda automática de huecos disponibles, que analiza los planes de uso de trabajadores y recursos para sugerir el próximo intervalo válido. Además, el uso de estructuras como use\_plan permite mantener un historial claro y consistente del uso de cada entidad.

Otro aspecto destacable es la integración entre la lógica del dominio y la interfaz gráfica, lo que permite reflejar de inmediato los cambios en el estado del sistema.

Una funcionalidad curiosa del proyecto es la implementación de un menú inteligente para completar campos de la interfaz en los que se requiere vocabulario sin errores como las especialidades.

## Persistencia de Datos
La información del sistema se almacena en archivos JSON, uno por cada tipo de entidad. Cada objeto se serializa respetando una estructura fija que permite reconstruir correctamente los objetos al cargar los datos.

Este enfoque garantiza simplicidad, legibilidad y facilidad de depuración.

Además como solución a la inificiencia de agregar y eliminar elementos de un JSON se pueden crear o seleccionar todos los elementos que el usuario desee agregar/eliminar y realizar la operación sobre los mismos reescribiendo la información del JSON una sola vez.

## Conclusiones
El proyecto demuestra la aplicación práctica de conceptos de programación orientada a objetos, diseño modular y validación de restricciones. El sistema desarrollado constituye una solución funcional y extensible para la planificación inteligente de eventos, y sienta las bases para futuras mejoras y ampliaciones.