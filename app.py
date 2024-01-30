from flask import Flask, render_template
import mysql.connector

DATABASE_CONFIG = {
    'host': 'villarpandoAlejandro.mysql.pythonanywhere-services.com',
    'user': 'villarpandoAleja',
    'password': 'todoloque32',
    'database': 'villarpandoAleja$default',
    'port': 3306
}


class Candidate:
    def __init__(self, id_candidato, id_eleccion, id_partido, id_departamento, id_distrito, ci):
        self.id_candidato = id_candidato
        self.id_eleccion = id_eleccion
        self.id_partido = id_partido
        self.id_departamento = id_departamento
        self.id_distrito = id_distrito
        self.ci = ci




app = Flask(__name__)

@app.route('/home', methods=["GET", "POST"])
def obtener_informacion_candidatos():
    try:
        conn = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = conn.cursor(dictionary=True)

        consulta_candidatos = "SELECT * FROM Candidato"
        cursor.execute(consulta_candidatos)
        candidatos_data = cursor.fetchall()

        candidatos = [
            Candidate(
                c['id_candidato'],
                c['id_eleccion'],
                c['id_partido'],
                c['id_departamento'],
                c['id_distrito'],
                c['ci']
            ) for c in candidatos_data
        ]

        cursor.close()
        conn.close()

        # Print candidates' information to the console
        for candidato in candidatos:
            print(f"ID Candidato: {candidato.id_candidato} | "
                  f"ID Elección: {candidato.id_eleccion} | "
                  f"ID Partido: {candidato.id_partido} | "
                  f"ID Departamento: {candidato.id_departamento} | "
                  f"ID Distrito: {candidato.id_distrito} | "
                  f"CI: {candidato.ci}")

        return render_template('votacion.html', candidatos=candidatos)

    except mysql.connector.Error as err:
        return f"Error en la base de datos: {err}"

if __name__ == '__main__':
    app.run(debug=True)



    