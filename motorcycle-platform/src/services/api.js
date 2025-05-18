import axios from "axios";

// Base URL of your backend
const API_BASE_URL = "https://special-barnacle-x5pv7vr69pxqcv9jq-5000.app.github.dev";

// Function to register a user
export const registerUser = async (formData) => {
  const response = await axios.post(`${API_BASE_URL}/register`, formData);
  return response.data; // Returns the data from the backend
};

// Function to confirm a user
export const confirmUser = async (email, confirmationCode) => {
  const response = await axios.post(`${API_BASE_URL}/confirm`, {
    email,
    confirmationCode,
  });
  return response.data; // Returns the data from the backend
};