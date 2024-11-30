import React, { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { FiLogOut, FiHome } from "react-icons/fi"; // Importing icons

const ChatPage = () => {
  const [chats, setChats] = useState([
    { id: 1, name: "Chat 1" },
    { id: 2, name: "Chat 2" },
    { id: 3, name: "Chat 3" },
    { id: 4, name: "Chat 4" },
    { id: 5, name: "Chat 5" },
    { id: 6, name: "Chat 6" },
  ]);
  const [currentChatId, setCurrentChatId] = useState(1);
  const [chatHistories, setChatHistories] = useState({
    1: [{ id: 1, text: "Hello!", sender: "me" }],
    2: [{ id: 1, text: "Welcome to Chat 2", sender: "them" }],
    3: [{ id: 1, text: "Welcome to Chat 3", sender: "them" }],
    4: [{ id: 1, text: "Welcome to Chat 4", sender: "them" }],
    5: [{ id: 1, text: "Welcome to Chat 5", sender: "them" }],
    6: [{ id: 1, text: "Welcome to Chat 6", sender: "them" }],
  });
  const [newMessage, setNewMessage] = useState("");
  const chatBoxRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [chatHistories[currentChatId]]);

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    const userMessage = { id: Date.now(), text: newMessage, sender: "me" };
    setChatHistories((prevHistories) => ({
      ...prevHistories,
      [currentChatId]: [...prevHistories[currentChatId], userMessage],
    }));
    setNewMessage("");

    setTimeout(() => {
      const botMessage = {
        id: Date.now() + 1,
        text: "I'm a chatbot! How can I help?",
        sender: "them",
      };
      setChatHistories((prevHistories) => ({
        ...prevHistories,
        [currentChatId]: [...prevHistories[currentChatId], botMessage],
      }));
    }, 1000);
  };

  const handleChatSwitch = (chatId) => {
    setCurrentChatId(chatId);

    setChatHistories((prevHistories) => ({
      ...prevHistories,
      [chatId]: prevHistories[chatId] || [],
    }));
  };

  const handleHomePage = () => {
    navigate("/app");
  };

  const handleSignOut = () => {
    navigate("/signin");
  };

  return (
    <>
      <main className="h-screen flex items-center justify-center">
        <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-4xl relative">
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
            {chats.find((chat) => chat.id === currentChatId)?.name || "Message"}
          </h2>

          {/* Main Content */}
          <div className="flex space-x-6">
            {/* Left Section: Recent Chats */}
            <div className="space-y-4 w-1/4">
              <h3 className="text-lg font-bold text-center">Recent Chats</h3>
              <div
                className="bg-blue-100 rounded-lg p-2 space-y-2 overflow-y-auto"
                style={{ maxHeight: "300px" }}
              >
                {chats.map((chat) => (
                  <p
                    key={chat.id}
                    onClick={() => handleChatSwitch(chat.id)}
                    className={`p-2 rounded-lg text-center cursor-pointer ${
                      currentChatId === chat.id
                        ? "bg-blue-500 text-white"
                        : "bg-blue-200 hover:bg-blue-300"
                    }`}
                  >
                    {chat.name}
                  </p>
                ))}
              </div>
            </div>

            {/* Right Section: Chat Box */}
            <div className="flex-grow bg-blue-100 rounded-lg flex flex-col">
              {/* Chat Messages */}
              <div
                className="flex-grow p-4 overflow-y-auto max-h-64"
                ref={chatBoxRef}
              >
                {(chatHistories[currentChatId] || []).map((msg) => (
                  <div
                    key={msg.id}
                    className={`flex ${
                      msg.sender === "me" ? "justify-end" : "justify-start"
                    } mb-2`}
                  >
                    <p
                      className={`${
                        msg.sender === "me"
                          ? "bg-blue-500 text-white"
                          : "bg-blue-200 text-gray-800"
                      } px-4 py-2 rounded-lg max-w-xs`}
                    >
                      {msg.text}
                    </p>
                  </div>
                ))}
              </div>

              {/* Input Area */}
              <form
                onSubmit={handleSendMessage}
                className="bg-blue-300 p-4 flex items-center"
              >
                <input
                  type="text"
                  placeholder="Type a message..."
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                  className="flex-grow border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                  type="submit"
                  className="ml-4 bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600"
                >
                  Send
                </button>
              </form>
            </div>
          </div>
        </div>
      </main>
    </>
  );
};

export default ChatPage;
