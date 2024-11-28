import React from "react";
import Signin from "./Signin.jsx";
import Signup from "./Signup.jsx";
import Homepage from "./homepage.jsx";
import Create from "./create.jsx";
import Join from "./join.jsx";
import Chat from "./chat.jsx";
import Select from "./Select.jsx"
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
        <Route path="/create" element={<Create />} />
        <Route path="/join" element={<Join />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/select" element={<Select />} />
      </Routes>
    </Router>
  );
}

export default App;
