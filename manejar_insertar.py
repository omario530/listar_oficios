import sqlite3
#from manejar_tablas import borrar_tablas, crear_tablas
import roman


# conexion a la bd
conn = sqlite3.connect("static/arbol_oficios.db")
cursor = conn.cursor()
cursor_i = conn.cursor()
cursor_a = conn.cursor()

# contar columnas
cursor.execute("SELECT COUNT(*) as column_count FROM pragma_table_info('explorador');")
columnas = cursor.fetchall()
for col in columnas:
    n_col = col[0] -1

def insertar_datos_1():
        c = 1
        a = 1

        texto_1 = "SELECT carpeta_1, COUNT(carpeta_1), ruta FROM explorador_asc" +\
                " GROUP BY carpeta_1 ORDER BY carpeta_1 ASC;"
        cursor.execute(texto_1)
        resultado = cursor.fetchall()

        for res in resultado:
                valores = res[0]
                contenido = res[1]
                ruta = res[2]

                # carpetas
                if valores.find(".") == -1:
                        texto_i = "INSERT INTO carpeta_1 (n, valores, contenido, ruta) VALUES(" + "'" + str(c) + "'" + ", " + "'" + str(valores) + "'" + ", " + "'" + str(contenido) + "'" + ", " + "'" + ruta + "'" + ");"   
                        cursor_i.execute(texto_i)
                        c += 1
                        conn.commit()
                # archivos
                if valores.find(".") != -1:
                        texto_i = "INSERT INTO carpeta_1 (n, valores, contenido, ruta) VALUES(" + "'" + str(a) + "'" + ", " + "'" + str(valores) + "'" + ", " + "'" + str(contenido) + "'" + ", " + "'" + ruta + "'" + ");"     
                        cursor_i.execute(texto_i)
                        a += 1
                   
                        conn.commit()

def insertar_datos():
        c = 0
        a = 0

        for x in range(2, n_col):
                #valor anterior
                valor_anterior = "SELECT carpeta_" + str(x-1) + " FROM explorador_asc WHERE id = 1;"
                cursor_a.execute(valor_anterior)
                resultado_a = cursor_a.fetchall()
                for res_a in resultado_a:
                        anterior = res_a[0]

                # consulta de datos
                if x + 1 >= n_col:
                        texto = "SELECT carpeta_" + str(x-1) + ", carpeta_" + str(x) + ", 0 as carpeta_" + str(x+1) + ", ruta " + \
                        "FROM explorador_asc" +\
                        " GROUP BY carpeta_" + str(x) + " ORDER BY carpeta_" + str(x-1) + " ASC, carpeta_" + str(x) + " ASC;"
                else:
                        texto = "SELECT carpeta_" + str(x-1) + ", carpeta_" + str(x) + ", COUNT(carpeta_" + str(x+1) + "), ruta " + \
                                        "FROM explorador_asc" +\
                                        " GROUP BY carpeta_" + str(x) + " ORDER BY carpeta_" + str(x-1) + " ASC, carpeta_" + str(x) + " ASC;"
        
                cursor.execute(texto)
                resultado = cursor.fetchall()
                
                for res in resultado:
                        origen = res[0]
                        valores = res[1]
                        contenido = res[2]
                        ruta = res[3]

                        if valores != None:
                                # carpetas
                                if valores.find(".") == -1:
                                        if origen != anterior and origen != None:
                                                c = 1
                                                anterior = origen
                                        else:
                                                c += 1
                                        texto_i = "INSERT INTO carpeta_" + str(x) + "(n, origen, valores, contenido, ruta) VALUES(" + "'" + str(c) + "'" + ", " + "'" + str(origen) + "'" + ", " + "'" + str(valores) + "'" + ", " + "'" + str(contenido) + "'" + ", " + "'" + ruta + "'" + ") ;"   
                                        cursor_i.execute(texto_i)
                                        conn.commit()

                                
                                # archivos
                                if valores.find(".") != -1:
                                        if origen != anterior and origen != None:
                                                a = 1
                                                anterior = origen
                                        else:
                                                a += 1
                                        texto_i = "INSERT INTO carpeta_" + str(x) + "(n, origen, valores, contenido, ruta) VALUES(" + "'" + str(a) + "'" + ", " + "'" + str(origen) + "'" + ", " + "'" + str(valores) + "'" + ", " + "'" + str(contenido) + "'" + ", " + "'" + ruta + "'" + ");"   
                                        cursor_i.execute(texto_i)
                                        conn.commit()

