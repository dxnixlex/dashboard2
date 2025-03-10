import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { io } from "socket.io-client";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import axios from "axios";
import "leaflet/dist/leaflet.css";
import "../styles/Dashboard.css";

const Dashboard = () => {

  // Constante de navegacion para volver a la raiz
  const navigate = useNavigate();
  const handleLogout = () => {
    navigate("/");
  };

  //------------------------------------------------------------------------------------------------
  // Estado para almacenar los datos de Tarjetas Resumen
  const [data, setData] = useState({
    treesMonitored: 0,
    ripePeaches: 0,
    greenPeaches: 0,
    detectedCases: 0
  });
  // Funcion para obtener los datos del backend
  const fetchData = async () => {
    try {
      const response = await axios.get("http:localhost:5000");
      setData(response.data);         // Actualiza el estado con los datos obtenidos
    } catch (error){
      console.error("Error fetching data: ", error);
    }    
  }
  // useEffect para cargar los datos cuando el componente se monta
  useEffect( () => {
    fetchData();
  }, []);
  //------------------------------------------------------------------------------------------------
  // Estado para almacenar los datos de Tarjeta de Alertas

  //------------------------------------------------------------------------------------------------
  // Estado para almacenar los datos de Tiempo
  const [sensorData, setSensorData] = useState({
    temperature: 0,
    humidity: 0,
    pressure: 0,
    windSpeed: 0,
    precipitation: 0,
    solarRadiation: 0
  });
  // Conectar al servidor WebSocket
  useEffect( () => {
    const socket = io("http://localhost:5000");
    //Escuchar actualizaciones de datos de sensores
    socket.on("update_sensor_data", (data) => {
      setSensorData(data);              // Actualiza el estado con los nuevos datos
    });
    //Limpiar la conexion al desmontar el componente
    return () => {
      socket.disconnect();
    };
  }, []);
  //------------------------------------------------------------------------------------------------

  return (
    <div className="container">
      
      {/* Menú lateral */}
      <aside className="sidebar">
        <div className="user-info">Nombre de Usuario</div>
        <nav className="nav-links">
          <Link to="/analizar-video">Analizar Video</Link>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/imagenes-detectadas">Imágenes Detectadas</Link>
          <Link to="/acciones-recomendadas">Acciones Recomendadas</Link>
          <Link to="/predicciones">Predicciones de tiempo</Link>
        </nav>
        <button className="logout" onClick={handleLogout}>Cerrar Sesión</button>
      </aside>

      {/* Contenido principal */}
      <main className="main-content">
        <h1 className="title">ANÁLISIS DE VISIÓN ARTIFICIAL</h1>

        {/* Tarjetas de resumen */}
        <div className="cards-container">

          <div className="card">🌳 {data.treesMonitored} Árboles Monitoreados</div>
          <div className="card">🍑 {data.ripePeaches} Duraznos Maduros</div>
          <div className="card">🍏 {data.greenPeaches} Duraznos Verdes</div>
          <div className="card alert">⚠️ {data.detectedCases} Casos Detectados</div>

        </div>

        {/* Cuadro de datos de clima */}
        <div className="data-sections">

          <div className="data-box">
            <h2>Datos Meteorológicos</h2>
            <p>🌡️ Temperatura: {sensorData.temperature}°C</p>
            <p>💧 Humedad Relativa: {sensorData.humidity}%</p>
            <p>🌬️ Presión Atmosférica: {sensorData.pressure} hPa</p>
            <p>💨 Velocidad del Viento: {sensorData.windSpeed} km/h</p>
            <p>🌧️ Cantidad de Precipitación: {sensorData.precipitation} mm</p>
            <p>☀️ Radiación Solar: {sensorData.solarRadiation} W/m²</p>
          </div>

          <div className="data-box alerts">
            <h2>⚠️ Alertas Activas</h2>
            <ul>
              <li>Monilia: 20 Casos</li>
              <li>Oídio: 3 Casos</li>
              <li>Tiro: 6 Casos</li>
              <li>Taphrina: 23 Casos</li>
            </ul>
          </div>

          


        </div>


        {/* Geolocalización */}
        <div className="data-box">
            <h2>Ubicación de la Detección</h2>
            <MapContainer center={[-17.517587, -65.896741]} zoom={13} className="map">
              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              />
              <Marker position={[-17.517587, -65.896741]}>
                <Popup>Ubicación de la detección</Popup>
              </Marker>
              <Marker position={[-17.517655, -65.896976]}>
                <Popup>Ubicación de la detección</Popup>
              </Marker>
              <Marker position={[-17.517765, -65.897272]}>
                <Popup>Ubicación de la detección</Popup>
              </Marker>
              <Marker position={[-17.517912, -65.897198]}>
                <Popup>Ubicación de la detección</Popup>
              </Marker>
              <Marker position={[-17.517987, -65.897174]}>
                <Popup>Ubicación de la detección</Popup>
              </Marker>
              <Marker position={[-17.518077, -65.897134]}>
                <Popup>Ubicación de la detección</Popup>
              </Marker>
              <Marker position={[-17.517892, -65.896486]}>
                <Popup>Ubicación de la detección</Popup>
              </Marker>
            </MapContainer>
          </div>


      </main>
    </div>
  );
};

export default Dashboard;
