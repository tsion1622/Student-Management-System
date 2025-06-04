// src/components/Login.js
import React, { useState } from 'react';
import axios from '../api';
import { useNavigate } from 'react-router-dom';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('/accounts/login/', { username, password });
      const { access } = res.data;
      localStorage.setItem('token', access);

      // Get user data
      const userRes = await axios.get('/accounts/me/', {
        headers: { Authorization: `Bearer ${access}` },
      });

      const user = userRes.data;
      if (user.role === 'teacher') {
        navigate('/teacher');
      } else {
        navigate('/student');
      }
    } catch (err) {
      alert('Invalid credentials');
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <input value={username} onChange={e => setUsername(e.target.value)} placeholder="Username" />
        <input value={password} type="password" onChange={e => setPassword(e.target.value)} placeholder="Password" />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;
