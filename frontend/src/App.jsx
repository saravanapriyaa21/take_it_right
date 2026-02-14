import { BrowserRouter, Routes, Route } from "react-router-dom";
import InputPage from "./pages/InputPage";
import Dashboard from "./pages/Dashboard";
import { useState } from "react";

export default function App() {
  const [result, setResult] = useState(null);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<InputPage setResult={setResult} />} />
        <Route path="/dashboard" element={<Dashboard result={result} />} />
      </Routes>
    </BrowserRouter>
  );
}
