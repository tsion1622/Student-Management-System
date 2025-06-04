import logo from './logo.svg';
import './App.css';

// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/Login';
import TeacherDashboard from './components/TeacherDashboard';
import StudentDashboard from './components/StudentDashboard';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/teacher" element={
          <ProtectedRoute><TeacherDashboard /></ProtectedRoute>
        } />
        <Route path="/student" element={
          <ProtectedRoute><StudentDashboard /></ProtectedRoute>
        } />
      </Routes>
    </Router>
  );
}

export default App;

