# llenar las columnas de nivel en la tabla archivos_i

def act_iv(conn,cursor):
    # contar e insertar niveles
    consulta_1 = "SELECT id, ruta_archivo, n_niveles FROM archivos_i ORDER BY id ASC;"
    cursor.execute(consulta_1)
    resultado = cursor.fetchall()

    for res in resultado:
        ID = res[0]
        archivo = res[1]
        N_NIVELES = res[2]

        # nivel 1
        if N_NIVELES == 1:
            nivel = archivo
            ruta_nivel = "'\'" + archivo
        # los demas niveles
        else:
            posiciones = []

            for n_letra in range(0, len(archivo)):
                if archivo[n_letra] == "\\":
                    posiciones.append(n_letra)
            
            # obtener la ruta hasta la diagonal
            for n_posiciones in range(0, len(posiciones)):
                nivel = archivo[0:n_posiciones]
                print(nivel)