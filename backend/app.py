from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from detector import DetectorEnfermedades
import sqlite3
import threading
from datetime import datetime
import time

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")  # Habilitar WebSockets

# Credenciales validas 
VALID_USERNAME = "admin"
VALID_PASSWORD = "12345678"

# Conectar a la base de datos
def conectar_db():
    return sqlite3.connect("vision_artificial.db")

# Funcion para obtener los datos meteorologicos desde la base de datos
def obtener_datos_meteorologicos():
    with sqlite3.connect("vision_artificial.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM datos_meteorologicos ORDER BY fecha_hora DESC LIMIT 1")
        return cursor.fetchone()

# Ruta para recibir datos meteorologicos desde la ESP32
@app.route("/datos", methods=["POST"])
def recibir_datos():
    try:
        # Obtener los datos JSON enviados por el ESP32
        datos = request.json
        print("Datos recibidos:", datos)
        
        # Insertar los datos en la base de datos
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor. execute('''
           INSERT INTO datos_meteorologicos (temperatura, presion, humedad, velocidad_viento, precipitacion, radiacion_solar)
           VALUES (?, ?, ?, ?, ?, ?)
        ''', (datos["temperatura"], datos["presion"], datos["humedad"], datos["velocidad_viento"], datos["precipitacion"], datos["radiacion_solar"]))
        conexion.commit()
        conexion.close()
        return jsonify({"mensaje": "Datos almacenados correctamente"}), 200
    except Exception as e:
        print("Error al procesar los datos:", e)
        return jsonify({"error": str(e)}), 500
    
# Ruta para procesar imagenes (activa por el boton en el frontend)
@app.route("/procesar_imagen", methods=["POST"])
def procesar_imagen():
    try:
        # Crear una instancia del detector de enfermedades
        def procesar():
            detector = DetectorEnfermedades()
            detector.procesar_imagen()
            
        threading.Thread(target=procesar).start()
        return jsonify({"success": True, "message": "Procesamiento de imagen iniciado"}), 200
    except Exception as e:
        print("Error al procesar la imagen: ", e)
        return jsonify({"success": False, "message": str(e)}), 500

# Ruta para procesar videos (activada por el boton en el frontend)
@app.route("/procesar_video", methods=["POST"])
def procesar_video():
    try:
        # Crear una instancia del detector y procesar el video en un hilo separado para no bloquear Flask       
        def procesar():
            detector = DetectorEnfermedades()
            detector.procesar_video()
        
        threading.Thread(target=procesar).start()
        
        return jsonify({"success": True, "message": "Procesamiento de video iniciado"}), 200
    except Exception as e:
        print("Error al procesar el video: ", e)
        return jsonify({"success": False, "message": str(e)}), 500

# Ruta para manejar el login
@app.route("/login", methods=["POST"])
def login():
    try:
        # Obtener los datos del formulario de login
        data = request.json
        username = data.get("username")
        password = data.get("password")
        
        # Verificar las credenciales 
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            return jsonify({"success": True, "message": "Login exitoso"}), 200
        else:
            return jsonify({"success": False, "message": "Usuario o contraseña incorrectos"}), 401
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# Función para enviar datos meteorológicos automáticamente
def enviar_datos_automaticamente():
    while True:
        datos = obtener_datos_meteorologicos()
        if datos:
            socketio.emit("actualizar_datos_meteorologicos", {
                "fecha_hora": datos[1],
                "temperatura": datos[2],
                "presion": datos[3],
                "humedad": datos[4],
                "velocidad_viento": datos[5],
                "precipitacion": datos[6],
                "radiacion_solar": datos[7],
            })
        else:
            socketio.emit("actualizar_datos_meteorologicos", {"error": "No hay datos disponibles"})
        time.sleep(5)  # Enviar datos cada 5 segundos

# Iniciar el servidor Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
        