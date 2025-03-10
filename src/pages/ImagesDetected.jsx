import React from "react";
import { Link, useNavigate } from "react-router-dom";
import "../styles/ImagesDetected.css";

const ImagesDetected = () => {

    const navigate = useNavigate();
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
                <button className="logout">Cerrar Sesión</button>
            </aside>

            <main className="main-content">
                <h1 className="title">IMÁGENES DETECTADAS</h1>
                {/* Resto del contenido */}
            </main>
        </div>
    )
    
    
};

export default ImagesDetected;
