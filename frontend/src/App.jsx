import React from "react";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Sparkles, Brain, BookOpenText, MessageCircle } from "lucide-react";

export default function FakeNewsDetector() {
  const [claim, setClaim] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    const response = await fetch("http://127.0.0.1:5000/api/check", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ claim }),
    });
    const data = await response.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-[#050505] text-gray-100 flex flex-col items-center justify-center px-6 py-12 font-[Inter]">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="text-center mb-12"
      >
        <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-gray-100 to-gray-400 tracking-tight uppercase flex items-center justify-center gap-3">
          <Sparkles className="text-gray-300" size={34} /> Fake News Detector
        </h1>
        <p className="text-gray-500 mt-2 text-md tracking-wide">
          Fast, reliable and AI-powered news verification.
        </p>
      </motion.div>

      <motion.form
        onSubmit={handleSubmit}
        className="w-full max-w-2xl bg-[#0b0b0b] rounded-xl shadow-[0_0_30px_rgba(255,255,255,0.05)] border border-gray-800 p-8 flex flex-col gap-6"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.4 }}
      >
        <textarea
          value={claim}
          onChange={(e) => setClaim(e.target.value)}
          placeholder="Type or paste a claim to verify..."
          className="w-full h-40 text-md p-4 rounded-md bg-[#0f0f0f] border border-gray-700 focus:outline-none focus:ring-1 focus:ring-gray-400 text-gray-200 resize-none placeholder-gray-600 tracking-wide leading-relaxed"
        />
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          disabled={loading}
          className="w-full py-3 rounded-md text-lg font-semibold tracking-wide text-gray-900 bg-gray-100 hover:bg-gray-300 transition-all duration-300 shadow-md disabled:opacity-60 disabled:cursor-not-allowed"
        >
          {loading ? "Analyzing..." : "Check Authenticity"}
        </motion.button>
      </motion.form>

      <AnimatePresence>
        {result && (
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            transition={{ duration: 0.5 }}
            className="mt-10 w-full max-w-2xl bg-[#0b0b0b] border border-gray-800 rounded-xl p-8 shadow-[0_0_30px_rgba(255,255,255,0.05)]"
          >
            <div className="mb-5">
              <h2 className="text-xl font-bold flex items-center gap-2 text-gray-200 uppercase tracking-wider">
                <Brain className="text-gray-400" size={22} /> Verdict
              </h2>
              <span
                className={`inline-block mt-2 text-lg font-semibold px-3 py-1 border rounded-sm ${
                  result.verdict === "True"
                    ? "border-green-500 text-green-400"
                    : result.verdict === "False"
                    ? "border-red-500 text-red-400"
                    : "border-yellow-500 text-yellow-400"
                }`}
              >
                {result.verdict}
              </span>
            </div>

            <div className="mt-6">
              <h3 className="flex items-center gap-2 text-gray-300 font-semibold mb-2 uppercase tracking-wider">
                <BookOpenText className="text-gray-400" size={20} /> Verified Facts Used
              </h3>
              <ul className="list-disc list-inside text-gray-400 ml-4 text-sm leading-relaxed space-y-1">
                {result.facts.map((fact, i) => (
                  <li key={i}>{fact}</li>
                ))}
              </ul>
            </div>

            <div className="mt-6">
              <h3 className="flex items-center gap-2 text-gray-300 font-semibold mb-2 uppercase tracking-wider">
                <MessageCircle className="text-gray-400" size={20} /> Reasoning
              </h3>
              <p className="text-gray-400 text-sm leading-relaxed bg-[#0f0f0f] p-4 rounded-md border border-gray-800">
                {result.reasoning}
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <footer className="mt-16 text-gray-600 text-xs tracking-wide uppercase">
        ⚡ Built with <span className="text-gray-300 font-medium">RAG</span> + <span className="text-gray-400 font-medium">GPT</span>
      </footer>
    </div>
  );
}
