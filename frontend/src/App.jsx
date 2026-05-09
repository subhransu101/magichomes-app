import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Building2 } from 'lucide-react';
import HomePage from './pages/HomePage';
import PropertyPage from './pages/PropertyPage';
import './index.css';

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <header className="header">
          <div className="container header-content">
            <a href="/" className="logo">
              <Building2 size={32} />
              MagicHomes
            </a>
          </div>
        </header>

        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/property/:id" element={<PropertyPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
