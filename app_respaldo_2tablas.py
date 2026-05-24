from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def conectar():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="objetos"
    )
    return conexion


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/perdidos")
def perdidos():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT Nombre, Categoria, Lugar, Fecha, Descripcion
        FROM perdidos
    """)

    lista_perdidos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template("perdidos.html", perdidos=lista_perdidos)


@app.route("/encontrados")
def encontrados():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT Nombre, Categoria, Lugar, Fecha, Descripcion
        FROM encontrados
    """)

    lista_encontrados = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template("encontrados.html", encontrados=lista_encontrados)


@app.route("/registrar_perdido", methods=["GET", "POST"])
def registrar_perdido():
    if request.method == "POST":
        nombre = request.form["nombre"]
        categoria = request.form["categoria"]
        lugar = request.form["lugar"]
        fecha = request.form["fecha"]
        descripcion = request.form["descripcion"]

        conexion = conectar()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO perdidos 
            (Nombre, Categoria, Lugar, Fecha, Descripcion)
            VALUES (%s, %s, %s, %s, %s)
        """

        valores = (nombre, categoria, lugar, fecha, descripcion)

        cursor.execute(sql, valores)
        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect("/perdidos")

    return render_template("registrar_perdido.html")


@app.route("/registrar_encontrado", methods=["GET", "POST"])
def registrar_encontrado():
    if request.method == "POST":
        nombre = request.form["nombre"]
        categoria = request.form["categoria"]
        lugar = request.form["lugar"]
        fecha = request.form["fecha"]
        descripcion = request.form["descripcion"]

        conexion = conectar()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO encontrados 
            (Nombre, Categoria, Lugar, Fecha, Descripcion)
            VALUES (%s, %s, %s, %s, %s)
        """

        valores = (nombre, categoria, lugar, fecha, descripcion)

        cursor.execute(sql, valores)
        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect("/encontrados")

    return render_template("registrar_encontrado.html")


if __name__ == "__main__":
    app.run(debug=True)