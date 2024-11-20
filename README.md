# Proyecto de Gestión de Encuestas

Este proyecto implementa una aplicación en Python para gestionar encuestas relacionadas con el consumo de alcohol y problemas de salud. La aplicación permite realizar las siguientes operaciones:

- **Crear encuestas**: Insertar datos sobre el consumo de alcohol y problemas de salud.
- **Consultar y visualizar encuestas**: Visualizar los registros de las encuestas almacenadas en una base de datos MySQL.
- **Actualizar y eliminar registros**: Modificar o eliminar encuestas ya registradas.
- **Aplicar filtros y generar gráficos**: Filtrar los registros según condiciones específicas (como consumo de alcohol alto) y generar gráficos visualizando estos datos.
- **Exportar a Excel**: Exportar los datos de las encuestas a un archivo Excel para su análisis.

## Requisitos

- **Python 3.x**: El proyecto está desarrollado en Python.
- **MySQL**: Se utiliza una base de datos MySQL para almacenar las encuestas.
- **Bibliotecas de Python**:
  - `tkinter`: Para la interfaz gráfica de usuario (GUI).
  - `pandas`: Para exportar datos a archivos Excel.
  - `matplotlib`: Para generar gráficos dinámicos.
  - `pymysql`: Para interactuar con la base de datos MySQL.

## Instalación

Sigue los siguientes pasos para instalar y ejecutar la aplicación:

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/tu_usuario/gestion_encuestas.git
cd gestion_encuestas
