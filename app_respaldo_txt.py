from flask import Flask, render_template, request

app = Flask(__name__)

# -------- FUNCIONES QUE YA TENÍAS --------

def cargar_datos(nombre_archivo):
    lista = []

    try:
        archivo = open(nombre_archivo, "r", encoding="utf-8")

        for linea in archivo:
            linea = linea.strip()

            if linea != "":
                datos = linea.split("|")
                lista.append(datos)

        archivo.close()

    except FileNotFoundError:
        archivo = open(nombre_archivo, "w", encoding="utf-8")
        archivo.close()

    return lista


def guardar_dato(nombre_archivo, datos):
    archivo = open(nombre_archivo, "a", encoding="utf-8")

    linea = ""
    for i in range(len(datos)):
        linea += datos[i]
        if i < len(datos) - 1:
            linea += "|"

    archivo.write(linea + "\n")
    archivo.close()


def registrar_objeto_perdido(nombre, categoria, lugar, fecha, descripcion):
    reporte = [nombre, categoria, lugar, fecha, descripcion]
    guardar_dato("perdidos.txt", reporte)


def registrar_objeto_encontrado(nombre, categoria, lugar, fecha, descripcion):
    reporte = [nombre, categoria, lugar, fecha, descripcion]
    guardar_dato("encontrados.txt", reporte)


def ver_objetos_perdidos():
    return cargar_datos("perdidos.txt")


def ver_objetos_encontrados():
    return cargar_datos("encontrados.txt")

# -------- RUTAS DE LA WEB --------

@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/perdidos")
def perdidos():
    lista = ver_objetos_perdidos()
    return render_template("perdidos.html", perdidos=lista)


@app.route("/encontrados")
def encontrados():
    lista = ver_objetos_encontrados()
    return render_template("encontrados.html", encontrados=lista)


@app.route("/registrar_perdido", methods=["GET", "POST"])
def registrar_perdido():
    
    if request.method == "POST":

        nombre = request.form["nombre"]
        categoria = request.form["categoria"]
        lugar = request.form["lugar"]
        fecha = request.form["fecha"]
        descripcion = request.form["descripcion"]

        registrar_objeto_perdido(
            nombre,
            categoria,
            lugar,
            fecha,
            descripcion
        )

    return render_template("registrar_perdido.html")


@app.route("/registrar_encontrado", methods=["GET", "POST"])
def registrar_encontrado():

    if request.method == "POST":

        nombre = request.form["nombre"]
        categoria = request.form["categoria"]
        lugar = request.form["lugar"]
        fecha = request.form["fecha"]
        descripcion = request.form["descripcion"]

        registrar_objeto_encontrado(
            nombre,
            categoria,
            lugar,
            fecha,
            descripcion
        )

    return render_template("registrar_encontrado.html")


if __name__ == "__main__":
    app.run(debug=True)