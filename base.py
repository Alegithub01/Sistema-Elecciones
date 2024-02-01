import mysql.connector
from mysql.connector import errorcode

print("Conectando...")
try:
    conn = mysql.connector.connect(
           host='DanielTolaba41.mysql.pythonanywhere-services.com',
           user='DanielTolaba41',
           password='Prueba123'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe un error en el nombre de usuario o en la clave')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS DanielTolaba41$default;")

cursor.execute("CREATE DATABASE DanielTolaba41$default;")

cursor.execute("USE DanielTolaba41$default;")

# creando las tablas
TABLES = {}
TABLES['Departamentos'] = ('''
    CREATE TABLE Departamento (
    id_departamento NUMERIC NOT NULL,
    nombre VARCHAR(60) NOT NULL,
    PRIMARY KEY (id_departamento)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Distritos'] = ('''
    CREATE TABLE Distrito (
    id_distrito NUMERIC NOT NULL,
    id_departamento NUMERIC NOT NULL,
    nombre VARCHAR(60) NOT NULL,
    PRIMARY KEY (id_distrito, id_departamento)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Elecciones'] = ('''
    CREATE TABLE Eleccion (
    id_eleccion NUMERIC NOT NULL,
    nombre VARCHAR(40) NOT NULL,
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    PRIMARY KEY (id_eleccion)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Resultado_ELecciones'] = ('''
    CREATE TABLE Resultado_Eleccion (
    id_resultado NUMERIC NOT NULL,
    id_eleccion NUMERIC NOT NULL,
    candidato NUMERIC NOT NULL,
    votos NUMERIC NOT NULL,
    porcentaje DOUBLE PRECISION NOT NULL,
    total_votos NUMERIC NOT NULL,
    PRIMARY KEY (id_resultado, id_eleccion, candidato)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')


TABLES['Partidos'] = ('''
    CREATE TABLE partido (
    id_partido NUMERIC NOT NULL,
    nombre VARCHAR(40) NOT NULL,
    ideologia VARCHAR (255)NOT NULL,
    PRIMARY KEY (id_partido)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')


TABLES['Tribunales'] = ('''
    CREATE TABLE Tribunal (
    id NUMERIC NOT NULL,
    id_eleccion NUMERIC NOT NULL,
    nombre_usuario VARCHAR(100) NOT NULL,
    password VARCHAR(100) NULL,
    PRIMARY KEY (id, id_eleccion)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')


TABLES['Administradores'] = ('''
    CREATE TABLE Administrador (
    id_administrador NUMERIC NOT NULL,
    usuario VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    PRIMARY KEY (id_administrador)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')


TABLES['Usuarios'] = ('''
    CREATE TABLE Usuario (
    ci NUMERIC NOT NULL,
    id_distrito NUMERIC NOT NULL,
    id_departamento NUMERIC NOT NULL,
    nombres VARCHAR(60) NOT NULL,
    apellidos VARCHAR(70) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    genero VARCHAR(1) NOT NULL,
    habilitado BOOLEAN NOT NULL,
    voto BOOLEAN NOT NULL,
    carnet LONGBLOB NOT NULL,
    foto LONGBLOB NOT NULL,
    PRIMARY KEY (ci, id_distrito, id_departamento)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')


TABLES['Candidatos'] = ('''
    CREATE TABLE Candidato (
    id_candidato NUMERIC NOT NULL,
    id_eleccion NUMERIC NOT NULL,
    id_partido NUMERIC NOT NULL,
    id_departamento NUMERIC NOT NULL,
    id_distrito NUMERIC NOT NULL,
    ci NUMERIC NOT NULL,
    PRIMARY KEY (id_candidato)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')


TABLES['Votos'] = ('''
    CREATE TABLE Voto (
    id_voto NUMERIC NOT NULL,
    id_eleccion NUMERIC NOT NULL,
    id_candidato NUMERIC NOT NULL,
    id_distrito NUMERIC NOT NULL,
    id_departamento NUMERIC NOT NULL,
    ci_usuario NUMERIC NOT NULL,
    fecha DATETIME NOT NULL,
    PRIMARY KEY (id_voto, id_eleccion, id_candidato, id_distrito, id_departamento)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')



for tabla_nombre in TABLES:
      tabla_sql = TABLES[tabla_nombre]
      try:
            print('Creando tabla {}:'.format(tabla_nombre), end=' ')
            cursor.execute(tabla_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Ya existe la tabla')
            else:
                  print(err.msg)
      else:
            print('OK')

conn.commit()




#RELACIONES TABLAS
# Relación entre Distrito y Departamento
try:
    cursor.execute('''
        ALTER TABLE Distrito
        ADD CONSTRAINT departamento_distrito_fk
        FOREIGN KEY (id_departamento)
        REFERENCES Departamento (id_departamento)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
    ''')
    print("Relación entre Distrito y Departamento: OK")
except mysql.connector.Error as err:
    print(f"Error al establecer la relación: {err}")

# Relación entre Usuario y Distrito
try:
    cursor.execute('''
        ALTER TABLE Usuario
        ADD CONSTRAINT distrito_usuario_fk
        FOREIGN KEY (id_distrito, id_departamento)
        REFERENCES Distrito (id_distrito, id_departamento)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
    ''')
    print('Relación entre Usuario y Distrito: OK')
except mysql.connector.Error as err:
    print(f'Error al crear la relación: {err}')

# Relación entre Voto y Distrito
try:
    cursor.execute('''
        ALTER TABLE Voto
        ADD CONSTRAINT distrito_voto_fk
        FOREIGN KEY (id_distrito, id_departamento)
        REFERENCES Distrito (id_distrito, id_departamento)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
    ''')
    print('Relación entre Voto y Distrito: OK')
except mysql.connector.Error as err:
    print(f'Error al crear la relación: {err}')

# Relación entre Candidato y Eleccion
try:
    cursor.execute('''
        ALTER TABLE Candidato
        ADD CONSTRAINT eleccion_candidato_fk
        FOREIGN KEY (id_eleccion)
        REFERENCES Eleccion (id_eleccion)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
    ''')
    print('Relación entre Candidato y Eleccion: OK')
except mysql.connector.Error as err:
    print(f'Error al crear la relación: {err}')

# Relación entre Tribunal y Eleccion
try:
    cursor.execute('''
        ALTER TABLE Tribunal
        ADD CONSTRAINT eleccion_tribunal_fk
        FOREIGN KEY (id_eleccion)
        REFERENCES Eleccion (id_eleccion)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
    ''')
    print('Relación entre Tribunal y Eleccion: OK')
except mysql.connector.Error as err:
    print(f'Error al crear la relación: {err}')

# Relación entre Voto y Eleccion
try:
    cursor.execute('''
        ALTER TABLE Voto
        ADD CONSTRAINT eleccion_voto_fk
        FOREIGN KEY (id_eleccion)
        REFERENCES Eleccion (id_eleccion)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
    ''')
    print('Relación entre Voto y Eleccion: OK')
except mysql.connector.Error as err:
    print(f'Error al crear la relación: {err}')

# Relación entre Resultado_Eleccion y Eleccion
try:
    cursor.execute('''
        ALTER TABLE Resultado_Eleccion
        ADD CONSTRAINT eleccion_resultado_eleccion_fk
        FOREIGN KEY (id_eleccion)
        REFERENCES Eleccion (id_eleccion)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
    ''')
    print('Relación entre Resultado_Eleccion y Eleccion: OK')
except mysql.connector.Error as err:
    print(f'Error al crear la relación: {err}')

# Relación entre Candidato y Partido
try:
    cursor.execute('''
        ALTER TABLE Candidato
        ADD CONSTRAINT partido_candidato_fk
        FOREIGN KEY (id_partido)
        REFERENCES partido (id_partido)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
    ''')
    print('Relación entre Candidato y Partido: OK')
except mysql.connector.Error as err:
    print(f'Error al crear la relación: {err}')

# Relación entre Candidato y Usuario
try:
    cursor.execute('''
        ALTER TABLE Candidato
        ADD CONSTRAINT usuario_candidato_fk
        FOREIGN KEY (ci, id_distrito, id_departamento)
        REFERENCES Usuario (ci, id_distrito, id_departamento)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
    ''')
    print('Relación entre Candidato y Usuario: OK')
except mysql.connector.Error as err:
    print(f'Error al crear la relación: {err}')

# Relación entre Voto y Candidato
try:
    cursor.execute('''
        ALTER TABLE Voto
        ADD CONSTRAINT candidato_voto_fk
        FOREIGN KEY (id_candidato)
        REFERENCES Candidato (id_candidato)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
    ''')
    print('Relación entre Voto y Candidato: OK')
except mysql.connector.Error as err:
    print(f'Error al crear la relación: {err}')



# commitando si no hay nada que tenga efecto
conn.commit()

cursor.close()
conn.close()