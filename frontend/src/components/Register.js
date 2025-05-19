import React, { useState } from "react";
import { registerUser, confirmUser } from "../services/api"; // Import API service functions

const Register = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });
  const [confirmationCode, setConfirmationCode] = useState("");
  const [isRegistered, setIsRegistered] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState(null); // Tracks errors

  // Handle form input changes
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Submit registration form
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null); // Reset error
    try {
      await registerUser(formData); // Call the API to register the user
      setIsRegistered(true); // Switch to confirmation step
      setMessage("Registration successful! Check your email for the confirmation code.");
    } catch (error) {
      setError(error.response?.data?.error || "Registration failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  // Submit confirmation form
  const handleConfirm = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null); // Reset error
    try {
      await confirmUser(formData.email, confirmationCode); // Call the API to confirm the user
      setMessage("Account confirmed successfully! You can now log in.");
    } catch (error) {
      setError(error.response?.data?.error || "Confirmation failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-5">
      <h2 className="text-center">{!isRegistered ? "Register" : "Confirm Registration"}</h2>
      {error && <p className="text-danger text-center">{error}</p>} {/* Displays error message */}
      {!isRegistered ? (
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Username</label>
            <input
              type="text"
              name="username"
              className="form-control"
              value={formData.username}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              name="email"
              className="form-control"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              name="password"
              className="form-control"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>
          <button type="submit" className="btn btn-primary btn-block" disabled={loading}>
            {loading ? "Registering..." : "Register"}
          </button>
        </form>
      ) : (
        <form onSubmit={handleConfirm}>
          <div className="form-group">
            <label>Confirmation Code</label>
            <input
              type="text"
              className="form-control"
              value={confirmationCode}
              onChange={(e) => setConfirmationCode(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="btn btn-success btn-block" disabled={loading}>
            {loading ? "Confirming..." : "Confirm"}
          </button>
        </form>
      )}
      {message && <p className="mt-3 text-center">{message}</p>}
    </div>
  );
};

export default Register;