def insertar_datos_n():
        c = 0
        a = 0
        # dato anterior
        valor_anterior = "SELECT carpeta_" + str(n_col-1) + " FROM explorador_asc WHERE id = 1;"
        cursor_a.execute(valor_anterior)
        resultado_a = cursor_a.fetchall()

        for res_a in resultado_a:
                anterior = res_a[0]

        texto = "SELECT carpeta_" + str(n_col - 1) + ", carpeta_" + str(n_col) + ", ruta FROM explorador_asc" +\
                " GROUP BY carpeta_" + str(n_col) + " ORDER BY carpeta_" + str(n_col - 1) + " ASC, " + "carpeta_" + str(n_col) + " ASC;"
        cursor.execute(texto)
        resultado = cursor.fetchall()

        for res in resultado:
                origen = res[0]
                valores = res[1]
                ruta = res[2]
                
                # carpetas
                if valores != None and valores.find(".") == -1:
                        if origen != anterior and origen != None:
                                c = 1
                                anterior = origen
                        else:
                                c += 1

                        texto_i = "INSERT INTO carpeta_" + str(n_col) + "(n, origen, valores, ruta) VALUES(" + "'" + str(c) + "'" + ", " + "'" + str(origen) + "'" + ", " + "'" + str(valores) + "'" + ", " + "'" + ruta + "'" + ");"   
                        cursor_i.execute(texto_i)

                # archivos
                if valores != None and valores.find(".") != -1:
                        if origen != anterior and origen != None:
                                a = 1
                                anterior = origen
                        else:
                                a += 1

                        texto_i = "INSERT INTO carpeta_" + str(n_col) + "(n, origen, valores, ruta) VALUES(" + "'" + str(a) + "'" + ", " + "'" + str(origen) + "'" + ", " + "'" + str(valores) + "'" + ", " + "'" + ruta + "'" + ");"   
                        cursor_i.execute(texto_i)
                conn.commit()
        #print("datos insertados a la tablas de carpetas")
                       
def codigo_html_nivel_1(folder_path):
        # nivel 1 -------------------------------------

        consulta_1 = "SELECT n, valores, contenido, ruta FROM carpeta_1 ORDER BY valores ASC;" 
        cursor.execute(consulta_1)
        valores_1 = cursor.fetchall()

        cursor.execute("INSERT INTO nivel_1(codigo) VALUES('<table border = 1>');")
        for valor_1 in valores_1:
                num_1 = valor_1[0]
                val_1 = valor_1[1]
                cont_1 = valor_1[2]
                ruta = "file:///" + folder_path + "/" + valor_1[3]
                
                # carpetas
                if val_1.find(".") == -1:
                # si contiene archivos o carpetas
                        if cont_1 != 0:
                                cursor.execute("INSERT INTO nivel_1(codigo) VALUES('<tr>')")
                                cursor.execute("INSERT INTO nivel_1(codigo) VALUES('<td>" + "[" + str(roman.toRoman(num_1)) + "]  " + str(val_1) + " </td>')")
                                cursor.execute("INSERT INTO nivel_1(codigo) VALUES('<td>')")
                                cursor.execute("INSERT INTO nivel_1(codigo) VALUES('<table border = 1>');")
                                cursor.execute("INSERT INTO nivel_1(codigo) VALUES('<tr>')")
                                cursor.execute("INSERT INTO nivel_1(codigo) VALUES('<td>')")
                                cursor.execute("INSERT INTO nivel_1(codigo) VALUES('carpeta_1_" + str(val_1) +  "')")
                                cursor.execute("INSERT INTO nivel_1(codigo) VALUES('</table>')")
                                cursor.execute("INSERT INTO nivel_1(codigo) VALUES('</tr>')")

                        else:
                                cursor.execute("INSERT INTO nivel_1(codigo) VALUES('<td>" + "[" + str(roman.toRoman(num_1)) + "]  " + str(val_1) + " </td>')")
                                cursor.execute("INSERT INTO nivel_1(codigo) VALUES('</table>')")
                                cursor.execute("INSERT INTO nivel_1(codigo) VALUES('</tr>')")

                # archivos
                if val_1.find(".") != -1:
                        cursor.execute("INSERT INTO nivel_1(codigo) VALUES('<tr>')")
                        cursor.execute("INSERT INTO nivel_1(codigo) VALUES('<td>')")
                        cursor.execute("INSERT INTO nivel_1(codigo) VALUES('<a href = " + ruta + '>' + "[" + str(num_1) + "]  " + str(val_1) + "</a>')")
                        cursor.execute("INSERT INTO nivel_1(codigo) VALUES('</td>')")
                        cursor.execute("INSERT INTO nivel_1(codigo) VALUES('</tr>')")

                #cursor.execute("INSERT INTO nivel_1(codigo) VALUES('</table>')")
                conn.commit()

