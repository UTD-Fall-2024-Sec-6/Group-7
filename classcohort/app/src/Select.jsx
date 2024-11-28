import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Select = () => {
    const navigate = useNavigate();
    const [courses] = useState([
        { name: "CS 3354", location: "ECS 1.205", memberLimit: 24 },
        { name: "CS 4341", location: "ECS 1.206", memberLimit: 7 },
        { name: "CS 3230", location: "ECS 2.101", memberLimit: 26 },
        { name: "CS 2305", location: "ECS 2.102", memberLimit: 15 },
    ]);

    return (
        <>
            <main className="h-screen flex items-center justify-center">
                <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-4xl">
                    { }
                    <h2 className="text-xl font-bold text-center mb-6">
                        Your Study Groups
                    </h2>

                    { }
                    <div className="grid grid-cols-2 gap-6 md:grid-cols-3 lg:grid-cols-4">
                        {courses.map((course, index) => (
                            <div key={index} className="bg-blue-100 p-6 rounded-lg shadow-lg text-center flex flex-col items-center">
                                <h3 className="text-lg font-bold mb-2">{course.name}</h3>
                                <p className="text-sm mb-2">Located in {course.location}</p>
                                <p className="text-sm mb-4">{course.memberLimit} Members</p>
                                <button
                                    onClick={() => navigate("/chat")}
                                    className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                                >
                                    Select
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            </main>
        </>
    );
};

export default Select;
