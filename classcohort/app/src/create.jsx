import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FiLogOut, FiHome } from "react-icons/fi"; // Importing icons

const CreateStudyGroup = () => {
  const navigate = useNavigate();

  const courseOptions = ["CS 3354", "CS 4341", "CS 3230", "CS 2305"];
  const locationOptions = ["ECS 1.205", "ECS 1.206", "ECS 2.101", "ECS 2.102"];

  const [courseName, setCourseName] = useState(courseOptions[0]); // Default to first option
  const [location, setLocation] = useState(locationOptions[0]); // Default to first option
  const [memberLimit, setMemberLimit] = useState(6);
  const [dateTime, setDateTime] = useState("");
  const [dateError, setDateError] = useState(""); // To handle date/time errors

  const handleIncrement = () => {
    setMemberLimit((prev) => prev + 1);
  };

  const handleDecrement = () => {
    if (memberLimit > 1) setMemberLimit((prev) => prev - 1);
  };

  const handleSignOut = () => {
    navigate("/signin");
  };

  const handleHomePage = () => {
    navigate("/app");
  };

  const handleDateChange = (value) => {
    setDateTime(value);
    if (new Date(value) <= new Date()) {
      setDateError("Please select a valid future date and time.");
    } else {
      setDateError("");
    }
  };

  const handleConfirm = () => {
    // Validate Date/Time
    if (!dateTime || new Date(dateTime) <= new Date()) {
      setDateError("Please select a valid future date and time.");
      return;
    }

    // Validate Member Limit
    if (memberLimit <= 0) {
      alert("Member limit must be greater than 0!");
      return;
    }

    // Save the study group information and navigate to the Select page
    const newStudyGroup = { courseName, location, memberLimit, dateTime };

    // Retrieve existing study groups from localStorage
    const existingGroups =
      JSON.parse(localStorage.getItem("studyGroups")) || [];

    // Add new study group
    const updatedGroups = [...existingGroups, newStudyGroup];
    localStorage.setItem("studyGroups", JSON.stringify(updatedGroups));

    // Navigate to the Select page
    navigate("/select");
  };

  return (
    <>
      <main className="h-screen flex items-center justify-center">
        <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-2xl relative">
          {/* Navigation Buttons */}
          <div className="absolute top-4 right-4 flex space-x-2">
            {/* Homepage Button */}
            <button
              onClick={handleHomePage}
              className="text-blue-500 hover:text-blue-600 px-3 py-2 rounded-lg border border-blue-500 hover:bg-blue-100 flex items-center space-x-1"
              aria-label="HomePage"
            >
              <FiHome size={20} />
            </button>

            {/* Sign Out Button */}
            <button
              onClick={handleSignOut}
              className="text-red-500 hover:text-red-600 px-3 py-2 rounded-lg border border-red-500 hover:bg-red-100 flex items-center space-x-1"
              aria-label="Sign Out"
            >
              <FiLogOut size={20} />
            </button>
          </div>

          {/* Header */}
          <h2 className="text-xl font-bold text-center mb-4">
            Create Study Group
          </h2>

          {/* Main Content */}
          <div className="space-y-4">
            {/* Course Name Dropdown */}
            <div>
              <label className="block text-sm font-bold">Course Name</label>
              <select
                value={courseName}
                onChange={(e) => setCourseName(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {courseOptions.map((course) => (
                  <option key={course} value={course}>
                    {course}
                  </option>
                ))}
              </select>
            </div>

            {/* Location Dropdown */}
            <div>
              <label className="block text-sm font-bold">Location</label>
              <select
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {locationOptions.map((loc) => (
                  <option key={loc} value={loc}>
                    {loc}
                  </option>
                ))}
              </select>
            </div>

            {/* Date/Time Picker */}
            <div>
              <label className="block text-sm font-bold">Date/Time</label>
              <input
                type="datetime-local"
                value={dateTime}
                onChange={(e) => handleDateChange(e.target.value)}
                className={`w-full px-3 py-2 border ${
                  dateError ? "border-red-500" : "border-gray-300"
                } rounded-lg focus:outline-none focus:ring-2 ${
                  dateError ? "focus:ring-red-500" : "focus:ring-blue-500"
                }`}
              />
              {dateError && (
                <p className="text-red-500 text-sm mt-1">{dateError}</p>
              )}
            </div>

            {/* Member Limit */}
            <div>
              <label className="block text-sm font-bold text-center">
                Member Limit
              </label>
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

          {/* Confirm Button */}
          <div className="flex justify-center mt-6">
            <button
              onClick={handleConfirm}
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
