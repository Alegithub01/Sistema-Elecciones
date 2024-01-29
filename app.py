from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

DATABASE_CONFIG = {
    'host': 'alejandroCaceres.mysql.pythonanywhere-services.com',
    'user': 'alejandroCaceres',
    'password': '------',
    'database': 'alejandroCaceres$default'
}

@app.route('/home/<ci>')
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

if __name__ == '__main__':
    app.run(debug=True)