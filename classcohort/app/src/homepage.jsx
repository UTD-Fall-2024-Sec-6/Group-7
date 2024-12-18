import { useNavigate } from "react-router-dom";
import React from "react";
import { FiLogOut } from "react-icons/fi"; // Importing a logout icon from react-icons

const Homepage = () => {
  const navigate = useNavigate();

  const handleSignOut = () => {
    // Perform sign-out logic here, e.g., clear authentication tokens, etc.
    navigate("/signin"); // Navigate to sign-in page or other appropriate route
  };

  return (
    <>
      <main className="h-screen flex items-center justify-center">
        <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-sm relative">
          {/* Sign Out Icon */}
          <button
            onClick={handleSignOut}
            className="absolute top-4 right-4 text-red-500 hover:text-red-600"
            aria-label="Sign Out"
          >
            <FiLogOut size={20} />
          </button>

          {/* Centered Title */}
          <h2 className="text-xl font-bold text-center mb-4">Homepage</h2>

          {/* Buttons */}
          <div className="flex justify-center space-x-4 mt-4">
            <button
              onClick={() => navigate("/create")}
              className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
            >
              Create
            </button>
            <button
              onClick={() => navigate("/select")}
              className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              Select
            </button>
            <button
              onClick={() => navigate("/join")}
              className="px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600"
            >
              Join
            </button>
          </div>
        </div>
      </main>
    </>
  );
};

export default Homepage;
