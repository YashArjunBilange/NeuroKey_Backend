import axios from 'axios';

const API_URL = `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/v1`;

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const NLPService = {
  detectLanguage: async (text: string) => (await api.post('/nlp/language', { text })).data,
  tokenize: async (text: string) => (await api.post('/nlp/tokenize', { text })).data,
  stem: async (text: string) => (await api.post('/nlp/stem', { text })).data,
  lemmatize: async (text: string) => (await api.post('/nlp/lemmatize', { text })).data,
  posTag: async (text: string) => (await api.post('/nlp/pos', { text })).data,
  ner: async (text: string) => (await api.post('/nlp/ner', { text })).data,
  classify: async (text: string) => (await api.post('/nlp/classify', { text })).data,
  sentiment: async (text: string) => (await api.post('/nlp/sentiment', { text })).data,
  emotion: async (text: string) => (await api.post('/nlp/emotion', { text })).data,
  vibe: async (text: string) => (await api.post('/nlp/vibe', { text })).data,
  emoji: async (text: string) => (await api.post('/nlp/emoji', { text })).data,
  gif: async (text: string) => (await api.post('/nlp/gif', { text })).data,
  improve: async (text: string, style: string = 'Professional') => (await api.post('/nlp/improve', { text, style })).data,
};

export const PredictionService = {
  nextWord: async (text: string, top_k: number = 3) => (await api.post('/predict/next-word', { text, top_k })).data,
  nextSentence: async (context: string, top_k: number = 3) => (await api.post('/predict/next-sentence', { context, top_k })).data,
};

export const ScrapingService = {
  scrape: async (url: string) => (await api.post('/scrape', { url })).data,
};

export const AnalysisService = {
  dataset: async () => (await api.get('/analysis/dataset/analysis')).data,
};
