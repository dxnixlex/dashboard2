import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import ImagesDetected from "./pages/ImagesDetected";
import RecommendedActions from "./pages/RecommendedActions";
import WeatherPredictions from "./pages/WeatherPredictions";
import Login from "./pages/Login";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/imagenes-detectadas" element={<ImagesDetected />} />
        <Route path="/acciones-recomendadas" element={<RecommendedActions />} />
        <Route path="/predicciones" element={<WeatherPredictions />} />
      </Routes>
    </Router>
  );
}

export default App;