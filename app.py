from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'cochabamba'

@app.route("/")
def login_elector():
    titulo="LOGIN ELECTOR"
    lista = ["nose","juan","pedro"]
    return render_template("login.html",titulo=titulo, lista=lista)

@app.route("/administrador")
def login_administrador():
    titulo="LOGIN ADMINISTRACION"
    return render_template("login_administrador.html",titulo=titulo)

@app.route("/tribunal")
def login_tribunal():
    titulo="LOGIN TRIBUNAL"
    return render_template("login_tribunal.html",titulo=titulo)

if __name__ == '__main__':
    app.run(debug=True)



    