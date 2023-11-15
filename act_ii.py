# crear tabla archivos_i
def act_ii(conn,cursor):
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

    sentencia_sql = "CREATE TABLE archivos_i(id INTEGER, ruta_archivo TEXT, n_niveles INTEGER, " + texto_f + ");"
    cursor.execute(sentencia_sql)
    conn.commit()
