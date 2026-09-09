import { useState } from 'react';
import { NLPService, PredictionService } from '../services/api';
import { Sparkles, Smile, Image as ImageIcon, Mic, Send } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function KeyboardDemo() {
  const [context, setContext] = useState([
    { role: 'friend', text: 'Are you coming to college tomorrow?' }
  ]);
  const [input, setInput] = useState('');
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [vibe, setVibe] = useState('Neutral');
  const [emojis, setEmojis] = useState<string[]>([]);
  const [improved, setImproved] = useState<string | null>(null);

  const handleInputChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    setInput(val);
    
    if (val.trim().length > 2) {
      try {
        const nextWords = await PredictionService.nextWord(val);
        setSuggestions(nextWords.predictions.map((p: any) => p.word));
        
        // Background analysis
        NLPService.vibe(val).then(res => setVibe(res.vibe));
        NLPService.emoji(val).then(res => setEmojis(res.emojis));
      } catch (err) {
        console.error(err);
      }
    } else {
      setSuggestions([]);
      setVibe('Neutral');
      setEmojis([]);
    }
  };

  const handleSuggestClick = (word: string) => {
    setInput(prev => prev.endsWith(' ') ? prev + word : prev + ' ' + word);
    setSuggestions([]);
  };

  const handleSend = () => {
    if (!input.trim()) return;
    setContext([...context, { role: 'user', text: input }]);
    setInput('');
    setSuggestions([]);
    setVibe('Neutral');
    setEmojis([]);
    setImproved(null);
  };

  const handleImprove = async () => {
    if (!input.trim()) return;
    setLoading(true);
    try {
      const res = await NLPService.improve(input, 'Professional');
      setImproved(res.improved);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto h-[calc(100vh-8rem)] flex flex-col">
      <header className="mb-6">
        <h1 className="text-3xl font-bold tracking-tight">Smart Keyboard Demo</h1>
        <p className="text-gray-500 mt-2">Interactive demonstration of Next-Word Prediction, Emotion Detection, and AI Chat Improvement.</p>
      </header>

      <div className="flex-1 bg-white dark:bg-gray-900 rounded-3xl shadow-xl border border-gray-200 dark:border-gray-800 flex flex-col overflow-hidden relative">
        
        {/* Chat Area */}
        <div className="flex-1 p-6 overflow-y-auto space-y-4 bg-gray-50 dark:bg-gray-950/50">
          {context.map((msg, idx) => (
            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[70%] rounded-2xl px-5 py-3 ${
                msg.role === 'user' 
                  ? 'bg-primary text-white rounded-br-none' 
                  : 'bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200 rounded-bl-none shadow-sm border border-gray-100 dark:border-gray-700'
              }`}>
                {msg.text}
              </div>
            </div>
          ))}
        </div>

        {/* NLP Info Panel */}
        <div className="px-6 py-3 bg-white dark:bg-gray-900 border-t border-gray-100 dark:border-gray-800 flex items-center justify-between text-sm">
          <div className="flex gap-4">
            <span className="flex items-center gap-1 text-gray-500">
              <span className="w-2 h-2 rounded-full bg-blue-500"></span> Vibe: <strong className="text-gray-700 dark:text-gray-300">{vibe}</strong>
            </span>
          </div>
          {emojis.length > 0 && (
            <div className="flex gap-2">
              {emojis.map((emoji, i) => (
                <button key={i} onClick={() => setInput(prev => prev + emoji)} className="hover:scale-125 transition-transform text-lg">{emoji}</button>
              ))}
            </div>
          )}
        </div>

        {/* Keyboard Area */}
        <div className="p-4 bg-gray-100 dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800">
          
          {/* Suggestions */}
          <div className="flex gap-2 mb-4 h-10">
            <AnimatePresence>
              {suggestions.map((word, i) => (
                <motion.button
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  key={`${word}-${i}`}
                  onClick={() => handleSuggestClick(word)}
                  className="px-4 py-2 bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 text-sm font-medium hover:bg-gray-50 dark:hover:bg-gray-700 flex-1 whitespace-nowrap overflow-hidden text-ellipsis"
                >
                  {word}
                </motion.button>
              ))}
            </AnimatePresence>
          </div>

          {/* AI Toolbar */}
          <div className="flex gap-2 mb-3">
            <button onClick={handleImprove} disabled={loading || !input} className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 text-xs font-medium hover:bg-blue-100 disabled:opacity-50 transition-colors">
              <Sparkles size={14} /> Improve
            </button>
            <button onClick={async () => {
              if (input) {
                const res = await NLPService.emoji(input);
                if (res.emojis?.length) setInput(prev => prev + res.emojis[0]);
              } else {
                setInput(prev => prev + "😊");
              }
            }} className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-gray-200 dark:bg-gray-800 text-gray-600 dark:text-gray-400 text-xs font-medium hover:bg-gray-300 transition-colors">
              <Smile size={14} /> Emoji
            </button>
            <button onClick={async () => {
              if (input) {
                const res = await NLPService.gif(input);
                setContext([...context, { role: 'user', text: `[GIF Request: ${res.query}]` }]);
                setInput('');
              } else {
                setContext([...context, { role: 'user', text: `[GIF Request: hello]` }]);
              }
            }} className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-gray-200 dark:bg-gray-800 text-gray-600 dark:text-gray-400 text-xs font-medium hover:bg-gray-300 transition-colors">
              <ImageIcon size={14} /> GIF
            </button>
            <button onClick={() => {
              setInput(prev => prev + " (🎙️ Listening...)");
              setTimeout(() => {
                setInput(prev => prev.replace(" (🎙️ Listening...)", " Yeah, I'm using Voice Input now!"));
              }, 2000);
            }} className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-gray-200 dark:bg-gray-800 text-gray-600 dark:text-gray-400 text-xs font-medium hover:bg-gray-300 transition-colors ml-auto">
              <Mic size={14} /> Voice
            </button>
          </div>

          {/* Input Box */}
          <div className="relative">
            {improved && (
              <div className="absolute bottom-full mb-2 left-0 right-0 p-3 bg-blue-600 text-white rounded-xl text-sm shadow-lg z-10 flex justify-between items-center">
                <span>{improved}</span>
                <div className="flex gap-2">
                  <button onClick={() => { setInput(improved); setImproved(null); }} className="px-2 py-1 bg-white/20 hover:bg-white/30 rounded">Accept</button>
                  <button onClick={() => setImproved(null)} className="px-2 py-1 hover:bg-white/10 rounded">Discard</button>
                </div>
              </div>
            )}
            <div className="flex gap-2">
              <input 
                type="text" 
                value={input}
                onChange={handleInputChange}
                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Type a message..."
                className="flex-1 px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-primary shadow-inner"
              />
              <button 
                onClick={handleSend}
                disabled={!input.trim()}
                className="p-3 bg-primary text-white rounded-xl hover:bg-emerald-600 disabled:opacity-50 disabled:hover:bg-primary transition-colors flex items-center justify-center shadow-sm"
              >
                <Send size={20} />
              </button>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