def codigo_html_niveles(folder_path):
        # niveles siguientes ..............................................
        for w in range(2, n_col):
                consulta_w = "SELECT n, origen, valores, contenido, ruta FROM carpeta_" + str(w) + " WHERE valores NOT NULL ORDER BY origen, valores ASC;"
                cursor.execute(consulta_w)
                valores_w = cursor.fetchall()

                for valor_w in valores_w:
                        num = valor_w[0]
                        origen = valor_w[1]
                        valores = valor_w[2]
                        contenido = valor_w[3]
                        ruta = "file:///" + folder_path + "/" + valor_w[4]
                
                        cursor.execute("INSERT INTO nivel_" + str(w) + " (origen, codigo) VALUES('carpeta_" + str(w-1) + "_" + str(origen) + "','<table border = 1>');")
                        # carpetas
                        if valores.find(".") == -1:
                                # si contiene archivos o carpetas
                                if contenido != 0:
                                        cursor.execute("INSERT INTO nivel_" + str(w) + "(origen, codigo) VALUES('carpeta_" + str(w-1) + "_" + str(origen) + "', '<tr>')")
                                        cursor.execute("INSERT INTO nivel_" + str(w) + "(origen, codigo) VALUES('carpeta_" + str(w-1) + "_" + str(origen) + "', '<td>" + "[" + str(roman.toRoman(num)) + "]  " + str(valores) + " </td>')")
                                        cursor.execute("INSERT INTO nivel_" + str(w) + "(origen, codigo) VALUES('carpeta_" + str(w-1) + "_" + str(origen) + "', '<td>')")
                                        cursor.execute("INSERT INTO nivel_" + str(w) + "(origen, codigo) VALUES('carpeta_" + str(w-1) + "_" + str(origen) + "', 'carpeta_" + str(w) + "_" + str(valores) +"')")
                                        cursor.execute("INSERT INTO nivel_" + str(w) + "(origen, codigo) VALUES('carpeta_" + str(w-1) + "_" + str(origen) + "', '</tr>')")

                                else:
                                        cursor.execute("INSERT INTO nivel_" + str(w) + "(origen, codigo) VALUES('carpeta_" + str(w-1) + "_" + str(origen) + "', '<tr>')")
                                        cursor.execute("INSERT INTO nivel_" + str(w) + "(origen, codigo) VALUES('carpeta_" + str(w-1) + "_" + str(origen) + "', '<td>" + "[" + str(roman.toRoman(num)) + "]  " + str(valores) + " </td>')")
                                        cursor.execute("INSERT INTO nivel_" + str(w) + "(origen, codigo) VALUES('carpeta_" + str(w-1) + "_" + str(origen) + "', '</tr>')")

                        # archivos
                        if valores.find(".") != -1:
                                cursor.execute("INSERT INTO nivel_" + str(w) + "(origen, codigo) VALUES('carpeta_" + str(w-1) + "_" + str(origen) + "', '<tr>')")
                                cursor.execute("INSERT INTO nivel_" + str(w) + "(origen, codigo) VALUES('carpeta_" + str(w-1) + "_" + str(origen) + "', '<td>')")
                                cursor.execute("INSERT INTO nivel_" + str(w) + "(origen, codigo) VALUES('carpeta_" + str(w-1) + "_" + str(origen) + "', '<a href = " + ruta + '>' + "[" + str(num) + "]  " + str(valores) + "</a>')")
                                cursor.execute("INSERT INTO nivel_" + str(w) + "(origen, codigo) VALUES('carpeta_" + str(w-1) + "_" + str(origen) + "', '</td>')")
                                cursor.execute("INSERT INTO nivel_" + str(w) + "(origen, codigo) VALUES('carpeta_" + str(w-1) + "_" + str(origen) + "', '</tr>')")
                        
                        cursor.execute("INSERT INTO nivel_" + str(w) + "(origen, codigo) VALUES('carpeta_" + str(w-1) + "_" + str(origen) + "', '</table>')")
                conn.commit()

