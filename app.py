from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Datos de prueba para el inicio de sesión
tribunal_users = {'juez1': 'password1', 'juez2': 'password2'}

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username in tribunal_users:
        if tribunal_users[username] == password:
            flash('Inicio de sesión exitoso. Bienvenido al panel de control del tribunal.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Contraseña incorrecta. Por favor, inténtalo de nuevo.', 'danger')
    else:
        flash('Usuario no encontrado. Por favor, inténtalo de nuevo o regístrate.', 'danger')

    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    return 'Bienvenido al panel de control del tribunal'

if __name__ == '__main__':
    app.run(debug=True)
