from flask import Flask, render_template,request, redirect, session, flash, url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
import io
import base64
from matplotlib import pyplot as plt

app = Flask(__name__)
app.secret_key = 'cochabamba'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://lejandro:ez"4u4dwHd~HZ#7@lejandro.mysql.pythonanywhere-services.com/lejandro$Sistema_Eleccion'
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
    habilitado = db.Column(db.Boolean(), nullable=False, server_default='1')

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
    persona = db.relationship('Persona', foreign_keys=[ci_persona])
    id_partido = db.Column(db.Integer, db.ForeignKey('partido.id_partido'), nullable=False)
    partido = db.relationship('Partido')
    imagen_path = db.Column(db.String(255), nullable=False)

class Tribunal(db.Model):
    __tablename__ = 'tribunal'
    id_tribunal = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Voto(db.Model):
    __tablename__ = 'voto'
    id_voto = db.Column(db.Integer, primary_key=True)
    id_candidato = db.Column(db.Integer, db.ForeignKey('candidato.id_candidato'), nullable=False)
    candidato = db.relationship('Candidato')

@app.route("/")
def login_elector():
    titulo = "LOGIN ELECTOR"
    return render_template("login.html", titulo=titulo)


@app.route("/loginTribunal", methods=["GET", "POST"])
def login_tribunal():
    if request.method == "POST":
        username = request.form["usuario"]
        password = request.form["password"]

        usuario = Tribunal.query.filter_by(username = username).first()
        if usuario and password == usuario.password:
            return redirect(url_for('resultados'))
        return redirect(url_for('error_login_tribunal', user=username))

    titulo = "LOGIN TRIBUNAL"
    return render_template("login_tribunal.html", titulo=titulo)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    ci = request.form['usuario']
    fecha_nacimiento = request.form['dob']

    usuario = Persona.query.filter_by(ci=ci).first()
    if usuario and fecha_nacimiento == str(usuario.fecha_nacimiento):
        session['usuario_logueado'] = usuario.ci
        flash(usuario.nombres + ' logueado con éxito!')
        return redirect(url_for('home_elector', ci=ci))
    else:
        flash('Credenciales Incorrectos')
        return redirect(url_for('error_autenticacion', ci=ci, fecha_nacimiento=fecha_nacimiento))


@app.route('/error_autenticacion/<ci>/<fecha_nacimiento>')
def error_autenticacion(ci, fecha_nacimiento):
    return render_template('mensajeError.html', ci=ci, fecha_nacimiento=fecha_nacimiento)



@app.route('/error_login/<user>')
def error_login_tribunal(user):
    return render_template('mensajeTribunal.html', user=user)

@app.route('/resultados')
def resultados():
    try:
        candidatos = Candidato.query.all()
        votos = Voto.query.all()

        # Calcular la suma total de votos
        total_votos = len(votos)

        # Crear la lista de duplas (candidato, porcentaje)
        resultados = [
            (
                candidato.persona.nombres + " " + candidato.persona.ap_paterno + " " + candidato.persona.ap_materno,
                len([voto for voto in votos if voto.id_candidato == candidato.id_candidato]),
                len([voto for voto in votos if voto.id_candidato == candidato.id_candidato]) / total_votos * 100
            )
            for candidato in candidatos
        ]


        # Crear la gráfica de barras con colores diferentes de la paleta tab10 y mayor resolución
        plt.figure(figsize=(8, 8), dpi=300)  # Ajusta el valor de dpi según sea necesario
        colors = plt.cm.tab10.colors  # Utiliza la paleta de colores tab10 de Matplotlib
        bars = plt.bar([result[0] for result in resultados], [result[1] for result in resultados], alpha=0.7, color=colors)

        # Añadir etiquetas de porcentaje en las torres
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.1f}%', ha='center', va='bottom')

        plt.xlabel('Candidatos')
        plt.ylabel('Porcentaje')
        plt.title('Resultados de la Elección')

        # Guardar la gráfica en un objeto de bytes
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)

        # Convertir la gráfica a base64 para mostrarla en la plantilla
        graph_url = base64.b64encode(img.getvalue()).decode()
        img.close()

        return render_template('resultados.html', resultados=resultados, total_votos=total_votos, graph_url=graph_url)

    except Exception as e:
        return f"Error: {str(e)}"



@app.route('/guardar_voto/<ci>', methods=['POST'])
def guardar_voto(ci):
    try:
        id_candidato_seleccionado = request.form.get('candidato')
        elector = Elector.query.filter_by(ci_persona=ci).first()

        nuevo_voto = Voto(id_candidato=id_candidato_seleccionado)
        db.session.add(nuevo_voto)
        elector.habilitado = False
        db.session.commit()

        return render_template('confirmacion.html')

    except Exception as e:
        return jsonify({"error": str(e)})




@app.route('/home_elector/<ci>')
def home_elector(ci):
    usuario = Persona.query.filter_by(ci=ci).first()

    if not usuario:
        flash('Usuario no encontrado')
        return redirect(url_for('login_elector'))

    elector = Elector.query.filter_by(ci_persona=ci).first()

    estado = "Deshabilitado" if elector is None or not elector.habilitado else "Habilitado"

    fecha_nacimiento = usuario.fecha_nacimiento.strftime('%d/%m/%Y') if usuario.fecha_nacimiento else 'Fecha no disponible'

    return render_template("home.html",
                           ci=ci,
                           elector=elector,
                           nombre=usuario.nombres,
                           ap_paterno=usuario.ap_paterno,
                           ap_materno=usuario.ap_materno,
                           fecha_nacimiento=fecha_nacimiento,
                           genero=usuario.genero,
                           direccion=usuario.direccion,
                           estado=estado)


def obtener_candidatos():
    candidatos = Candidato.query.all()
    return candidatos


@app.route('/papeleta_votacion/<ci>')
def papeleta_votacion(ci):
    tus_candidatos = obtener_candidatos()
    return render_template('papeleta.html', ci=ci, candidatos=tus_candidatos)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
