import React, { useState } from 'react';
import Form from 'react-bootstrap/Form';
import FloatingLabel from 'react-bootstrap/FloatingLabel';
import Button from 'react-bootstrap/Button';
import { useAuth } from './AuthContext';
import { useNavigate } from 'react-router-dom';

const SignupForm = () => {
    const { signup } = useAuth();
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (password !== confirmPassword) {
            return setError('Passwords do not match');
        }
        try {
            await signup(email, password);
            navigate('/landing'); // Redirect after signup
        } catch (err) {
            if (err.code === 'auth/email-already-in-use') {
                setError('Email already in use. Please log in.');
            } else {
                setError('Failed to create an account. Please try again.');
            }
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                {error && <p style={{ color: 'red' }}>{error}</p>}
                
                <Form.Group className="mb-3" controlId="formBasicEmail">
                    <FloatingLabel
                        controlId="floatingInput"
                        label="Email address"
                        className="mb-3"
                    >
                        <Form.Control
                            type="email"
                            placeholder="Enter email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </FloatingLabel>
                </Form.Group>
                
                <Form.Group className="mb-3" controlId="formBasicPassword">
                    <FloatingLabel controlId="floatingPassword" label="Password">
                        <Form.Control
                            type="password"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </FloatingLabel>
                </Form.Group>
                {/* Confirm Password Field */}
                <Form.Group className="mb-3" controlId="formBasicConfirmPassword">
                    <FloatingLabel controlId="floatingConfirmPassword" label="Confirm Password">
                        <Form.Control
                            type="password"
                            placeholder="Confirm Password"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            required
                        />
                    </FloatingLabel>
                </Form.Group>
                <Button variant="primary" type="submit">
                    Sign Up
                </Button>
            </form>
        </div>
    );
};

export default SignupForm;
