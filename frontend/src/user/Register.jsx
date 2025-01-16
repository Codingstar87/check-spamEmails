import React, { useState } from 'react';
import axios from 'axios';

// Axios instance with credentials and base URL
const api = axios.create({
    baseURL: '/auth', 
    withCredentials: true, // Ensures cookies are included in requests
});

function Register() {
    const [formData, setFormData] = useState({ username: '', email: '', password: '' });
    const [message, setMessage] = useState('');

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await api.post('/register', formData);
            setMessage(response.data.message || 'User registered successfully!');
        } catch (error) {
            if (error.response && error.response.data) {
                // Extracting detail from backend error response
                setMessage(error.response.data.detail || 'Error: Registration failed.');
            } else {
                // Handling unexpected errors
                setMessage('Error: Something went wrong. Please try again.');
            }
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <h1>Register</h1>
                <input
                    type="text"
                    name="username"
                    placeholder="Username"
                    value={formData.username}
                    onChange={handleChange}
                    required
                />
                <input
                    type="email"
                    name="email"
                    placeholder="Email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                />
                <input
                    type="password"
                    name="password"
                    placeholder="Password"
                    value={formData.password}
                    onChange={handleChange}
                    required
                />
                <button type="submit">Register</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
}

export default Register;
