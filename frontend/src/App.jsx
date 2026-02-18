import { useState } from "react";
import axios from "axios";

function App() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);

  const checkUrl = async () => {
    if (!url) {
      alert("Please enter a URL");
      return;
    }

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/check-url",
        { url }
      );
      setResult(response.data);
    } catch (error) {
      alert("Make sure backend is running!");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-800 text-white flex flex-col items-center justify-center">
      <h1 className="text-4xl font-bold mb-8 text-blue-400">
        AI Phishing Detection System
      </h1>

      <div className="bg-gray-800 p-8 rounded-xl shadow-xl">
        <input
          type="text"
          placeholder="Enter website URL..."
          className="w-96 p-3 rounded text-black"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />

        <button
          onClick={checkUrl}
          className="w-full mt-4 bg-blue-600 p-3 rounded hover:bg-blue-700 transition"
        >
          Check Website
        </button>

        {result && (
          <div className="mt-6 w-full">
            <p className="text-lg text-center mb-2">
              Phishing Probability: {result.phishing_probability}%
            </p>

            {/* Risk Bar */}
            <div className="w-full bg-gray-700 rounded-full h-6 overflow-hidden">
              <div
                className={`h-6 transition-all duration-700 ${
                  result.phishing_probability < 30
                    ? "bg-green-500"
                    : result.phishing_probability < 70
                    ? "bg-yellow-500"
                    : "bg-red-500"
                }`}
                style={{ width: `${result.phishing_probability}%` }}
              ></div>
            </div>

            <p className="text-xl font-bold text-center mt-4">
              Verdict:
              <span
                className={
                  result.verdict === "Safe"
                    ? "text-green-400 ml-2"
                    : "text-red-400 ml-2"
                }
              >
                {result.verdict}
              </span>
            </p>
          </div>
        )}


      </div>
    </div>
  );
}

export default App;
