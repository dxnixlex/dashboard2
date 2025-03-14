import cv2
import os
import sqlite3
from ultralytics import YOLO
from datetime import datetime

class DetectorEnfermedades:
    def __init__(self):
        # Rutas fijas (ajusta estas rutas según tu sistema)
        self.modelo_path = "yolo11x.pt"
        self.video_path = "C:/Users/WIN11/Desktop/Dashboard/complemento/backend/input/Professional_Mode_generates_a_realistic_high_defin.mp4"
        self.output_folder = "C:/Users/WIN11/Desktop/Dashboard/complemento/backend/output"
        self.db_path = "vision_artificial.db"  # Ruta de la base de datos
        self.labels = ['fruto_maduro', 'fruto_monilia', 'fruto_oidiosis', 
                      'fruto_tiro', 'fruto_verde', 'hoja_taphrina']  # Etiquetas del modelo

        # Cargar el modelo YOLO
        self.model = YOLO(self.modelo_path)

    def almacenar_detecciones(self, detecciones):
        """Almacena las detecciones en la tabla 'registros' de la base de datos."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for etiqueta, cantidad in detecciones.items():
                if cantidad > 0:
                    cursor.execute('''
                        INSERT INTO registros (latitud, longitud, tipo_dato, valor)
                        VALUES (?, ?, ?, ?)
                    ''', (0.0, 0.0, etiqueta, cantidad))  # Omite latitud y longitud por ahora
            conn.commit()

    def procesar_frame(self, frame):
        """Procesa un frame del video y devuelve el frame con las detecciones dibujadas."""
        results = self.model.predict(source=frame, conf=0.3)
        detections_count = {label: 0 for label in self.labels}
        has_detections = False
        
        if not results:
            return frame, detections_count, has_detections
        
        for result in results:
            for box in result.boxes:
                if len(box.cls) > 0:
                    has_detections = True
                    class_id = int(box.cls[0])
                    if class_id < len(self.labels):
                        label = self.labels[class_id]
                        detections_count[label] += 1
                        
                        # Dibujar detecciones en el frame
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, f"{label}", (x1, y1 - 10),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return frame, detections_count, has_detections

    def redimensionar_frame(self, frame, width=640):
        """Redimensiona el frame manteniendo la proporción de aspecto."""
        height = int(frame.shape[0] * (width / frame.shape[1]))
        return cv2.resize(frame, (width, height))

    def procesar_video(self):
        """Procesa el video y almacena las detecciones en la base de datos."""
        if not os.path.exists(self.video_path):
            print(f"Error: El archivo de video no existe en la ruta: {self.video_path}")
            return

        os.makedirs(self.output_folder, exist_ok=True)
        cap = cv2.VideoCapture(self.video_path)
        
        if not cap.isOpened():
            print(f"Error: No se pudo abrir el video en la ruta: {self.video_path}")
            return

        filename = os.path.basename(self.video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_skip = 20  # Procesar 1 de cada 15 frames
        frame_count = 0
        detection_count = 0
        acumulado_detecciones = {label: 0 for label in self.labels}
        
        print(f"Procesando video: {filename}")
        print(f"Total frames: {total_frames}")
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            if frame_count % frame_skip != 0:
                continue
            
            frame_resized = self.redimensionar_frame(frame)
            processed_frame, detections, has_detections = self.procesar_frame(frame_resized)
            
            if has_detections:
                detection_count += 1
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = os.path.join(self.output_folder, f"detection_{timestamp}_{detection_count}.jpg")
                cv2.imwrite(output_path, processed_frame)
                
                for label, count in detections.items():
                    acumulado_detecciones[label] += count
            
            if frame_count % 100 == 0:
                progress = (frame_count / total_frames) * 100
                print(f"Progreso: {progress:.1f}% - Detecciones encontradas: {detection_count}")
        
        cap.release()
        
        if any(acumulado_detecciones.values()):
            self.almacenar_detecciones(acumulado_detecciones)
            
        print(f"\nProcesamiento completado:")
        print(f"- Frames totales procesados: {frame_count}")
        print(f"- Imágenes con detecciones guardadas: {detection_count}")
        print(f"- Detecciones por categoría:")
        for label, count in acumulado_detecciones.items():
            if count > 0:
                print(f"  {label}: {count}")

# Si el script se ejecuta directamente, procesar el video
if __name__ == "__main__":
    detector = DetectorEnfermedades()
    detector.procesar_video()