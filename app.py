from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'cochabamba'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{clave}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'lejandro',
        clave = 'ez"4u4dwHd~HZ#7',
        servidor = 'lejandro.mysql.pythonanywhere-services.com',
        database = 'lejandro$Sistema_Eleccion'
    )

db = SQLAlchemy(app)

class Persona(db.Model):
    __tablename__ = 'persona'
    ci = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(50), nullable=False)
    ap_paterno = db.Column(db.String(40), nullable=False)
    ap_materno = db.Column(db.String(40), nullable=False)
    fecha_nacimiento = db.Column(db.Date(), nullable=False)
    genero = db.Column(db.String(1), nullable=False)
    direccion = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<Personas ci={self.ci}, nombres={self.nombres}, ap_paterno={self.ap_paterno}, ap_materno={self.ap_materno}, fecha_nacimiento={self.fecha_nacimiento}, genero={self.genero}, direccion={self.direccion}>'


class Elector(db.Model):
    __tablename__ = 'elector'
    id_elector = db.Column(db.Integer, primary_key=True)
    ci_persona = db.Column(db.Integer, db.ForeignKey('persona.ci'), nullable=False)
    habilitado = db.Column(db.Boolean(), default=True)

    def __repr__(self):
        return f'<Elector id_elector={self.id_elector}, ci_persona={self.ci_persona}, habilitado={self.habilitado}>'

class Partido(db.Model):
    __tablename__ = 'partido'
    id_partido = db.Column(db.Integer, primary_key=True)
    nombre_partido = db.Column(db.String(50), nullable=False)
    siglas = db.Column(db.String(8), nullable=False)

class Candidato(db.Model):
    __tablename__ = 'candidato'
    id_candidato = db.Column(db.Integer, primary_key=True)
    ci_persona = db.Column(db.Integer, db.ForeignKey('persona.ci'), nullable=False)
    id_partido = db.Column(db.Integer, db.ForeignKey('partido.id_partido'), nullable=False)




@app.route("/")
def login_elector():
    titulo="LOGIN ELECTOR"
    return render_template("login.html",titulo=titulo)




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)



'''@app.route('/home/<ci>')
def obtener_informacion_elector(ci):
    try:
        conn = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = conn.cursor(dictionary=True)

        consulta = "SELECT * FROM Usuario WHERE ci = %s"
        cursor.execute(consulta, (ci,))
        elector = cursor.fetchone()

        cursor.close()
        conn.close()

        return render_template('home.html', elector=elector)

    except mysql.connector.Error as err:
        return f"Error en la base de datos: {err}"


@app.route("/home_elector", methods=["GET", "POST"])
def home_elector():
    if request.method == "POST":
        ci = request.form.get("user")
        fecha_nacimiento = request.form.get("password")

        try:
            # Crear una conexión a la base de datos
            conn = mysql.connector.connect(**DATABASE_CONFIG)
            cursor = conn.cursor(dictionary=True)

            # Consultar la base de datos para verificar las credenciales
            query = "SELECT * FROM Usuario WHERE ci = %s AND fecha_nacimiento = %s"
            values = (ci, fecha_nacimiento)
            cursor.execute(query, values)

            # Obtener el resultado de la consulta
            persona = cursor.fetchone()

            if persona:
                # Si las credenciales son correctas, redirigir a la página de inicio con el número de CI
                return redirect(url_for('obtener_informacion_elector', ci=ci))
            else:
                # Si las credenciales son incorrectas, mostrar un mensaje de error
                error_message = "Carnet de identidad o fecha de nacimiento incorrectos."
                return render_template("login.html", titulo="Inicio de Sesión", error_message=error_message)

        except Exception as e:
            # En caso de error, mostrar un mensaje de error
            error_message = f"Error: {str(e)}"
            return render_template("login.html", titulo="Inicio de Sesión", error_message=error_message)

        finally:
            # Cerrar la conexión y el cursor
            cursor.close()
            conn.close()

    return render_template("login.html", titulo="Inicio de Sesión")


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
'''
