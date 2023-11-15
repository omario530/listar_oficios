from tkinter import *
import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
from tkinter import filedialog

from manejar_tablas import borrar_tablas, crear_tablas
from manejar_archivos import tabla_explorador, insertar_datos_explorador, tabla_explorador_asc, insertar_datos_explorador_asc
from manejar_insertar import insertar_datos_1, insertar_datos, insertar_datos_n, codigo_html_nivel_1, codigo_html_niveles, codigo_html_nivel_n
from manejar_vistas import crear_vista, borrar_vista
from crear_tabla import tabla

import sqlite3
import os

# exportar datos a la BD
conn = sqlite3.connect("static/arbol_oficios.db")
cursor = conn.cursor()

# Acccion del boton etiqueta
def habilitar_etiqueta():

    acceso = clave.get()
    if acceso == "Mia1":
        bot_carpeta.config(state=tk.NORMAL)  # Enable the label
        bot_carpeta.config(fg="black")
    else:
        messagebox.showerror("Clave incorrecta")

def seleccionar_carpeta():
    # ruta seleccionada
    folder_path = filedialog.askdirectory()
    respuesta = messagebox.askyesno(title="Carpeta Seleccionada", message=folder_path + "¿Desea continuar?", type = 'yesno')

    if respuesta:

        if folder_path != None:
            # obtener los nombres de los arhivos
            act_i(folder_path)

            # crear tabla archivos_i
            act_ii()

            print("datos exportados a BD")        
        else:
            print("Ruta no verificable")

# obtener los nombres de los arhivos
def act_i(folder_path):
    conteo = 0

    # borrar los datos de la BD
    cursor.execute("DELETE FROM carpetas;")
    cursor.execute("DELETE FROM archivos;")
    conn.commit()

    # Obtener el largo del texto ingresado
    largo_ruta = len(folder_path) + 1

    # Verificar el tipo de elemento, si es que se ingresa una ruta valida
    if os.path.exists(folder_path):
        elements = os.listdir(folder_path)
        for element in elements:
            element_path = os.path.join(folder_path, element)  # Ruta completa del elemento

            # extraer el nombre de las carpetas
            if os.path.isdir(element_path):
                # Contar las carpetas
                conteo += 1
                # Exportar a la base de datos
                cursor.execute("INSERT INTO carpetas(carpeta) VALUES(" + "'" + element_path + "'" + ");")

            #  extraer el nombre de los archivos
            if os.path.isfile(element_path):
                cursor.execute("INSERT INTO archivos(archivo) VALUES(" + "'" + element_path[largo_ruta:] + "'" + ");")
            conn.commit()
        
        # segundo nivel
        while conteo > 0:
            conteo = 0
            cursor.execute("SELECT carpeta FROM carpetas;")
            resultado = cursor.fetchall()

            # Vaciar la tabla de carpetas
            cursor.execute("DELETE FROM carpetas;")
            conn.commit()

            for res in resultado:
                ruta_carpeta = res[0]
                
                elementos = os.listdir(ruta_carpeta)
                for elemento in elementos:
                    elemento_path = os.path.join(ruta_carpeta, elemento)
                    # print(elemento_path)

                    #  extraer el nombre de los archivos
                    if os.path.isfile(elemento_path):
                        cursor.execute("INSERT INTO archivos(archivo) VALUES(" + "'" + elemento_path[largo_ruta:]  + "'" + ");")

                    # extraer el nombre de las carpetas
                    if os.path.isdir(elemento_path):
                        # Contar las carpetas
                        conteo += 1
                        # Exportar a la base de datos
                        cursor.execute("INSERT INTO carpetas(carpeta) VALUES(" + "'" + elemento_path  + "'" + ");")
            conn.commit()

            if conteo == 0:
                break

# crear tabla archivos_i
def act_ii():
    num_carpetas = []
    try:
        cursor.execute("DROP TABLE archivos_i;")
    except:
        print("tabla no encontrada")

    # leer cada archivo en la BD
    cursor.execute("SELECT archivo FROM archivos;")
    resultado = cursor.fetchall()

    for res in resultado:
        ruta_archivo = res[0]
        largo = len(ruta_archivo)
        cuenta = 0

    # encontrar los separadores de carpeta
        for letra in range(0,largo):
            encontrar = ruta_archivo[letra].find("\\")
            if encontrar > -1:
                cuenta += 1
        num_carpetas.append(cuenta)
    max_num_carpetas = max(num_carpetas) + 1

    # crear la tabla archivos_i
    texto = ""
    for col in range(1, max_num_carpetas + 1):
        agregar = "nivel_" + str(col) + " TEXT, " + "ruta_nivel_" + str(col) + " TEXT, "
        texto = texto + agregar
    texto_f = texto[0:len(texto)-2]

    sentencia_sql = "CREATE TABLE archivos_i(ruta_archivo TEXT, " + texto_f + ");"
    cursor.execute(sentencia_sql)
    conn.commit()

    conn.close()


# datos del formulario de tkinter  ------------------------------------------------------------------------
root = Tk()
# formulario
root.title("Carpeta a analizar")
# tamaño de ventana
width=600
height=300
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.resizable(width=False, height=False)


# etiqueta clave
et_clave=tk.Label(root)
ft = tkFont.Font(family='Arial',size=14)
et_clave["font"] = ft
et_clave["fg"] = "#333333"
et_clave["justify"] = "left"
et_clave["text"] = "Clave de acceso"
et_clave.place(x=30,y=60,width=200,height=31)


 # ingreso clave
clave=tk.Entry(root)
clave["borderwidth"] = "2px"
ft = tkFont.Font(family='Arial',size=14)
clave["font"] = ft
clave["fg"] = "#333333"
clave["justify"] = "left"
clave["text"] = ""
clave["relief"] = "sunken"
clave.place(x=250,y=60,width=150,height=30)
clave["show"] = "*"


# botón de la clave
bot_clave=tk.Button(root, command=habilitar_etiqueta)
bot_clave["bg"] = "#f0f0f0"
ft = tkFont.Font(family='Arial',size=14)
bot_clave["font"] = ft
bot_clave["fg"] = "#000000"
bot_clave["justify"] = "center"
bot_clave["text"] = "Validar"
bot_clave["relief"] = "raised"
bot_clave.place(x=420,y=60,width=70,height=30)
bot_clave["command"] = habilitar_etiqueta


# boton para seleccionar la carpeta
bot_carpeta=tk.Button(root, state=tk.DISABLED, command=seleccionar_carpeta)
bot_carpeta["bg"] = "#f0f0f0"
ft = tkFont.Font(family='Arial',size=14)
bot_carpeta["font"] = ft
bot_carpeta["fg"] = "#000000"
bot_carpeta["justify"] = "center"
bot_carpeta["text"] = "Elegir carpeta"
bot_carpeta.place(x=180,y=170,width=247,height=31)

 
root.mainloop() 

  
