import React, { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { FiLogOut, FiHome } from "react-icons/fi";

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
  const [errorMessage, setErrorMessage] = useState(""); // Updated for inline error message
  const chatBoxRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [chatHistories[currentChatId]]);

  const handleSendMessage = (e) => {
    e.preventDefault();
    const sender = "me";
    const validUsers = ["me", "them"];
    const MAX_MESSAGE_LENGTH = 500;

    // Test Cases for Messages
    if (!validUsers.includes(sender)) {
      setErrorMessage("Invalid sender.");
      return;
    }

    if (!newMessage.trim()) {
      setErrorMessage("Message cannot be empty.");
      return;
    }

    if (newMessage.length > MAX_MESSAGE_LENGTH) {
      setErrorMessage(
        `Message exceeds the maximum allowed length of ${MAX_MESSAGE_LENGTH} characters.`
      );
      return;
    }

    if (!chats.some((chat) => chat.id === currentChatId)) {
      setErrorMessage("Invalid chat ID.");
      return;
    }

    // If all validations pass, send the message
    const userMessage = { id: Date.now(), text: newMessage, sender };
    setChatHistories((prevHistories) => ({
      ...prevHistories,
      [currentChatId]: [...prevHistories[currentChatId], userMessage],
    }));
    setNewMessage("");
    setErrorMessage(""); // Clear error message on successful send

    // Add bot response
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
    if (!chats.some((chat) => chat.id === chatId)) {
      setErrorMessage("Invalid chat selected.");
      return;
    }

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
    <main className="h-screen flex items-center justify-center">
      <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-4xl relative">
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
        <h2 className="text-xl font-bold text-center mb-4">
          {chats.find((chat) => chat.id === currentChatId)?.name || "Message"}
        </h2>
        <div className="flex space-x-6">
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
          <div className="flex-grow bg-blue-100 rounded-lg flex flex-col">
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
            <form
              onSubmit={handleSendMessage}
              className="bg-blue-300 p-4 flex flex-col relative"
            >
              <input
                type="text"
                placeholder="Type a message..."
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                className={`flex-grow border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 ${
                  errorMessage ? "border-red-500" : "border-gray-300"
                }`}
              />
              {/* Inline Error Message */}
              {errorMessage && (
                <div className="absolute top-full mt-1 text-sm text-red-500 bg-white border border-red-500 rounded p-2 shadow-lg">
                  {errorMessage}
                </div>
              )}
              <button
                type="submit"
                className="ml-4 bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 mt-4"
              >
                Send
              </button>
            </form>
          </div>
        </div>
      </div>
    </main>
  );
};

export default ChatPage;
