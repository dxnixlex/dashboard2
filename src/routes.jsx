import { Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import ImagesDetected from "./pages/ImagesDetected";
import RecommendedActions from "./pages/RecommendedActions";
import WeatherPredictions from "./pages/WeatherPredictions";

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/images-detected" element={<ImagesDetected />} />
      <Route path="/recommended-actions" element={<RecommendedActions />} />
      <Route path="/weather-predictions" element={<WeatherPredictions />} />
    </Routes>
  );
};

export default AppRoutes;
