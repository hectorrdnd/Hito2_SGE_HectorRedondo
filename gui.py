import os
from tkinter import Menu
from tkinter import messagebox, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from db_connection import conectar
import seaborn as sns
import tkinter as tk
import matplotlib.pyplot as plt
import pandas as pd
import pymysql


def crear_encuesta(treeview, entrada_edad, entrada_sexo, entrada_bebidas_semana, entrada_cervezas_semana,
                   entrada_bebidas_fin_semana, entrada_bebidas_destiladas, entrada_vinos_semana,
                   entrada_perdidas_control, entrada_diversion_dependencia, entrada_problemas_digestivos,
                   entrada_tension_alta, entrada_dolor_cabeza):
    edad = entrada_edad.get()
    sexo = entrada_sexo.get()
    bebidas_semana = entrada_bebidas_semana.get()
    cervezas_semana = entrada_cervezas_semana.get()
    bebidas_fin_semana = entrada_bebidas_fin_semana.get()
    bebidas_destiladas = entrada_bebidas_destiladas.get()
    vinos_semana = entrada_vinos_semana.get()
    perdidas_control = entrada_perdidas_control.get()
    diversion_dependencia = entrada_diversion_dependencia.get()
    problemas_digestivos = entrada_problemas_digestivos.get()
    tension_alta = entrada_tension_alta.get()
    dolor_cabeza = entrada_dolor_cabeza.get()

    if not (edad and sexo and bebidas_semana and cervezas_semana and bebidas_fin_semana and
            bebidas_destiladas and vinos_semana and perdidas_control and diversion_dependencia and
            problemas_digestivos and tension_alta and dolor_cabeza):
        messagebox.showwarning("Advertencia", "Por favor, complete todos los campos necesarios.")
        return

    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO ENCUESTA (edad, sexo, BebidasSemana, CervezasSemana, BebidasFinSemana, 
                                      BebidasDestiladasSemana, VinosSemana, PerdidasControl, 
                                      DiversionDependenciaAlcohol, ProblemasDigestivos, TensionAlta, DolorCabeza)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                int(edad), sexo, int(bebidas_semana), int(cervezas_semana), int(bebidas_fin_semana),
                int(bebidas_destiladas), int(vinos_semana), int(perdidas_control), diversion_dependencia,
                problemas_digestivos, tension_alta, dolor_cabeza
            ))
            conexion.commit()
            messagebox.showinfo("Éxito", "Encuesta registrada exitosamente")
            ver_registros(treeview)

        except pymysql.MySQLError as err:
            messagebox.showerror("Error de base de datos", f"Hubo un error al insertar el registro: {err}")
        finally:
            conexion.close()


def ver_registros(treeview):
    for row in treeview.get_children():
        treeview.delete(row)

    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM ENCUESTA")
            registros = cursor.fetchall()
            for registro in registros:
                treeview.insert("", "end", values=registro)

        except pymysql.MySQLError as err:
            messagebox.showerror("Error de base de datos", f"Hubo un error al recuperar los registros: {err}")
        finally:
            conexion.close()


