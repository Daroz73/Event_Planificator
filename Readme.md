# Sistema de Planificación Inteligente de Eventos

Sistema de escritorio desarrollado en **Python** para la planificación automática de eventos con asignación inteligente de **personal** y **recursos**, evitando conflictos de horario y violaciones de restricciones.

El proyecto está orientado a entornos médicos, pero su arquitectura permite adaptarlo fácilmente a otros dominios.

---

## 🚀 Características principales

- Creación y gestión de eventos
- Asignación automática de trabajadores según especialidad
- Asignación de recursos materiales
- Control de disponibilidad mediante planes de uso (`use_plan`)
- Búsqueda automática del próximo intervalo de tiempo disponible
- Persistencia de datos en archivos JSON
- Interfaz gráfica interactiva desarrollada con **Flet**

---

## 🖥️ Tecnologías utilizadas

- **Python 3.10+**
- **Flet** (interfaz gráfica)
- **JSON** (persistencia de datos)

---

## 📦 Requisitos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

- Python 3.10 o superior
- Flet 0.28.3 o superior
- pip (gestor de paquetes de Python)

Instala las dependencias ejecutando:

```bash
pip install -r requirements.txt
```

---

## ▶️ Ejecución del proyecto

El punto de entrada del sistema es:

```
GUI/main_windows.py
```

Para ejecutar la aplicación:

```bash
python GUI/main_windows.py
```

---

## 📁 Estructura del proyecto

```
📦 sistema-planificacion-eventos
 ├── GUI/
 │    └── main_windows.py   # Punto de entrada
 ├── core/                # Lógica del negocio
 ├── data/                  # Archivos JSON (persistencia)
 │    ├── events.json
 │    ├── personal.json
 │    └── resources.json
 ├── requirements.txt
 ├── README.md
 └── Informe_Proyecto.pdf
```

---

## 🧠 Funcionamiento general

1. El usuario crea un evento desde la interfaz gráfica
2. Selecciona personal requerido por especialidad y recursos necesarios
3. El sistema valida disponibilidad y conflictos
4. Se asignan automáticamente trabajadores y recursos disponibles
5. Se actualizan los planes de uso (`use_plan`)
6. La información se guarda en archivos JSON

Opcionalmente, el sistema puede **buscar automáticamente el próximo hueco disponible** en función de una duración indicada.

---

## 💾 Persistencia de datos

Los datos se almacenan en archivos JSON independientes para:

- Eventos
- Trabajadores
- Recursos

Cada entidad mantiene un `use_plan` que registra los eventos en los que participa, garantizando consistencia y control de disponibilidad.

---

## 📄 Documentación

- **Informe del proyecto:** documento académico con el análisis, diseño e implementación del sistema.
- **README.md:** guía técnica para instalación y ejecución.

---

## 👤 Autor

**Dayan Rodríguez Pérez**
Estudiante de Ciencias de la Computación
Universidad de La Habana

---

## 📌 Estado del proyecto

Proyecto funcional y extensible. Diseñado para futuras mejoras como:

- Exportación de eventos
- Soporte multiusuario
- Persistencia en base de datos
- Optimización del algoritmo de planificación

---

¡Gracias por revisar el proyecto! 🚀