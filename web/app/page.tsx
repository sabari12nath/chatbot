"use client";

import React, { useCallback, useEffect, useRef, useState } from "react";

export default function Page() {
  const [messages, setMessages] = useState<{ from: string; text: string }[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    setMessages([
      {
        from: "bot",
        text: "Hello! I'm Astra, your personal banking assistant. How can I help you today?",
      },
    ]);
  }, []);

  const sendMessage = useCallback(async () => {
    if (!input.trim()) return;

    setMessages((prev) => [...prev, { from: "user", text: input }]);
    setLoading(true);
    setError("");

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      if (!res.ok) throw new Error("Network error");

      const data = await res.json();
      setMessages((prev) => [...prev, { from: "bot", text: data.response }]);
    } catch (err) {
      setError("Failed to connect to ASTRA support. Please try again.");
    }

    setInput("");
    setLoading(false);
  }, [input]);

  return (
    <main className="min-h-screen min-w-screen flex flex-col items-center justify-center bg-gradient-to-br from-[#232526] via-[#414345] to-[#6a11cb] relative overflow-hidden">
      {/* ChatGPT-like centered chat container */}
      <div className="flex flex-col w-full max-w-2xl min-h-[70vh] max-h-[90vh] bg-[#18181b] shadow-2xl rounded-3xl border border-[#33354a] m-4 z-10 backdrop-blur-xl overflow-hidden">
        {/* Header */}
        <header className="bg-[#232526] text-white px-6 py-5 text-center shadow rounded-t-3xl flex flex-col items-center border-b border-[#33354a]">
          <div className="flex items-center justify-center gap-3 mb-1">
            <span className="bg-gradient-to-br from-[#6a11cb] to-[#2575fc] text-white rounded-full w-14 h-14 flex items-center justify-center font-extrabold text-3xl shadow-xl border-2 border-[#33354a]">💬</span>
            <span className="text-2xl font-bold drop-shadow-lg tracking-wide font-mono bg-gradient-to-r from-[#6a11cb] to-[#2575fc] bg-clip-text text-transparent">Astra Chat</span>
          </div>
          <p className="text-xs opacity-80 mt-1 font-light tracking-wide">Your Smart Banking Assistant</p>
        </header>

        {/* Chat Display */}
        <div className="flex-1 flex flex-col px-6 py-6 space-y-4 bg-[#18181b] text-base overflow-auto scrollbar-thin scrollbar-thumb-[#33354a] scrollbar-track-transparent">
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full opacity-80">
              <span className="text-6xl mb-2 animate-bounce">💬</span>
              <span className="text-lg text-[#6a11cb] font-semibold font-mono">Start a conversation with Astra!</span>
            </div>
          )}
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.from === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`px-5 py-3 rounded-2xl shadow transition-all duration-300 max-w-[80%] break-words ${
                  msg.from === "user"
                    ? "bg-gradient-to-r from-[#232526] to-[#33354a] text-white self-end border border-[#33354a]"
                    : "bg-gradient-to-r from-[#232526] to-[#6a11cb] text-white self-start border border-[#6a11cb]"
                }`}
                style={{
                  animation: "fadeInUp 0.4s cubic-bezier(.23,1.01,.32,1) both"
                }}
              >
                {/* Render bot messages as HTML, user as plain text */}
                {msg.from === "bot" ? (
                  <span dangerouslySetInnerHTML={{ __html: msg.text }} />
                ) : (
                  <span>{msg.text}</span>
                )}
              </div>
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>

        {/* Error if any */}
        {error && (
          <div className="text-xs text-red-600 px-6 py-2 bg-red-100 rounded-b-lg">{error}</div>
        )}

        {/* Input Box */}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            sendMessage();
          }}
          className="flex gap-3 px-6 py-5 border-t border-[#33354a] bg-[#232526] rounded-b-3xl"
        >
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 p-3 border border-[#33354a] rounded-xl focus:ring focus:ring-[#6a11cb] text-base shadow-sm bg-[#232526] text-white placeholder-gray-400"
            disabled={loading}
            autoFocus
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-gradient-to-r from-[#6a11cb] to-[#2575fc] px-6 py-2 text-white font-semibold rounded-xl hover:from-[#2575fc] hover:to-[#6a11cb] text-base shadow-lg transition-all duration-200"
          >
            {loading ? <span className="animate-spin">⏳</span> : "Send"}
          </button>
        </form>
        <style>{`
          @keyframes fadeInUp {
            0% { opacity: 0; transform: translateY(30px); }
            100% { opacity: 1; transform: translateY(0); }
          }
        `}</style>
      </div>
    </main>
  );
}
