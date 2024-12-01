import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { FiLogOut, FiHome } from "react-icons/fi";

const JoinGroup = () => {
  const navigate = useNavigate();

  const [studyGroups, setStudyGroups] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedGroup, setSelectedGroup] = useState(null);
  const [showDropdown, setShowDropdown] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const dropdownRef = useRef(null);

  const currentUser = "currentUser";

  useEffect(() => {
    const existingGroups = JSON.parse(localStorage.getItem("studyGroups")) || [];
    const defaultGroups = [
      {
        courseName: "Math 101",
        location: "Library Room 2",
        dateTime: new Date(new Date().setHours(0, 0, 0, 0)),
        memberLimit: 5,
        members: [],
      },
    ];

    const mergedGroups = [...existingGroups];

    defaultGroups.forEach((defaultGroup) => {
      const exists = existingGroups.some(
        (group) =>
          group.courseName === defaultGroup.courseName &&
          group.location === defaultGroup.location &&
          group.dateTime === defaultGroup.dateTime
      );

      if (!exists) {
        mergedGroups.push(defaultGroup);
      }
    });

    // Remove duplicates based on courseName
    const uniqueGroups = mergedGroups.filter((group, index, self) =>
      index === self.findIndex((g) => g.courseName === group.courseName)
    );

    localStorage.setItem("studyGroups", JSON.stringify(uniqueGroups));
    setStudyGroups(uniqueGroups);
  }, []);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowDropdown(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const handleSearch = (query) => {
    setSearchQuery(query);

    const matches = studyGroups.filter(
      (group) =>
        group.courseName.toLowerCase().includes(query.toLowerCase()) ||
        group.location.toLowerCase().includes(query.toLowerCase())
    );

    if (query && matches.length === 0) {
      setErrorMessage("No groups match your search query.");
    } else {
      setErrorMessage("");
    }
  };

  const handleSelectGroup = (group) => {
    setSelectedGroup(group);
    setSearchQuery(
      `${group.courseName} at ${group.location} on ${new Date(group.dateTime).toLocaleString()}`
    );
    setShowDropdown(false);
    setErrorMessage("");
  };

  const handleJoinGroup = () => {
    if (!selectedGroup) {
      alert("Please select a group to join!");
      return;
    }

    const { members = [], memberLimit } = selectedGroup;

    if (members.includes(currentUser)) {
      alert("You are already a member of this group!");
      return;
    }

    if (members.length >= memberLimit) {
      alert("This group is already full!");
      return;
    }

    const updatedGroups = studyGroups.map((group) => {
      if (group.dateTime === selectedGroup.dateTime) {
        return { ...group, members: [...members, currentUser] };
      }
      return group;
    });

    localStorage.setItem("studyGroups", JSON.stringify(updatedGroups));
    setStudyGroups(updatedGroups);

    alert(`You have successfully joined the group for ${selectedGroup.courseName}`);
    navigate("/app");
  };

  const handleSignOut = () => {
    navigate("/signin");
  };

  const handleHomePage = () => {
    navigate("/app");
  };

  const filteredGroups = studyGroups.filter(
    (group) =>
      group.courseName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      group.location.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <main className="h-screen flex items-center justify-center">
      <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-2xl relative">
        <div className="absolute top-4 right-4 flex space-x-2">
          <button
            onClick={handleHomePage}
            className="text-blue-500 hover:text-blue-600 px-3 py-2 rounded-lg border border-blue-500 hover:bg-blue-100 flex items-center space-x-1"
            aria-label="HomePage"
          >
            <FiHome size={20} />
          </button>
          <button
            onClick={handleSignOut}
            className="text-red-500 hover:text-red-600 px-3 py-2 rounded-lg border border-red-500 hover:bg-red-100 flex items-center space-x-1"
            aria-label="Sign Out"
          >
            <FiLogOut size={20} />
          </button>
        </div>

        <h2 className="text-xl font-bold text-center mb-4">Join a Study Group</h2>

        <div className="mb-4 relative" ref={dropdownRef}>
          <label className="block text-sm font-bold mb-2">Search & Select Group</label>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => handleSearch(e.target.value)}
            onFocus={() => setShowDropdown(true)}
            placeholder="Search by course or location"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          {errorMessage && (
            <p className="text-red-500 text-sm mt-1">{errorMessage}</p>
          )}
          {showDropdown && (
            <ul className="absolute bg-white border border-gray-300 rounded-lg mt-1 max-h-40 overflow-y-auto z-10 w-full">
              {filteredGroups.length > 0 ? (
                filteredGroups.map((group, index) => (
                  <li
                    key={index}
                    onClick={() => handleSelectGroup(group)}
                    className="px-4 py-2 hover:bg-gray-100 cursor-pointer"
                  >
                    {`${group.courseName} at ${group.location} on ${new Date(
                      group.dateTime
                    ).toLocaleString()}`}
                  </li>
                ))
              ) : (
                <li className="px-4 py-2 text-gray-500">No groups found</li>
              )}
            </ul>
          )}
        </div>

        <div className="flex justify-center mt-6">
          <button
            onClick={handleJoinGroup}
            className="px-6 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Join Group
          </button>
        </div>
      </div>
    </main>
  );
};

export default JoinGroup;
