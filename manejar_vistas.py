import sqlite3

# conexion a la bd
conn = sqlite3.connect("static/arbol_oficios.db")
cursor = conn.cursor()

# contar columnas
cursor.execute("SELECT COUNT(*) as column_count FROM pragma_table_info('explorador');")
columnas = cursor.fetchall()
for col in columnas:
    n_col = col[0] -1


# borrar vista
def borrar_vista():
    texto_borrar = "DROP VIEW codigos_w;"

    try:
        cursor.execute(texto_borrar)
        #print("vista borrada")
    except: 
        print("vista no encontrada")

# crear vista
def crear_vista():
    # EJEMPLO:
    #SELECT nivel_1.codigo AS codigo_1, nivel_2.codigo AS codigo_2, nivel_3.codigo AS codigo_3,
    #IFNULL(nivel_3.codigo, IFNULL(nivel_2.codigo, nivel_1.codigo)) as concatenado
    #FROM nivel_1 LEFT JOIN nivel_2 ON nivel_1.codigo = nivel_2.origen LEFT JOIN nivel_3 ON nivel_2.codigo = nivel_3.origen 
    #ORDER BY nivel_1.id ASC, nivel_2.id ASC, nivel_3.id ASC

    texto_sel = ""
    texto_if = ""
    texto_if_parentesis = ""
    texto_joi = ""
    texo_ord = ""


    # texto_sel
    for sel in range(1, n_col+1): 
        texto_sel = texto_sel + "nivel_" + str(sel) + ".codigo AS codigo_" + str(sel) + ", "

        # texo_ord
        texo_ord = texo_ord + "nivel_" + str(sel) + ".id ASC, "

    texto_seleccion = "CREATE VIEW codigos_w AS SELECT " + texto_sel[0:len(texto_sel)-2]
    texto_orden = "ORDER BY " + texo_ord[0:len(texo_ord)-2]
    

    # texto_joi
    for joi in range(1, n_col): 
        texto_joi = texto_joi + "LEFT JOIN nivel_" + str(joi +1) + " ON nivel_" + str(joi) + ".codigo = nivel_" + str(joi +1) + ".origen "
    texto_join = "FROM nivel_1 " + texto_joi


    # texto_if
    lista = []
    for i in range(2, n_col+1):
        lista.append(i)
    
    for ii in reversed(lista):
        texto_if = texto_if + "IFNULL(nivel_" + str(ii) + ".codigo,"
        texto_if_0 = texto_if[0:len(texto_if)-1]

    for iii in range(0, len(lista)):
        texto_if_parentesis = texto_if_parentesis + ")"

    texto_consulta = texto_seleccion + ", " + texto_if_0 + ", nivel_1.codigo" + texto_if_parentesis + " as concatenado " + texto_join + " " + texto_orden
    #print(texto_consulta)

    cursor.execute(texto_consulta)
    #print("vista creada")

