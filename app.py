# Flask App
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import io
import base64
from matplotlib import pyplot as plt

app = Flask(__name__)

# Configuración de la ruta a la carpeta de plantillas
app.template_folder = '/home/DanielTolaba41/mysite/templates'

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://DanielTolaba41:Prueba123@DanielTolaba41.mysql.pythonanywhere-services.com/DanielTolaba41$Base'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/')
def home():
    return '<h1>Para ver lo trabajado añada la ruta /resultados</h1>'

# Modelo de la base de datos
class ResultadoEleccion(db.Model):
    __tablename__ = 'Resultado_Eleccion'

    id_resultado = db.Column(db.Integer, primary_key=True)
    id_eleccion = db.Column(db.Integer)
    candidato = db.Column(db.Integer)
    votos = db.Column(db.Integer)
    porcentaje = db.Column(db.Float)
    total_votos = db.Column(db.Integer)

# Ruta para mostrar resultados
@app.route('/resultados')
def resultados():
    try:
        resultados = ResultadoEleccion.query.all()

        # Calcular la suma total de votos
        total_votos = sum(resultado.votos for resultado in resultados)

        # Obtener la lista de candidatos y porcentajes
        candidatos = [resultado.candidato for resultado in resultados]
        votos = [resultado.votos for resultado in resultados]
        porcentajes = [voto / total_votos * 100 for voto in votos]

        # Crear la gráfica de barras
        plt.figure(figsize=(8, 8))
        bars = plt.bar(candidatos, porcentajes, alpha=0.7)

        # Añadir etiquetas de porcentaje en las torres
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.1f}%', ha='center', va='bottom')

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

if __name__ == '__main__':
    app.run(debug=True)
