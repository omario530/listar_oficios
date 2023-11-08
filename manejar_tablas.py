import sqlite3

# conexion a la bd
conn = sqlite3.connect("static/arbol_oficios.db")
cursor = conn.cursor()

# contar columnas
cursor.execute("SELECT COUNT(*) as column_count FROM pragma_table_info('explorador');")
columnas = cursor.fetchall()
for col in columnas:
    n_col = col[0] -1

def borrar_tablas():
    for y in range(1,n_col+1):
        try:
            texto = "DROP TABLE nivel_" + str(y) + ";"
            texto_c = "DROP TABLE carpeta_" + str(y) + ";"
            cursor.execute(texto)
            cursor.execute(texto_c)
        except:
            print("Tabla nivel_" + str(y) + " no borrada")
            print("Tabla carpeta_" + str(y) + " no borrada")
    conn.commit()
    #print("Tablas de nivel borradas")


def crear_tablas():
    for v in range(1,n_col+1):
        texto = "CREATE TABLE nivel_" + str(v) + " (id INTEGER UNIQUE, origen TEXT, codigo TEXT, PRIMARY KEY(id AUTOINCREMENT));"
        texto_c = "CREATE TABLE carpeta_" + str(v) + " (n INTEGER, origen TEXT, valores TEXT, contenido INTEGER, ruta);"
        
        cursor.execute(texto)
        cursor.execute(texto_c)

    #print("crear_tablas terminado")
    conn.commit()
