import sqlite3

# Conectar a la base de datos (se crea si no existe)
conexion = sqlite3.connect("vision_artificial.db")
cursor = conexion.cursor()

# Crear la tabla de datos meteorológicos si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS datos_meteorologicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    temperatura REAL,
    presion REAL,
    humedad REAL,
    velocidad_viento REAL,
    precipitacion REAL,
    radiacion_solar REAL
)
''')

# Crear la tabla de registros si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS registros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    latitud REAL NOT NULL,
    longitud REAL NOT NULL,
    tipo_dato TEXT NOT NULL,  -- Tipo de dato (ej: "Durazno verde", "Fruto monilia", etc.)
    valor INTEGER NOT NULL    -- Valor del dato (ej: 2, 4, etc.)
)
''')

# Guardar los cambios y cerrar la conexión
conexion.commit()
conexion.close()

print("Base de datos y tablas creadas exitosamente.")