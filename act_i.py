import os


# obtener los nombres de los arhivos
def act_i(folder_path, conn, cursor):
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