import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import React from "react";
import { auth } from "./firebase";
import { signInWithEmailAndPassword } from "firebase/auth";

const Signin = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState(""); // State for error messages
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage(""); // Clear previous errors
    try {
      await signInWithEmailAndPassword(auth, email, password);
      console.log("User signed in successfully");
      navigate("/app");
    } catch (error) {
      console.error("Error during sign-in:", error.message);
      setErrorMessage(error.message); // Set error message to display
    }
  };

  return (
    <>
      <main className="h-screen flex items-center justify-center">
        <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-sm">
          <h2 className="text-xl font-bold text-center mb-4">Sign In</h2>
          {errorMessage && ( // Conditionally display the error message
            <div className="text-red-500 text-center mb-4">
              {errorMessage}
            </div>
          )}
          <form className="signin-form" onSubmit={handleSubmit}>
            <div className="mb-4">
              <label
                className="block text-gray-700 text-sm font-bold mb-2"
                htmlFor="email"
              >
                Email
              </label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
            <div className="mb-4">
              <label
                className="block text-gray-700 text-sm font-bold mb-2"
                htmlFor="password"
              >
                Password
              </label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
            <button
              type="submit"
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg w-full focus:outline-none focus:ring-2 focus:ring-blue-700"
            >
              Sign In
            </button>
          </form>
          <p className="mt-4 text-center">
            Don't have an account?{" "}
            <Link to="/signup" className="text-blue-600 hover:underline">
              Sign Up
            </Link>
          </p>
        </div>
      </main>
    </>
  );
};

export default Signin;
