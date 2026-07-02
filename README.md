# AI Study Buddy

AI Study Buddy is a production-ready, interactive study platform built with **Streamlit** and the **OpenAI API**. It lets users upload study materials (PDF, DOCX, TXT) or paste notes directly to generate comprehensive AI summaries, ask context-bound questions, obtain simplified explanations with analogies, take interactive 10-question quizzes, and study with flashcards.

## Key Features

- **🏠 Home Dashboard**: View live study metrics (session duration, files uploaded, questions asked) and quickly navigate to study tools.
- **📁 Upload Notes**: Parse TXT, PDF, and DOCX files securely with size validations (up to 10 MB).
- **📝 Paste Notes**: Paste materials directly using a clean, rich text field.
- **📊 AI Summary**: Instantly create Short, Medium, and Detailed summaries alongside Key Points, Key Topics, Definitions, Timelines, and Formulas.
- **💬 Ask AI (Chatbot)**: Chat with your notes. Answers are strictly constrained to the text in your notes (returns a fallback phrase if info is missing).
- **💡 Explain Simply**: Explains complex details in a beginner-friendly way, with real-world examples, easy analogies, and key recaps.
- **📝 Quiz Generator**: Creates exactly 10 interactive Multiple-Choice Questions (MCQs) complete with interactive scoring, grading metrics, and explanations.
- **🎴 Flashcards**: Generates exactly 10 digital flashcards with standard Question Front / Answer Back flipping controls.
- **⚙️ Settings**: Control font sizing dynamically, toggle Light/Dark Mode variables, check document metadata, save API keys locally to `.env`, and reset active notes/statistics.
- **ℹ️ About**: Project background details and technological stack information.

---

## Folder Structure

```text
AI_Study_Buddy/
│
├── app.py
├── ai.py
├── utils.py
├── requirements.txt
├── README.md
├── .env.example
├── assets/
└── uploads/
```

- `app.py`: Streamlit application file containing routing, pages, custom styling, and layout logic.
- `ai.py`: OpenAI API interface using the new SDK (`openai>=1.0.0`) and structured output formats.
- `utils.py`: Contains validations, text extraction routines (using `pdfplumber` and `python-docx`), text cleaning, session configuration, and stats counters.
- `requirements.txt`: Specified package version rules.
- `.env.example`: Template configuration file for environment parameters.

---

## Installation

Ensure you have Python 3.8+ installed on your computer.

1. **Clone or copy the directory** containing the source code.
2. Navigate to the project root directory:
   ```bash
   cd AI_Study_Buddy
   ```
3. Install the dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```

---

## Environment Variable Setup

The app requires an OpenAI API key to execute AI tasks.

1. Create a file named `.env` in the root folder of the project.
2. Add your OpenAI API key to the file (refer to `.env.example`):
   ```text
   OPENAI_API_KEY=your-actual-api-key-here
   ```
3. Alternatively, you can input your key dynamically inside the **Settings** page within the application UI.

---

## Running the Application

Start the web application locally by running:

```bash
streamlit run app.py
```

The server will initialize and direct your default browser to access `http://localhost:8501`.

---

## Design and Aesthetic Theme

This application sports a high-fidelity, modern UI designed with **Blue**, **White**, and **Light Purple** styling tokens:
- **Glassmorphism Layouts**: Custom cards featuring blurred backgrounds, thin semi-transparent white borders, and soft shadows.
- **Micro-Animations**: Hover animations on buttons and cards for a premium tactile feel.
- **Fluid Layouts**: Interactive components (like the sliding font size scaler or the responsive dark-mode toggle) respond instantly.

---

## Future Enhancements

- **Offline Vector Store Integration**: Add vector indexing (e.g. ChromaDB) to handle massive textbooks (100+ pages) with advanced retrieval augmentation.
- **Multi-document Analysis**: Compare and contrast study material across different uploaded files.
- **Flashcard Export**: Support exporting cards directly to Anki-compatible CSV formats.
- **Voice Mode**: Verbalize explanations or chat directly with the AI buddy using TTS.

---

## License

This project is open-source and licensed under the MIT License.
