import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import KeyboardDemo from './pages/KeyboardDemo';
import Analyzer from './pages/Analyzer';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="demo" element={<KeyboardDemo />} />
          <Route path="analyzer" element={<Analyzer />} />
          <Route path="data" element={<div className="p-8"><h2>Dataset & Scraper (To Be Implemented)</h2></div>} />
        </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
);
