from flask import Flask, render_template, request
import mysql.connector

DATABASE_CONFIG = {
    'host': 'lejandro.mysql.pythonanywhere-services.com',
    'user': 'lejandro',
    'password': 'ez"4u4dwHd~HZ#7',
    'database': 'lejandro$Sistema_Eleccion'
}

app = Flask(__name__)
app.secret_key = 'cochabamba'

@app.route("/")
def login_elector():
    titulo="LOGIN ELECTOR"
    return render_template("login.html",titulo=titulo)

@app.route("/registro_persona", methods=["GET", "POST"])
def registro_persona():
    if request.method == "POST":
        ci = request.form.get("ci")
        id_distrito = request.form.get("id_distrito")
        id_departamento = request.form.get("id_departamento")
        nombres = request.form.get("nombres")
        apellidos = request.form.get("apellidos")
        fecha_nacimiento = request.form.get("fecha_nacimiento")
        direccion = request.form.get("direccion")
        genero = request.form.get("genero")

        # Puedes obtener los campos opcionales si son proporcionados en el formulario
        carnet = request.files.get("carnet")
        foto = request.files.get("foto")

        try:
            # Crear una conexión a la base de datos
            conn = mysql.connector.connect(**DATABASE_CONFIG)
            cursor = conn.cursor()

            # Ejecutar la consulta de inserción
            query = "INSERT INTO Usuario (ci, id_distrito, id_departamento, nombres, apellidos, fecha_nacimiento, direccion, genero, habilitado, carnet, foto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, TRUE, %s, %s)"
            values = (ci, id_distrito, id_departamento, nombres, apellidos, fecha_nacimiento, direccion, genero, carnet.read() if carnet else None, foto.read() if foto else None)
            cursor.execute(query, values)

            # Confirmar la transacción
            conn.commit()

            return "Persona registrada exitosamente."

        except Exception as e:
            # En caso de error, realizar un rollback
            conn.rollback()
            return f"Error al registrar la persona: {str(e)}"

        finally:
            # Cerrar la conexión y el cursor
            cursor.close()
            conn.close()

    return render_template("registro_persona.html")



@app.route("/registro_distrito", methods=["GET", "POST"])
def registro_distrito():
    if request.method == "POST":
        nombre_distrito = request.form.get("nombre")
        id_departamento = request.form.get("departamento")

        try:
            # Crear una conexión a la base de datos
            conn = mysql.connector.connect(**DATABASE_CONFIG)
            cursor = conn.cursor()

            # Ejecutar la consulta de inserción con ID automático
            query = "INSERT INTO Distrito (nombre, id_departamento) VALUES (%s, %s)"
            values = (nombre_distrito, id_departamento)
            cursor.execute(query, values)

            # Confirmar la transacción
            conn.commit()

            return "Distrito registrado exitosamente."

        except Exception as e:
            # En caso de error, realizar un rollback
            conn.rollback()
            return f"Error al registrar el distrito: {str(e)}"

        finally:
            # Cerrar la conexión y el cursor
            cursor.close()
            conn.close()

    # Obtener la lista de departamentos para el formulario
    departamentos = obtener_lista_departamentos()

    return render_template("registro_distrito.html", departamentos=departamentos)


def obtener_lista_departamentos():
    try:
        # Crear una conexión a la base de datos
        conn = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()

        # Consultar la lista de departamentos
        query = "SELECT id_departamento, nombre FROM Departamento"
        cursor.execute(query)

        # Obtener los resultados
        departamentos = cursor.fetchall()

        return departamentos

    except Exception as e:
        print(f"Error al obtener la lista de departamentos: {str(e)}")

    finally:
        # Cerrar la conexión y el cursor
        cursor.close()
        conn.close()


@app.route("/registro_departamento", methods=["GET", "POST"])
def registro_departamento():
    if request.method == "POST":
        nombre_departamento = request.form.get("nombre")
        try:
            # Crear una conexión a la base de datos
            conn = mysql.connector.connect(**DATABASE_CONFIG)
            cursor = conn.cursor()
            # Ejecutar la consulta de inserción con ID automático
            query = "INSERT INTO Departamento (nombre) VALUES (%s)"
            values = (nombre_departamento,)
            cursor.execute(query, values)
            # Confirmar la transacción
            conn.commit()
            return "Departamento registrado exitosamente."

        except Exception as e:
            # En caso de error, realizar un rollback
            conn.rollback()
            return f"Error al registrar el departamento: {str(e)}"

        finally:
            # Cerrar la conexión y el cursor
            cursor.close()
            conn.close()

    return render_template("registro_departamento.html")



@app.route("/administrador")
def login_administrador():
    titulo="LOGIN ADMINISTRACION"
    return render_template("login_administrador.html",titulo=titulo)

@app.route("/tribunal")
def login_tribunal():
    titulo="LOGIN TRIBUNAL"
    return render_template("login_tribunal.html",titulo=titulo)

if __name__ == "__main__":
    app.run(debug=True)
'''blueprint investigar'''