import { useState } from 'react';
import { NLPService } from '../services/api';
import { Activity } from 'lucide-react';

export default function Analyzer() {
  const [input, setInput] = useState('NeuroKey is an incredibly fast and powerful NLP keyboard. I love using it!');
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!input.trim()) return;
    setLoading(true);
    try {
      const [lang, tokens, pos, sentiment, emotion, entities] = await Promise.all([
        NLPService.detectLanguage(input),
        NLPService.tokenize(input),
        NLPService.posTag(input),
        NLPService.sentiment(input),
        NLPService.emotion(input),
        NLPService.ner(input)
      ]);

      setResults({ lang, tokens, pos, sentiment, emotion, entities });
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8 animation-fade-in">
      <header>
        <h1 className="text-3xl font-bold tracking-tight">NLP Analyzer</h1>
        <p className="text-gray-500 mt-2">Deep dive into the Natural Language Processing algorithms powering NeuroKey.</p>
      </header>

      <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Input Text</label>
        <textarea 
          value={input}
          onChange={e => setInput(e.target.value)}
          className="w-full h-32 p-4 rounded-xl border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 focus:ring-2 focus:ring-blue-500 focus:outline-none resize-none"
          placeholder="Enter text to analyze..."
        />
        <div className="mt-4 flex justify-end">
          <button 
            onClick={handleAnalyze}
            disabled={loading || !input.trim()}
            className="flex items-center gap-2 px-6 py-2.5 bg-blue-600 text-white font-medium rounded-xl hover:bg-blue-700 disabled:opacity-50 transition-colors"
          >
            {loading ? <span className="animate-pulse">Analyzing...</span> : <><Activity size={18} /> Analyze Text</>}
          </button>
        </div>
      </div>

      {results && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Sentiment & Emotion */}
          <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
            <h3 className="text-lg font-bold mb-4">Sentiment & Emotion</h3>
            <div className="space-y-4">
              <div>
                <p className="text-sm text-gray-500">Language</p>
                <p className="text-xl font-semibold uppercase">{results.lang.language} <span className="text-sm font-normal text-gray-400">({(results.lang.confidence * 100).toFixed(0)}%)</span></p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Sentiment</p>
                <p className={`text-xl font-semibold ${results.sentiment.label === 'Positive' ? 'text-green-500' : results.sentiment.label === 'Negative' ? 'text-red-500' : 'text-gray-500'}`}>
                  {results.sentiment.label}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Emotion</p>
                <p className="text-xl font-semibold text-purple-500">{results.emotion.emotion}</p>
              </div>
            </div>
          </div>

          {/* Tokens */}
          <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 lg:col-span-2">
            <h3 className="text-lg font-bold mb-4">Tokens & POS Tagging</h3>
            <div className="flex flex-wrap gap-2">
              {results.pos.tagged_tokens?.map((tag: any, i: number) => (
                <div key={i} className="px-3 py-1 bg-gray-100 dark:bg-gray-900 rounded-lg text-sm border border-gray-200 dark:border-gray-700 flex flex-col items-center">
                  <span className="font-medium text-gray-900 dark:text-gray-100">{tag[0]}</span>
                  <span className="text-xs text-blue-500">{tag[1]}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Named Entities */}
          <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 lg:col-span-3">
            <h3 className="text-lg font-bold mb-4">Named Entity Recognition (NER)</h3>
            {results.entities.entities?.length > 0 ? (
               <div className="flex flex-wrap gap-3">
                 {results.entities.entities.map((ent: any, i: number) => (
                   <div key={i} className="px-4 py-2 bg-purple-50 dark:bg-purple-900/20 text-purple-700 dark:text-purple-300 rounded-xl border border-purple-200 dark:border-purple-800">
                     <span className="font-bold mr-2">{ent.text}</span>
                     <span className="text-xs uppercase tracking-wider opacity-80">{ent.label}</span>
                   </div>
                 ))}
               </div>
            ) : (
              <p className="text-gray-500 italic">No named entities detected.</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
