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
        SELECT Id_objeto, Nombre, Categoria, Lugar, Fecha, Descripcion, Carnet
        FROM objetos_registrados
        WHERE Tipo = 'perdido'
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
        SELECT Id_objeto, Nombre, Categoria, Lugar, Fecha, Descripcion, Carnet
        FROM objetos_registrados
        WHERE Tipo = 'encontrado'
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
        carnet = request.form["carnet"]
        descripcion = request.form["descripcion"]

        conexion = conectar()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO objetos_registrados
            (Nombre, Categoria, Lugar, Fecha, Descripcion, Carnet, Tipo)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        valores = (
            nombre,
            categoria,
            lugar,
            fecha,
            descripcion,
            carnet,
            "perdido"
        )

        cursor.execute(sql, valores)
        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect("/perdidos")

    return render_template("registrar_perdido.html")


@app.route("/registrar_encontrado")
def registrar_encontrado():
    return redirect("/")


@app.route("/marcar_encontrado/<int:id_objeto>", methods=["POST"])
def marcar_encontrado(id_objeto):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE objetos_registrados
        SET Tipo = 'encontrado'
        WHERE Id_objeto = %s
    """, (id_objeto,))

    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect("/perdidos")


@app.route("/eliminar_encontrado/<int:id_objeto>", methods=["POST"])
def eliminar_encontrado(id_objeto):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM objetos_registrados
        WHERE Id_objeto = %s AND Tipo = 'encontrado'
    """, (id_objeto,))

    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect("/encontrados")


if __name__ == "__main__":
    app.run(debug=True)