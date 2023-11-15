import sqlite3
from act_i import act_i
from act_ii import act_ii
from act_iii import act_iii
from act_iv import act_iv

# exportar datos a la BD
conn = sqlite3.connect("static/arbol_oficios.db")
cursor = conn.cursor()


folder_path = r'C:\Users\omar.escamilla\Documents\Listar_oficios_carpetas v4\carpeta_prueba'

act_i(folder_path, conn, cursor)
act_ii(conn, cursor)
act_iii(conn, cursor)
act_iv(conn, cursor)

print("Rutinas ejecutadas")

conn.close()
