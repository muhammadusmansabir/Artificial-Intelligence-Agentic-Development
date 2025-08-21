"use client";

import { useState } from "react";

export default function Home() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");

  const sendMessage = async () => {
    if (!message) return;
    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });
      const data = await res.json();
      setResponse(data.response);
    } catch (error) {
      console.error(error);
      setResponse("Error connecting to backend.");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-8 bg-gray-50">
      <h1 className="text-2xl font-bold mb-6">🍏 Health AI Chatbot</h1>

      <div className="w-full max-w-lg flex flex-col gap-4">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your health question (e.g., suggest a diet for 25 y/o, BMI 27)..."
          className="border rounded-lg p-3 w-full"
          rows={4}
        />

        <button
          onClick={sendMessage}
          className="bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition"
        >
          Send
        </button>

        {response && (
          <div className="mt-4 p-4 border rounded-lg bg-white shadow">
            <strong>AI Response:</strong>
            <p className="mt-2 text-gray-700 whitespace-pre-line">{response}</p>
          </div>
        )}
      </div>
    </div>
  );
}
