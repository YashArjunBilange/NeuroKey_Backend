import { Activity, Brain, Database, Keyboard, MessageSquare, Zap } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Dashboard() {
  const stats = [
    { name: 'NLP Modules Loaded', value: '25', icon: <Brain className="text-blue-500" /> },
    { name: 'Supported Languages', value: '3', icon: <MessageSquare className="text-green-500" /> },
    { name: 'Dataset Articles', value: 'Bring your dataset', icon: <Database className="text-purple-500" /> },
    { name: 'Backend status', value: 'On demand', icon: <Zap className="text-yellow-500" /> },
  ];

  return (
    <div className="max-w-6xl mx-auto space-y-8 animation-fade-in">
      <header>
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-gray-500 dark:text-gray-400 mt-2">Welcome to the NeuroKey NLP Demonstration Platform.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, i) => (
          <div key={i} className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 flex items-center gap-4 hover:shadow-md transition-shadow">
            <div className="p-4 bg-gray-50 dark:bg-gray-900 rounded-xl">
              {stat.icon}
            </div>
            <div>
              <p className="text-sm font-medium text-gray-500 dark:text-gray-400">{stat.name}</p>
              <h3 className="text-2xl font-bold">{stat.value}</h3>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8">
        <div className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 rounded-lg">
              <Keyboard />
            </div>
            <h2 className="text-xl font-bold">Smart Keyboard Demo</h2>
          </div>
          <p className="text-gray-600 dark:text-gray-300 mb-6">
            Experience the real-world application of our NLP pipeline. This interactive demo showcases next-word prediction, emotion detection, and AI chat improvements in real-time.
          </p>
          <Link to="/demo" className="inline-flex items-center justify-center px-6 py-3 bg-primary text-white font-medium rounded-xl hover:bg-emerald-600 transition-colors shadow-sm hover:shadow-md">
            Launch Demo
          </Link>
        </div>

        <div className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-blue-100 dark:bg-blue-900/30 text-blue-600 rounded-lg">
              <Activity />
            </div>
            <h2 className="text-xl font-bold">NLP Analyzer</h2>
          </div>
          <p className="text-gray-600 dark:text-gray-300 mb-6">
            Dive deep into the algorithms. Analyze text using tokenization, stemming, lemmatization, POS tagging, NER, TF-IDF, and more.
          </p>
          <Link to="/analyzer" className="inline-flex items-center justify-center px-6 py-3 bg-blue-600 text-white font-medium rounded-xl hover:bg-blue-700 transition-colors shadow-sm hover:shadow-md">
            Open Analyzer
          </Link>
        </div>
      </div>
    </div>
  );
}
