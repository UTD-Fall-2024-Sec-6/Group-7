import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const CreateStudyGroup = () => {
  const navigate = useNavigate();
  const [courseName, setCourseName] = useState("CS 3354");
  const [location, setLocation] = useState("ECS 1.205");
  const [memberLimit, setMemberLimit] = useState(6);

  const handleIncrement = () => {
    setMemberLimit((prev) => prev + 1);
  };

  const handleDecrement = () => {
    if (memberLimit > 1) setMemberLimit((prev) => prev - 1);
  };

  return (
    <>
      <main className="h-screen flex items-center justify-center">
        <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-2xl">
          {/* Header */}
          <h2 className="text-xl font-bold text-center mb-4">
            Create Study Group
          </h2>

          {/* Main Content */}
          <div className="flex space-x-6">
            {/* Left Section: Inputs */}
            <div className="space-y-4 w-1/3">
              <div>
                <label className="block text-sm font-bold">Course Name</label>
                <input
                  type="text"
                  value={courseName}
                  onChange={(e) => setCourseName(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-bold">Location</label>
                <input
                  type="text"
                  value={location}
                  onChange={(e) => setLocation(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
  <label className="block text-sm font-bold text-center">Member Limit</label>
  <div className="flex justify-center items-center space-x-4 mt-2">
    <button
      onClick={handleDecrement}
      className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600"
    >
      -
    </button>
    <span className="text-lg font-bold">{memberLimit}</span>
    <button
      onClick={handleIncrement}
      className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600"
    >
      +
    </button>
  </div>
</div>

            </div>

            {/* Right Section: Preview Box */}
            <div className="flex-grow bg-blue-100 rounded-lg p-6 text-center">
              <h3 className="text-lg font-bold">{courseName}</h3>
              <p className="text-sm">Located in {location}</p>
              <p className="text-sm">
                {memberLimit} Members
              </p>
            </div>
          </div>

          {/* Confirm Button */}
          <div className="flex justify-center mt-6">
            <button
              onClick={() => navigate("/join")}
              className="px-6 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              Confirm
            </button>
          </div>
        </div>
      </main>
    </>
  );
};

export default CreateStudyGroup;
