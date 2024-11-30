import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { FiLogOut, FiHome } from "react-icons/fi"; // Importing icons

const Select = () => {
  const navigate = useNavigate();

  // Retrieve study groups from localStorage or use predefined courses
  const [courses, setCourses] = useState(
    JSON.parse(localStorage.getItem("studyGroups")) || []
  );

  useEffect(() => {
    // Update localStorage when courses change
    localStorage.setItem("studyGroups", JSON.stringify(courses));
  }, [courses]);

  const handleHomePage = () => {
    navigate("/app");
  };

  const handleSignOut = () => {
    navigate("/signin");
  };

  const handleDelete = (index) => {
    const updatedCourses = courses.filter((_, i) => i !== index);
    setCourses(updatedCourses);
    localStorage.setItem("studyGroups", JSON.stringify(updatedCourses)); // Update localStorage
  };

  return (
    <>
      <main className="h-screen flex items-center justify-center">
        <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-4xl relative">
          {/* Navigation Buttons */}
          <div className="absolute top-4 right-4 flex space-x-2">
            {/* HomePage Button */}
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

          {/* Title */}
          <h2 className="text-xl font-bold text-center mb-6">
            Your Study Groups
          </h2>

          {/* Courses Section */}
          {courses.length > 0 ? (
            <div
              className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3 overflow-y-auto"
              style={{ maxHeight: "400px" }} // Add scroll if there are many groups
            >
              {courses.map((course, index) => (
                <div
                  key={index}
                  className="relative bg-blue-100 p-6 rounded-lg shadow-lg text-center flex flex-col items-center"
                >
                  <h3 className="text-lg font-bold mb-2">{course.name}</h3>
                  <p className="text-sm mb-2">
                    <strong>Course Number:</strong> {course.courseName}
                  </p>
                  <p className="text-sm mb-2">
                    <strong>Location:</strong> {course.location}
                  </p>
                  <p className="text-sm mb-4">
                    <strong>Members:</strong> {course.memberLimit}
                  </p>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => navigate("/chat")}
                      className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                    >
                      Select
                    </button>
                    <button
                      onClick={() => handleDelete(index)}
                      className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center h-64">
              <p className="text-center text-gray-500">
                No study groups available. Create one to get started!
              </p>
            </div>
          )}
        </div>
      </main>
    </>
  );
};

export default Select;