def actualizar_registro(treeview, entrada_edad, entrada_sexo, entrada_bebidas_semana, entrada_cervezas_semana,
                        entrada_bebidas_fin_semana, entrada_bebidas_destiladas, entrada_vinos_semana,
                        entrada_perdidas_control, entrada_diversion_dependencia, entrada_problemas_digestivos,
                        entrada_tension_alta, entrada_dolor_cabeza):
    seleccionado = treeview.selection()
    if not seleccionado:
        messagebox.showwarning("Advertencia", "Por favor, selecciona un registro para actualizar.")
        return

    registro_id = treeview.item(seleccionado)['values'][0]

    edad = entrada_edad.get()
    sexo = entrada_sexo.get()
    bebidas_semana = entrada_bebidas_semana.get()
    cervezas_semana = entrada_cervezas_semana.get()
    bebidas_fin_semana = entrada_bebidas_fin_semana.get()
    bebidas_destiladas = entrada_bebidas_destiladas.get()
    vinos_semana = entrada_vinos_semana.get()
    perdidas_control = entrada_perdidas_control.get()
    diversion_dependencia = entrada_diversion_dependencia.get()
    problemas_digestivos = entrada_problemas_digestivos.get()
    tension_alta = entrada_tension_alta.get()
    dolor_cabeza = entrada_dolor_cabeza.get()

    if not (edad and sexo and bebidas_semana and cervezas_semana and bebidas_fin_semana and
            bebidas_destiladas and vinos_semana and perdidas_control and diversion_dependencia and
            problemas_digestivos and tension_alta and dolor_cabeza):
        messagebox.showwarning("Advertencia", "Por favor, complete todos los campos necesarios.")
        return

    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE ENCUESTA
                SET edad=%s, sexo=%s, BebidasSemana=%s, CervezasSemana=%s, BebidasFinSemana=%s, 
                    BebidasDestiladasSemana=%s, VinosSemana=%s, PerdidasControl=%s, DiversionDependenciaAlcohol=%s,
                    ProblemasDigestivos=%s, TensionAlta=%s, DolorCabeza=%s
                WHERE idEncuesta=%s
            """, (
                int(edad), sexo, int(bebidas_semana), int(cervezas_semana), int(bebidas_fin_semana),
                int(bebidas_destiladas), int(vinos_semana), int(perdidas_control), diversion_dependencia,
                problemas_digestivos, tension_alta, dolor_cabeza, registro_id
            ))
            conexion.commit()
            messagebox.showinfo("Éxito", "Encuesta actualizada exitosamente")
            ver_registros(treeview)

        except pymysql.MySQLError as err:
            messagebox.showerror("Error de base de datos", f"Hubo un error al actualizar el registro: {err}")
        finally:
            conexion.close()


def eliminar_registro(treeview):
    seleccionado = treeview.selection()
    if not seleccionado:
        messagebox.showwarning("Advertencia", "Por favor, selecciona un registro para eliminar.")
        return

    registro_id = treeview.item(seleccionado)['values'][0]

    respuesta = messagebox.askyesno("Confirmar eliminación", f"¿Estás seguro de eliminar el registro con ID {registro_id}?")
    if respuesta:
        conexion = conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM ENCUESTA WHERE idEncuesta=%s", (registro_id,))
                conexion.commit()
                messagebox.showinfo("Éxito", f"Registro con ID {registro_id} eliminado exitosamente")
                ver_registros(treeview)

            except pymysql.MySQLError as err:
                messagebox.showerror("Error de base de datos", f"Hubo un error al eliminar el registro: {err}")
            finally:
                conexion.close()

def exportar_a_excel():
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM ENCUESTA")
            registros = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]  # Obtener nombres de las columnas

            # Crear un DataFrame y exportar
            df = pd.DataFrame(registros, columns=columnas)

            # Nombre base del archivo
            base_filename = "encuestas_exportadas.xlsx"
            filename = base_filename

            # Verificar si el archivo ya existe
            counter = 1
            while os.path.exists(filename):
                filename = f"encuestas_exportadas_{counter}.xlsx"
                counter += 1

            # Guardar el archivo con el nuevo nombre
            df.to_excel(filename, index=False)
            messagebox.showinfo("Éxito", f"Datos exportados a {filename}")

        except pymysql.MySQLError as err:
            messagebox.showerror("Error de base de datos", f"Hubo un error al exportar los datos: {err}")
        finally:
            conexion.close()
def exportar_filtro_a_excel(filtro_sql, nombre_archivo="encuestas_exportadas_filtradas.xlsx"):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = f"SELECT * FROM ENCUESTA WHERE {filtro_sql}"
            print(f"Ejecutando consulta: {query}")  # Esto te ayudará a ver la consulta ejecutada en la consola para depuración
            cursor.execute(query)
            registros = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]  # Obtener nombres de las columnas

            # Verifica si se obtuvieron los registros
            if len(registros) == 0:
                print("No se encontraron registros con el filtro aplicado")

            # Crear un DataFrame con los datos filtrados
            df = pd.DataFrame(registros, columns=columnas)

            # Crear un nombre de archivo único para evitar sobrescribir archivos existentes
            filename = nombre_archivo
            counter = 1
            while os.path.exists(filename):
                filename = f"encuestas_exportadas_filtradas_{counter}.xlsx"
                counter += 1

            # Exportar los datos filtrados a Excel
            df.to_excel(filename, index=False)
            messagebox.showinfo("Éxito", f"Datos filtrados exportados a {filename}")

        except pymysql.MySQLError as err:
            messagebox.showerror("Error de base de datos", f"Hubo un error al exportar los datos filtrados: {err}")
        finally:
            conexion.close()

# Función para aplicar filtros
def aplicar_filtro(treeview, filtro_sql):
    for row in treeview.get_children():
        treeview.delete(row)

    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = f"SELECT * FROM ENCUESTA WHERE {filtro_sql}"
            cursor.execute(query)
            registros = cursor.fetchall()

            # Insertar los registros en la tabla
            for registro in registros:
                treeview.insert("", "end", values=registro)
        except pymysql.MySQLError as err:
            messagebox.showerror("Error de base de datos", f"Hubo un error al aplicar el filtro: {err}")
        finally:
            conexion.close()


# Funciones predefinidas para filtros específicos
def filtro_consumo_alto(treeview):
    aplicar_filtro(treeview, "BebidasSemana > 10")


def filtro_perdidas_control(treeview):
    aplicar_filtro(treeview, "PerdidasControl > 3")


def filtro_problemas_salud(treeview):
    aplicar_filtro(treeview, "TensionAlta LIKE '%Sí%' OR DolorCabeza LIKE '%Sí%'")

def crear_interfaz():
    root = tk.Tk()
    root.title("Gestión de Encuestas")

    entradas = {}
    campos = [
        "Edad", "Sexo", "Bebidas Semana", "Cervezas Semana", "Bebidas Fin Semana",
        "Bebidas Destiladas Semana", "Vinos Semana", "Pérdidas Control",
        "Diversión Dependencia Alcohol", "Problemas Digestivos", "Tensión Alta", "Dolor de Cabeza"
    ]

    for campo in campos:
        tk.Label(root, text=f"{campo}:").pack()
        entrada = tk.Entry(root)
        entrada.pack()
        entradas[campo] = entrada

    treeview = ttk.Treeview(root, columns=("ID", *campos), show="headings")
    treeview.pack()
    for col in treeview["columns"]:
        treeview.heading(col, text=col)

    # Botones CRUD
    tk.Button(root, text="Crear Encuesta",
              command=lambda: crear_encuesta(treeview, *entradas.values())).pack()
    tk.Button(root, text="Actualizar Encuesta",
              command=lambda: actualizar_registro(treeview, *entradas.values())).pack()
    tk.Button(root, text="Eliminar Encuesta", command=lambda: eliminar_registro(treeview)).pack()
    tk.Button(root, text="Ver Registros", command=lambda: ver_registros(treeview)).pack()

    # Botones para filtros predefinidos
    tk.Button(root, text="Filtro: Consumo Alto", command=lambda: filtro_consumo_alto(treeview)).pack()
    tk.Button(root, text="Filtro: Pérdidas de Control", command=lambda: filtro_perdidas_control(treeview)).pack()
    tk.Button(root, text="Filtro: Problemas de Salud", command=lambda: filtro_problemas_salud(treeview)).pack()

    # Botón para exportar a Excel con filtro
    tk.Button(root, text="Exportar Datos Filtrados a Excel",
              command=lambda: exportar_filtro_a_excel("BebidasSemana > 10")).pack()

    # Botón para generar gráficos
    tk.Button(root, text="Generar Gráfico de Consumo Alto",
              command=lambda: generar_grafico("BebidasSemana > 10", tipo_grafico="histograma")).pack()
    tk.Button(root, text="Generar Gráfico de Bebidas por Sexo",
              command=lambda: generar_grafico("BebidasSemana > 10", tipo_grafico="barra")).pack()

    root.mainloop()

def generar_grafico(filtro_sql, tipo_grafico="histograma"):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = f"SELECT * FROM ENCUESTA WHERE {filtro_sql}"
            cursor.execute(query)
            registros = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]  # Obtener nombres de las columnas

            # Crear un DataFrame con los datos filtrados
            df = pd.DataFrame(registros, columns=columnas)

            if tipo_grafico == "histograma":
                # Crear un histograma de 'BebidasSemana'
                plt.figure(figsize=(10, 6))
                sns.histplot(df['BebidasSemana'], kde=True, color="blue")
                plt.title("Distribución de Bebidas por Semana")
                plt.xlabel("Bebidas Semana")
                plt.ylabel("Frecuencia")
                plt.show()

            elif tipo_grafico == "barra":
                # Crear un gráfico de barras que compare 'BebidasSemana' por 'Sexo'
                plt.figure(figsize=(10, 6))
                sns.barplot(x="Sexo", y="BebidasSemana", data=df, ci=None, palette="muted")
                plt.title("Promedio de Bebidas por Semana por Sexo")
                plt.xlabel("Sexo")
                plt.ylabel("Bebidas por Semana")
                plt.show()

            elif tipo_grafico == "boxplot":
                # Crear un gráfico de boxplot para 'BebidasSemana' por 'Edad'
                plt.figure(figsize=(10, 6))
                sns.boxplot(x="Edad", y="BebidasSemana", data=df, palette="Set2")
                plt.title("Distribución de Bebidas por Semana por Edad")
                plt.xlabel("Edad")
                plt.ylabel("Bebidas por Semana")
                plt.show()

        except pymysql.MySQLError as err:
            messagebox.showerror("Error de base de datos", f"Hubo un error al generar el gráfico: {err}")
        finally:
            conexion.close()


def obtener_datos_filtrados(filtro_sql):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = f"SELECT * FROM ENCUESTA WHERE {filtro_sql}"
            cursor.execute(query)
            registros = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]
            return pd.DataFrame(registros, columns=columnas)
        except pymysql.MySQLError as err:
            messagebox.showerror("Error de base de datos", f"Hubo un error al recuperar los datos filtrados: {err}")
        finally:
            conexion.close()
    return pd.DataFrame()


# Función para mostrar gráficos en una ventana emergente
def mostrar_grafico(df, tipo_grafico="barras"):
    # Crear la ventana de gráficos
    grafico_ventana = tk.Toplevel()
    grafico_ventana.title("Gráfico de Encuestas")

    fig, ax = plt.subplots(figsize=(8, 6))

    # Ejemplo de gráfico de barras: 'BebidasSemana' contra 'PerdidasControl'
    if tipo_grafico == "barras":
        df_grouped = df.groupby('BebidasSemana')[
            'PerdidasControl'].mean()  # Agrupamos por BebidasSemana y calculamos la media de PerdidasControl
        df_grouped.plot(kind='bar', ax=ax, color='skyblue')

        ax.set_title('Promedio de Pérdidas de Control por Bebidas a la Semana', fontsize=14)
        ax.set_xlabel('Bebidas por Semana', fontsize=12)
        ax.set_ylabel('Promedio de Pérdidas de Control', fontsize=12)
        ax.set_xticklabels(df_grouped.index, rotation=45)

    elif tipo_grafico == "pastel":
        # Ejemplo de gráfico de pastel: Distribución de Sexo
        sexo_count = df['Sexo'].value_counts()
        sexo_count.plot(kind='pie', ax=ax, autopct='%1.1f%%', colors=['#ff9999', '#66b3ff', '#99ff99'], startangle=90)

        ax.set_title('Distribución por Sexo', fontsize=14)

    # Incrustar el gráfico en la ventana Tkinter
    canvas = FigureCanvasTkAgg(fig, master=grafico_ventana)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Botón para cerrar la ventana
    tk.Button(grafico_ventana, text="Cerrar", command=grafico_ventana.destroy).pack()


# Función para crear la interfaz principal con menú
def crear_interfaz():
    root = tk.Tk()
    root.title("Gestión de Encuestas")

    # Crear el menú
    menu_bar = Menu(root)
    root.config(menu=menu_bar)

    # Menú de Encuestas
    encuesta_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Encuestas", menu=encuesta_menu)
    encuesta_menu.add_command(label="Crear Encuesta", command=lambda: crear_encuesta(treeview, *entradas.values()))
    encuesta_menu.add_command(label="Actualizar Encuesta",
                              command=lambda: actualizar_registro(treeview, *entradas.values()))
    encuesta_menu.add_command(label="Eliminar Encuesta", command=lambda: eliminar_registro(treeview))
    encuesta_menu.add_command(label="Ver Registros", command=lambda: ver_registros(treeview))

    # Menú de Filtros
    filtro_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Filtros", menu=filtro_menu)
    filtro_menu.add_command(label="Filtro: Consumo Alto", command=lambda: filtro_consumo_alto(treeview))
    filtro_menu.add_command(label="Filtro: Pérdidas de Control", command=lambda: filtro_perdidas_control(treeview))
    filtro_menu.add_command(label="Filtro: Problemas de Salud", command=lambda: filtro_problemas_salud(treeview))

    # Menú de Gráficos
    grafico_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Gráficos", menu=grafico_menu)
    grafico_menu.add_command(label="Gráfico de Consumo de Bebidas",
                             command=lambda: mostrar_grafico(obtener_datos_filtrados("BebidasSemana > 10"), "barras"))
    grafico_menu.add_command(label="Gráfico de Distribución de Sexo",
                             command=lambda: mostrar_grafico(obtener_datos_filtrados("1=1"), "pastel"))

    # Menú de Exportación
    exportar_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Exportar", menu=exportar_menu)
    exportar_menu.add_command(label="Exportar a Excel", command=exportar_a_excel)

    # Crear entradas y el Treeview
    entradas = {}
    campos = [
        "Edad", "Sexo", "Bebidas Semana", "Cervezas Semana", "Bebidas Fin Semana",
        "Bebidas Destiladas Semana", "Vinos Semana", "Pérdidas Control",
        "Diversión Dependencia Alcohol", "Problemas Digestivos", "Tensión Alta", "Dolor de Cabeza"
    ]

    for campo in campos:
        tk.Label(root, text=f"{campo}:").pack()
        entrada = tk.Entry(root)
        entrada.pack()
        entradas[campo] = entrada

    treeview = ttk.Treeview(root, columns=("ID", *campos), show="headings")
    treeview.pack()
    for col in treeview["columns"]:
        treeview.heading(col, text=col)

    root.mainloop()


# Función para conectar a la base de datos
def conectar():
    # Aquí deberías colocar los detalles de conexión a tu base de datos
    return pymysql.connect(host='localhost', user='root', password='curso', database='encuestas')


if __name__ == "__main__":
    crear_interfaz()
#
