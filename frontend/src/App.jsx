// App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Register from './user/Register';
import Login from './user/Login';

function App() {
    return (
        <Router>
            <nav>
                <Link to="/register">Register</Link>
                <Link to="/login">Login</Link>
            </nav>
            <Routes>
                {/* Define route for root path */}
                <Route path="/" element={<div>Welcome to the Home Page!</div>} /> {/* Add a default route for / */}
                <Route path="/register" element={<Register />} />
                <Route path="/login" element={<Login />} />
            </Routes>
        </Router>
    );
}

export default App;



