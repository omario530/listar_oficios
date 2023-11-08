import sqlite3
import webbrowser
import os

def tabla():
  # conectar con la BD
  conn = sqlite3.connect("static/arbol_oficios.db")
  cursor = conn.cursor()

  consulta = "SELECT concatenado FROM codigos_w;"
  cursor.execute(consulta)
  resultado = cursor.fetchall()

  # Datos para html
  title = "Contenido de carpeta"
  content =""
  for res in resultado:
      dato = res[0]
      content = content + dato

  # Crear el codigo para la pagina
  html_content = f"""
  <!doctype html>
    <head>
      <title>{title}</title>
  </head>
  <body>
      <h1>Contenido de la carpeta seleccionada</h1>
      {content}
  </body>
  </html>
  """

  # Specify the file path where you want to save the HTML file
  file_path = "static/resultado.html"

  # Write the HTML content to the file
  with open(file_path, "w") as file:
      file.write(html_content)
  webbrowser.open(os.path.realpath(file_path))

  conn.close()
  #print(f"HTML creado en {file_path}")
