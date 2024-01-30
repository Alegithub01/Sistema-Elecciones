from datetime import datetime

class Departamento:
    def __init__(self, id_departamento, nombre):
        self.id_departamento = id_departamento
        self.nombre = nombre
        self.distritos = []

    def agregar_distrito(self, id_distrito, nombre):
        distrito = Distrito(self.id_departamento, id_distrito, nombre)
        self.distritos.append(distrito)

    def __str__(self):
        return f"Departamento: {self.nombre}, ID: {self.id_departamento}"

class Distrito:
    def __init__(self, id_departamento, id_distrito, nombre):
        self.id_departamento = id_departamento
        self.id_distrito = id_distrito
        self.nombre = nombre
        self.elecciones = []

    def agregar_eleccion(self, id_eleccion, nombre, fecha, hora_inicio, hora_fin):
        eleccion = Eleccion(id_eleccion, self.id_departamento, self.id_distrito, nombre, fecha, hora_inicio, hora_fin)
        self.elecciones.append(eleccion)

    def __str__(self):
        return f"Distrito: {self.nombre}, ID: {self.id_distrito}, Departamento ID: {self.id_departamento}"

class Eleccion:
    def __init__(self, id_eleccion, id_departamento, id_distrito, nombre, fecha, hora_inicio, hora_fin):
        self.id_eleccion = id_eleccion
        self.id_departamento = id_departamento
        self.id_distrito = id_distrito
        self.nombre = nombre
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.candidatos = []
        self.votos = []

    def agregar_candidato(self, id_candidato, id_partido, ci, nombre):
        candidato = Candidato(id_candidato, self.id_eleccion, id_partido, self.id_departamento, self.id_distrito, ci, nombre)
        self.candidatos.append(candidato)

    def registrar_voto(self, id_voto, id_candidato, ci_usuario):
        voto = Voto(id_voto, self.id_eleccion, id_candidato, self.id_distrito, self.id_departamento, ci_usuario, datetime.now())
        self.votos.append(voto)

    def __str__(self):
        return f"Eleccion: {self.nombre}, ID: {self.id_eleccion}, Distrito ID: {self.id_distrito}, Departamento ID: {self.id_departamento}"

class Persona:
    def __init__(self, ci, nombres, apellidos, fecha_nacimiento, direccion, genero):
        self.ci = ci
        self.nombres = nombres
        self.apellidos = apellidos
        self.fecha_nacimiento = fecha_nacimiento
        self.direccion = direccion
        self.genero = genero

    def __str__(self):
        return f"Persona: CI: {self.ci}, Nombres: {self.nombres}, Apellidos: {self.apellidos}"

class Elector(Persona):
    def __init__(self, ci, nombres, apellidos, fecha_nacimiento, direccion, genero, id_departamento, id_distrito):
        super().__init__(ci, nombres, apellidos, fecha_nacimiento, direccion, genero)
        self.id_departamento = id_departamento
        self.id_distrito = id_distrito
        self.habilitado = False  # Por defecto, un elector no está habilitado para votar

    def habilitar_voto(self):
        self.habilitado = True

    def __str__(self):
        return f"Elector: CI: {self.ci}, Nombres: {self.nombres}, Apellidos: {self.apellidos}, Departamento ID: {self.id_departamento}, Distrito ID: {self.id_distrito}, Habilitado: {self.habilitado}"

class Candidato(Persona):
    def __init__(self, ci, nombres, apellidos, fecha_nacimiento, direccion, genero, id_departamento, id_distrito, id_partido):
        super().__init__(ci, nombres, apellidos, fecha_nacimiento, direccion, genero)
        self.id_departamento = id_departamento
        self.id_distrito = id_distrito
        self.id_partido = id_partido

    def __str__(self):
        return f"Candidato: CI: {self.ci}, Nombres: {self.nombres}, Apellidos: {self.apellidos}, Departamento ID: {self.id_departamento}, Distrito ID: {self.id_distrito}, Partido ID: {self.id_partido}"

class Voto:
    def __init__(self, id_voto, id_eleccion, id_candidato, id_distrito, id_departamento, ci_usuario, fecha):
        self.id_voto = id_voto
        self.id_eleccion = id_eleccion
        self.id_candidato = id_candidato
        self.id_distrito = id_distrito
        self.id_departamento = id_departamento
        self.ci_usuario = ci_usuario
        self.fecha = fecha

    def __str__(self):
        return f"Voto: ID: {self.id_voto}, Eleccion ID: {self.id_eleccion}, Candidato ID: {self.id_candidato}, Distrito ID: {self.id_distrito}, Departamento ID: {self.id_departamento}, CI Usuario: {self.ci_usuario}"
                
