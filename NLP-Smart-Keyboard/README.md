# NLP Smart Keyboard 🧠⌨️

A comprehensive NLP-powered Smart Keyboard Android application with a React-based Web Demonstration Application, powered by a FastAPI Python backend.

## Project Overview
This project serves two purposes:
1. **A real-world AI Android Smart Keyboard** that suggests words, emotions, and emojis based on conversation context.
2. **A college-level NLP demonstration** web app that showcases 25 fundamental Natural Language Processing algorithms.

## NLP Concepts Implemented
1. Web Scraping
2. Dataset Loading (HuffPost News)
3. Language Detection (English, Hindi, Hinglish)
4. Word & Sentence Tokenization
5. Porter Stemming
6. WordNet Lemmatization
7. POS Tagging
8. Word Embeddings (`all-MiniLM-L6-v2`)
9. Text Classification (VADER Sentiment)
10. Named Entity Recognition (NER)
11. TF-IDF
12. N-Gram Modeling (Unigram, Bigram, Trigram)
13. Sequence Probability Calculation
14. Next-Word Prediction
15. Next-Sentence Prediction
16. Conversation Memory
17. Sentiment Analysis
18. Emotion Detection
19. Opinion/Vibe Mining
20. Topic Modeling (LDA)
21. Emoji Recommendation
22. GIF Query Recommendation
23. Chat Improvement Styles
24. Voice Input (Android)
25. Full Unified NLP Pipeline

## Architecture & Technology Stack
- **Backend:** Python, FastAPI, Uvicorn, NLTK, spaCy, scikit-learn, sentence-transformers, SQLite
- **Frontend:** React, Vite, TypeScript, Tailwind CSS, Framer Motion
- **Android:** Kotlin, Android SDK (InputMethodService), Coroutines, Retrofit

## Folder Structure
```text
NLP-Smart-Keyboard/
├── android/        (Native Kotlin Android Keyboard app)
├── backend/        (Python FastAPI application)
├── frontend/       (React Web Application)
├── data/           (Dataset storage)
└── README.md
```

## Installation & Setup

### 1. Python Backend
```bash
cd backend
python -m venv .venv
# Activate the virtual environment:
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate

pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn app.main:app --reload
```
The backend will run on `http://localhost:8000`.

### 2. React Frontend
```bash
cd frontend
npm install
npm run dev
```
The frontend will run on `http://localhost:5173`.

### 3. Android Setup & Build
1. Ensure you have the Android SDK installed.
2. Open the `android` folder in Android Studio.
3. Allow Gradle to sync.
4. Run the build:
```bash
cd android
gradlew.bat assembleDebug
```
The APK will be generated at `android/app/build/outputs/apk/debug/app-debug.apk`.

### How to Install the Android APK
1. Copy the APK to your Android device or emulator.
2. Install the APK.
3. Go to **Settings -> System -> Languages & Input -> On-screen keyboard -> Manage on-screen keyboards**.
4. Enable **NeuroKey Smart Keyboard**.
5. When typing in any text field, switch your keyboard to NeuroKey.

## Privacy & Security
The keyboard automatically detects sensitive input fields (like passwords, PINs) and disables network transmission and AI suggestions to protect user privacy.

## Known Limitations
- The `sentence-transformers` model downloads the first time you run an embedding task.
- GIF support requires a valid Giphy/Tenor API Key placed in `backend/app/config.py`.
- N-Gram prediction uses a lightweight training set; for better predictions, load a larger corpus.
- The Android UI is currently a simplified QWERTY visualization and requires a full KeyMap integration for production sizing.

## License
MIT License
