import { useState } from 'react';
import { Database, Download, Loader2, Search } from 'lucide-react';
import { ScrapingService } from '../services/api';

type ScrapeResult = {
  title: string;
  extracted_text: string;
  word_count: number;
  sentence_count: number;
  language: string;
  sentiment: string;
  url: string;
};

export default function DatasetScraper() {
  const [url, setUrl] = useState('https://en.wikipedia.org/wiki/Natural_language_processing');
  const [result, setResult] = useState<ScrapeResult | null>(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const scrape = async () => {
    if (!url.trim()) return;
    setLoading(true);
    setError('');
    try {
      setResult(await ScrapingService.scrape(url));
    } catch (requestError: any) {
      setResult(null);
      setError(requestError?.response?.data?.detail || 'The page could not be analyzed. Check the URL and try again.');
    } finally {
      setLoading(false);
    }
  };

  const downloadText = () => {
    if (!result) return;
    const blob = new Blob([result.extracted_text], { type: 'text/plain;charset=utf-8' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'neurokey-extracted-text.txt';
    link.click();
    URL.revokeObjectURL(link.href);
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8 animation-fade-in">
      <header>
        <div className="flex items-center gap-3">
          <div className="p-3 rounded-xl bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300"><Database /></div>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Dataset & Web Scraper</h1>
            <p className="text-gray-500 dark:text-gray-400 mt-1">Extract a public page, clean its text, and run the NLP pipeline.</p>
          </div>
        </div>
      </header>

      <section className="bg-white dark:bg-gray-800 p-6 rounded-2xl border border-gray-200 dark:border-gray-700 shadow-sm">
        <label htmlFor="scrape-url" className="block text-sm font-semibold mb-2">Public URL</label>
        <div className="flex flex-col sm:flex-row gap-3">
          <input id="scrape-url" value={url} onChange={(event) => setUrl(event.target.value)} onKeyDown={(event) => event.key === 'Enter' && scrape()} className="flex-1 px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-emerald-500" placeholder="https://example.com/article" />
          <button onClick={scrape} disabled={loading || !url.trim()} className="inline-flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-emerald-600 text-white font-semibold disabled:opacity-50 hover:bg-emerald-700">
            {loading ? <Loader2 size={18} className="animate-spin" /> : <Search size={18} />} Analyze page
          </button>
        </div>
        {error && <p className="mt-3 text-sm text-red-600 dark:text-red-400">{error}</p>}
      </section>

      {result && <section className="space-y-5">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
          <div><p className="text-sm text-gray-500">Page title</p><h2 className="text-2xl font-bold">{result.title}</h2></div>
          <button onClick={downloadText} className="inline-flex items-center justify-center gap-2 px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-800"><Download size={16} /> Download text</button>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
          {[["Words", result.word_count], ["Sentences", result.sentence_count], ["Language", result.language.toUpperCase()], ["Sentiment", result.sentiment], ["Source", "Public page"]].map(([label, value]) => <div key={String(label)} className="p-4 rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700"><p className="text-xs text-gray-500">{label}</p><p className="mt-1 font-bold truncate">{value}</p></div>)}
        </div>
        <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl border border-gray-200 dark:border-gray-700"><h3 className="font-bold mb-3">Extracted text</h3><p className="whitespace-pre-wrap text-sm leading-6 text-gray-700 dark:text-gray-300 max-h-96 overflow-y-auto">{result.extracted_text}</p></div>
      </section>}
    </div>
  );
}
