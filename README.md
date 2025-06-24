# 💬 Astra Chat – Smart Banking Assistant

Astra Chat is a sleek and responsive chatbot interface built with React and Tailwind CSS. It connects to a backend API (e.g., FastAPI, Flask) for intelligent banking conversations. Designed to be embedded in a customer-facing web portal, Astra provides users with friendly and helpful banking assistance.

---

## 🚀 Features

* Real-time user and bot messaging
* Scroll-to-latest chat
* Responsive, modern UI with Tailwind
* Graceful error handling
* Loading state for better UX
* Keyboard-friendly interaction (hit `Enter` to send)
* Animated message transitions

---

## 📦 Installation & Setup

### 1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/chatbot
cd chatbot
```

### 2. **Install Dependencies**

Ensure you have Node.js and npm installed.

```bash
npm install
```

### 3. **Start the Frontend**

```bash
npm run dev
```

This will open the React app (typically at `http://localhost:3000`).

---

## 🔌 Backend Connection

The frontend sends messages to a backend endpoint at:

```
http://localhost:8000/chat
```

### 🔧 To use it:

* Make sure your backend server (e.g., FastAPI/Flask) is running on port `8000`
* It should accept POST requests at `/chat` and return a response like:

```json
{
  "response": "Your smart banking response here."
}
```

---

## 💬 How to Use

1. Open the application in your browser: `http://localhost:3000`
2. You'll be greeted by Astra with a welcome message.
3. Type your banking-related query in the input box (e.g., “What’s my account balance?”).
4. Hit `Enter` or click `Send`.
5. Astra will respond with helpful information.
6. Continue the conversation freely.

---

## 🛑 How to Stop or Close the App

### ⛔ Frontend

To stop the frontend server:

```bash
CTRL + C
```

from your terminal.

### ⛔ Backend

If you're running a local server on port 8000, also stop that process:

```bash
CTRL + C
```

---

## 🧠 Tips

* You can modify the backend URL in the `fetch` call if deploying to another server.
* Make sure CORS is properly configured on the backend if you deploy separately.
* Style and animation can be customized with Tailwind and CSS-in-JS.

---

## 📁 Project Structure

```
astra-chat/
├── pages/
│   └── index.tsx       # Main Chat UI
├── public/
├── styles/
├── package.json
└── README.md
```

---

## 📌 TODO

* Add authentication for secure access
* Store chat history
* Integrate with NLP models (OpenAI, TensorFlow, Rasa, etc.)
* Voice input/output

---

## 📃 License

MIT License. Feel free to fork and adapt this project!

---
