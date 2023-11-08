import sqlite3

# conexion a la bd
conn = sqlite3.connect("static/arbol_oficios.db")
cursor = conn.cursor()


def tabla_explorador():
    num_carpetas = []

    # conexion a la bd
    conn = sqlite3.connect("static/arbol_oficios.db")
    cursor = conn.cursor()

    # borrar la tabla
    try:
        cursor.execute("DROP TABLE explorador;")
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
    max_num_carpetas = max(num_carpetas)

    # crear la tabla en la bd
    texto = ""
    for col in range(1, max_num_carpetas + 1):
        agregar = "carpeta_" + str(col) + " TEXT, "
        texto = texto + agregar
    texto = texto +  "carpeta_" + str(max_num_carpetas + 1) + " TEXT"
    
    sentencia_sql = "CREATE TABLE explorador(" + texto + ");"
    cursor.execute(sentencia_sql)
    conn.commit()

    sentencia_sql_1 = "ALTER TABLE explorador ADD column ruta TEXT"
    cursor.execute(sentencia_sql_1)
    conn.commit()

def insertar_datos_explorador():
    # Borrar la tabla explorador
    cursor.execute("DELETE from explorador;")
    conn.commit()
    
    # leer cada archivo en la BD
    cursor.execute("SELECT archivo FROM archivos;")
    resultado = cursor.fetchall()

    for res in resultado:
        cuenta = 0
        ruta_archivo = res[0]
        largo = len(ruta_archivo)
        posiciones = []
        palabras = []
    # buscar los separadores de carpeta
        for letra in range(0, largo):
            encontrar = ruta_archivo[letra].find("\\")
            # agregar posiciones
            if encontrar > -1:
                cuenta += 1
                posiciones.append(letra)
        # agregar las palabras encontradas
        if len(posiciones)>0:

            n = 0
            for i in range(0, len(posiciones)):
                palabra = ruta_archivo[n:posiciones[i]]
                palabras.append(palabra)
                n = posiciones[i] + 1
            palabra_final = ruta_archivo[posiciones[len(posiciones)-1]+1:]
            palabras.append(palabra_final)
        else:
            palabras.append(ruta_archivo)

        t_insertar = ""
        t_valores = ""
        for cc in range(0,len(palabras)):
            # parte de insertar
            insetar = "carpeta_" + str(cc+1) + ", "
            t_insertar = t_insertar + insetar
            texto_insertar = "INSERT INTO explorador(" + t_insertar[0:len(t_insertar)-2] + ", ruta) VALUES ("

            # parte de valores
            valores = "'" + palabras[cc] + "'" + ", "
            t_valores = t_valores + valores
            texto_valores = t_valores[0:len(t_valores)-2] + ", " + "'" + ruta_archivo + "'" + ");"
            sql = texto_insertar + texto_valores

        cursor.execute(sql)
        conn.commit()

def tabla_explorador_asc():

    # contar columnas
    cursor.execute("SELECT COUNT(*) as column_count FROM pragma_table_info('explorador');")
    columnas = cursor.fetchall()
    for col in columnas:
        n_col = col[0] - 1

    # borrar tabla
    try:
        borrar = "DROP table explorador_asc;"
        cursor.execute(borrar)
        conn.commit()
    except:
        print("Tabla explorador_asc no encontrada")

    # Crear tabla
    parte_i_0 = ""
    for col in range(1, n_col+1):
        parte_i_0= parte_i_0 + "carpeta_" + str(col) + " TEXT, "
        parte_i = parte_i_0[0:len(parte_i_0)-2]

    try:
        crear = "CREATE TABLE explorador_asc(id INTEGER UNIQUE, " + parte_i + ", ruta TEXT, PRIMARY KEY(id AUTOINCREMENT));"
        cursor.execute(crear)
        conn.commit()
    except:
       print("Fallo al crear tabla explorador_asc")

def insertar_datos_explorador_asc():

    # contar columnas
    cursor.execute("SELECT COUNT(*) as column_count FROM pragma_table_info('explorador');")
    columnas = cursor.fetchall()
    for col in columnas:
        n_col = col[0] - 1

    # insertar valores
    parte_i_0 = ""
    parte_ii_0 = ""

    for col in range(1, n_col+1):
        parte_i_0= parte_i_0 + "carpeta_" + str(col) + ", "
        parte_i = parte_i_0[0:len(parte_i_0)-2]
        parte_ii_0 = parte_ii_0 + " carpeta_" + str(col) + " ASC, "
        parte_ii = parte_ii_0[0:len(parte_ii_0)-2]

    try:
        insertar = "INSERT INTO explorador_asc(" + parte_i + ", ruta) SELECT " + parte_i + " , ruta FROM explorador ORDER BY " + parte_ii + ";"
        cursor.execute(insertar)
        conn.commit()
        #print("datos insertados a explorador_asc")
    except:
        print("Datos no insertados")