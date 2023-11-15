# llenar la tabla archivos_i

def act_iii(conn,cursor):

    # dato archivo
    consulta_1 = "INSERT INTO archivos_i(ruta_archivo) SELECT archivo FROM archivos ORDER BY archivo ASC;"
    cursor.execute(consulta_1)
    conn.commit()

    # contar e insertar niveles
    consulta_2 = "SELECT ruta_archivo FROM archivos_i ORDER BY ruta_archivo ASC;"
    cursor.execute(consulta_2)
    resultado = cursor.fetchall()

    n = 1
    for res in resultado:
        ruta_archivo = res[0]
        largo = len(ruta_archivo)
        cuenta = 1
        
        # encontrar los separadores de carpeta
        for letra in range(0,largo):

            encontrar = ruta_archivo[letra].find("\\")
            if encontrar > -1:
                cuenta += 1
            consulta_3 = "UPDATE archivos_i SET id = " + "'" + str(n) + "'" + ", n_niveles = " + "'" + str(cuenta) + "'" " WHERE ruta_archivo = " + "'" + ruta_archivo + "';"             
            cursor.execute(consulta_3)
            
        n += 1
        conn.commit()