import React, { useState } from "react";

const ChatPage = () => {
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello!", sender: "me" },
    { id: 2, text: "What's up!", sender: "them" },
  ]);
  const [newMessage, setNewMessage] = useState("");

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    setMessages((prevMessages) => [
      ...prevMessages,
      { id: prevMessages.length + 1, text: newMessage, sender: "me" },
    ]);
    setNewMessage("");
  };

  return (
    <>
      <main className="h-screen flex items-center justify-center">
        <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-2xl">
          {/* Header */}
          <h2 className="text-xl font-bold text-center mb-4">
            Message 
          </h2>

          {/* Main Content */}
          <div className="flex space-x-6">
            {/* Left Section: Recent Chats */}
            <div className="space-y-4 w-1/3">
              <div>
                <h3 className="text-lg font-bold text-center">Recent Chats</h3>
                <div className="bg-blue-100 rounded-lg p-2 space-y-2">
                  {Array.from({ length: 6 }, (_, i) => (
                    <p
                      key={i}
                      className="bg-blue-200 p-2 rounded-lg text-center hover:bg-blue-300 cursor-pointer"
                    >
                      Chat {i + 1}
                    </p>
                  ))}
                </div>
              </div>
            </div>

            {/* Right Section: Chat Box */}
            <div className="flex-grow bg-blue-100 rounded-lg flex flex-col">
              {/* Chat Messages */}
              <div className="flex-grow p-4 overflow-y-auto">
                {messages.map((msg) => (
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
