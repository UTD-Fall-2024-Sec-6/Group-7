import React from "react";
import Signin from "./Signin.jsx";
import Signup from "./Signup.jsx";
import Homepage from "./homepage.jsx"; // Import Homepage
import "./App.css";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Signin />} />
        <Route path="/signin" element={<Signin />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/app" element={<Homepage />} />
      </Routes>
    </Router>
  );
}

export default App;