def codigo_html_nivel_n(folder_path):
        # nivel n -------------------------------------
        consulta_n = "SELECT n, origen, valores, ruta FROM carpeta_" + str(n_col) + " WHERE valores NOT NULL ORDER BY origen, valores ASC;" 
        cursor.execute(consulta_n)
        valores_n = cursor.fetchall()

        for valor_n in valores_n:
                num_n = valor_n[0]
                origen_n = valor_n[1]
                val_n = valor_n[2]
                ruta = "file:///" + folder_path + "/" + valor_n[3]
                
                cursor.execute("INSERT INTO nivel_" + str(n_col) + " (origen, codigo) VALUES('carpeta_" + str(n_col-1) + "_" + str(origen_n) + "','<table border = 1>');")
                # carpetas
                if val_n.find(".") == -1:
                # si contiene archivos o carpetas

                        cursor.execute("INSERT INTO nivel_" + str(n_col) + "(origen, codigo) VALUES('carpeta_" + str(n_col-1) + "_" + str(origen_n) + "', '<tr>')")
                        cursor.execute("INSERT INTO nivel_" + str(n_col) + "(origen, codigo) VALUES('carpeta_" + str(n_col-1) + "_" + str(origen_n) + "', '<td>" + "[" + str(roman.toRoman(num_n)) + "]  " + str(val_n) + " </td>')")
                        cursor.execute("INSERT INTO nivel_" + str(n_col) + "(origen, codigo) VALUES('carpeta_" + str(n_col-1) + "_" + str(origen_n) + "', '<td>')")
                        cursor.execute("INSERT INTO nivel_" + str(n_col) + "(origen, codigo) VALUES('carpeta_" + str(n_col-1) + "_" + str(origen_n) + "', 'carpeta_" + str(num_n) + "_" + str(val_n) +"')")
                        cursor.execute("INSERT INTO nivel_" + str(n_col) + "(origen, codigo) VALUES('carpeta_" + str(n_col-1) + "_" + str(origen_n) + "', '</tr>')")

                # archivos
                if val_n.find(".") != -1:
                        cursor.execute("INSERT INTO nivel_" + str(n_col) + "(origen, codigo) VALUES('carpeta_" + str(n_col-1) + "_" + str(origen_n) + "', '<tr>')")
                        cursor.execute("INSERT INTO nivel_" + str(n_col) + "(origen, codigo) VALUES('carpeta_" + str(n_col-1) + "_" + str(origen_n) + "', '<td>')")
                        cursor.execute("INSERT INTO nivel_" + str(n_col) + "(origen, codigo) VALUES('carpeta_" + str(n_col-1) + "_" + str(origen_n) + "', '<a href = " + ruta + '>' + "[" + str(num_n) + "]  " + str(val_n) + "</a>')")
                        cursor.execute("INSERT INTO nivel_" + str(n_col) + "(origen, codigo) VALUES('carpeta_" + str(n_col-1) + "_" + str(origen_n) + "', '</td>')")
                        cursor.execute("INSERT INTO nivel_" + str(n_col) + "(origen, codigo) VALUES('carpeta_" + str(n_col-1) + "_" + str(origen_n) + "', '</tr>')")
       
                cursor.execute("INSERT INTO nivel_" + str(n_col) + "(origen, codigo) VALUES('carpeta_" + str(n_col-1) + "_" + str(origen_n) + "', '</table>')")
                conn.commit()
                #print("datos html insertados a tablas de nivel")

#borrar_tablas()
#crear_tablas()
#insertar_datos_1()
#insertar_datos()
#insertar_datos_n()
#codigo_html_nivel_1()
#codigo_html_niveles()
#codigo_html_nivel_n()