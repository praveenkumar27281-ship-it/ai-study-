import os
import time
import streamlit as st
import utils
import ai

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
utils.init_session_state()

# ----------------------------------------------------
# Inject Custom CSS Theme
# ----------------------------------------------------
theme = st.session_state.settings["theme"]
font_size = st.session_state.settings["font_size"]

if theme == "dark":
    css_vars = """
    :root {
        --primary: #818cf8;
        --primary-gradient: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        --bg-gradient: linear-gradient(135deg, #090d16 0%, #111827 100%);
        --card-bg: rgba(17, 24, 39, 0.7);
        --card-border: rgba(255, 255, 255, 0.08);
        --card-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        --text-primary: #f3f4f6;
        --text-secondary: #9ca3af;
    }
    """
else:
    css_vars = """
    :root {
        --primary: #4f46e5;
        --primary-gradient: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        --bg-gradient: linear-gradient(135deg, #eff6ff 0%, #f5f3ff 100%);
        --card-bg: rgba(255, 255, 255, 0.75);
        --card-border: rgba(255, 255, 255, 0.45);
        --card-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.06);
        --text-primary: #0f172a;
        --text-secondary: #475569;
    }
    """

custom_css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

{css_vars}

/* App wide typography setup */
html, body, [class*="css"], .stApp, p, li, button, input, label, textarea {{
    font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif !important;
    font-size: {font_size}px !important;
}}

h1 {{ font-size: {font_size + 18}px !important; font-weight: 700 !important; color: var(--text-primary) !important; }}
h2 {{ font-size: {font_size + 12}px !important; font-weight: 600 !important; color: var(--text-primary) !important; }}
h3 {{ font-size: {font_size + 6}px !important; font-weight: 600 !important; color: var(--text-primary) !important; }}
h4 {{ font-size: {font_size + 2}px !important; font-weight: 500 !important; color: var(--text-primary) !important; }}

/* Streamlit style override */
.stApp {{
    background: var(--bg-gradient) !important;
    background-attachment: fixed !important;
}}

/* Hide standard components */
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
header {{visibility: hidden;}}

/* Custom glassmorphism card styling */
.glass-card {{
    background: var(--card-bg) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border-radius: 16px !important;
    border: 1px solid var(--card-border) !important;
    box-shadow: var(--card-shadow) !important;
    padding: 24px !important;
    margin-bottom: 20px !important;
    transition: all 0.3s ease-in-out !important;
    color: var(--text-primary) !important;
}}

.glass-card:hover {{
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.12) !important;
}}

/* Custom styling for metrics */
.kpi-container {{
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
    gap: 15px;
    margin-bottom: 24px;
}}

.kpi-card {{
    flex: 1;
    min-width: 140px;
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    box-shadow: var(--card-shadow);
    padding: 16px;
    border-radius: 12px;
    text-align: center;
}}

.kpi-value {{
    font-size: 24px;
    font-weight: 700;
    color: var(--primary);
}}

.kpi-label {{
    font-size: 12px;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 600;
}}

/* Scrollable container for text */
.scroll-container {{
    max-height: 350px;
    overflow-y: auto;
    background: rgba(0, 0, 0, 0.03);
    border-radius: 12px;
    padding: 16px;
    border: 1px dashed var(--card-border);
    color: var(--text-primary);
}}

/* Flashcard design */
.flashcard-inner {{
    min-height: 250px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    border-radius: 16px;
    padding: 30px;
    margin-bottom: 20px;
    box-shadow: var(--card-shadow);
    border: 2px solid var(--card-border);
    transition: all 0.3s ease;
}}

.flashcard-front {{
    background: linear-gradient(135deg, rgba(239, 246, 255, 0.9) 0%, rgba(219, 234, 254, 0.9) 100%);
    color: #1e3a8a;
}}

.flashcard-back {{
    background: linear-gradient(135deg, rgba(245, 243, 255, 0.9) 0%, rgba(237, 233, 254, 0.9) 100%);
    color: #4c1d95;
}}

.flashcard-text {{
    font-size: 22px;
    font-weight: 600;
}}

/* Customize default Streamlit elements */
.stTextInput>div>div>input, .stTextArea>div>div>textarea {{
    background-color: var(--card-bg) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 10px !important;
}}

/* Primary Buttons */
.stButton>button {{
    background: var(--primary-gradient) !important;
    color: white !important;
    border: none !important;
    padding: 10px 24px !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 14px 0 rgba(79, 70, 229, 0.3) !important;
    transition: all 0.3s ease !important;
    width: 100%;
}}

.stButton>button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px 0 rgba(79, 70, 229, 0.5) !important;
    color: white !important;
}}

/* Radio options styling */
.stRadio>div {{
    background-color: var(--card-bg) !important;
    padding: 12px !important;
    border-radius: 12px !important;
    border: 1px solid var(--card-border) !important;
}}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ----------------------------------------------------
# API Key Verification Warning
# ----------------------------------------------------
api_key_valid = True
if not os.getenv("OPENAI_API_KEY"):
    api_key_valid = False
    st.warning("⚠️ OpenAI API key is missing. Please set the `OPENAI_API_KEY` in settings or `.env` to enable AI summaries, chat, quizzes, and flashcards.")

# ----------------------------------------------------
# Sidebar Navigation Setup
# ----------------------------------------------------
pages = [
    "🏠 Home",
    "📁 Upload Notes",
    "📝 Paste Notes",
    "📊 AI Summary",
    "💬 Ask AI",
    "💡 Explain Simply",
    "📝 Quiz Generator",
    "🎴 Flashcards",
    "⚙️ Settings",
    "ℹ️ About"
]

# Synchronize selected page with session state
if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

default_index = pages.index(st.session_state.page) if st.session_state.page in pages else 0
selected_page = st.sidebar.selectbox("Navigate to", pages, index=default_index)

if selected_page != st.session_state.page:
    st.session_state.page = selected_page
    st.rerun()

# Helper CTA to show when no notes have been uploaded
def check_notes_loaded() -> bool:
    if not st.session_state.notes.strip():
        st.markdown("""
        <div class="glass-card" style="text-align: center; border: 2px dashed var(--primary);">
            <h3 style="margin: 0 0 10px 0;">No Notes Loaded</h3>
            <p style="color: var(--text-secondary); margin-bottom: 20px;">You need to upload notes or paste text before using this feature.</p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📁 Upload Notes Page"):
                st.session_state.page = "📁 Upload Notes"
                st.rerun()
        with col2:
            if st.button("📝 Paste Notes Page"):
                st.session_state.page = "📝 Paste Notes"
                st.rerun()
        return False
    return True

# ----------------------------------------------------
# 🏠 Page: Home
# ----------------------------------------------------
if st.session_state.page == "🏠 Home":
    st.markdown("""
    <div class="glass-card" style="text-align: center; background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%); margin-bottom: 30px;">
        <h1 style="margin: 0; color: var(--primary);">🎓 AI Study Buddy</h1>
        <p style="margin: 10px 0 0 0; font-size: 1.25rem; opacity: 0.85; font-weight: 400; color: var(--text-primary);">Upload your notes. Learn smarter with AI.</p>
    </div>
    """, unsafe_allow_html=True)

    # Statistics Section (KPI cards)
    st.subheader("📊 Your Study Statistics")
    duration_seconds = time.time() - st.session_state.stats["session_start_time"]
    minutes = int(duration_seconds // 60)
    seconds = int(duration_seconds % 60)
    duration_str = f"{minutes}m {seconds}s"
    
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-value">{st.session_state.stats["documents_uploaded"]}</div>
            <div class="kpi-label">Docs Uploaded</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-value">{st.session_state.stats["questions_asked"]}</div>
            <div class="kpi-label">Questions Asked</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-value">{st.session_state.stats["quizzes_generated"]}</div>
            <div class="kpi-label">Quizzes Taken</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-value">{st.session_state.stats["flashcards_generated"]}</div>
            <div class="kpi-label">Cards Created</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-value">{duration_str}</div>
            <div class="kpi-label">Session Duration</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Feature Grid Dashboard
    st.subheader("⚡ Features")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="glass-card" style="min-height: 180px;">
            <h4 style="margin: 0 0 8px 0;">📁 Upload Notes</h4>
            <p style="color: var(--text-secondary); font-size: 0.95rem; margin-bottom: 15px;">Upload notes in PDF, DOCX, or TXT format. Text is automatically parsed and saved to the session.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Upload", key="home_upload"):
            st.session_state.page = "📁 Upload Notes"
            st.rerun()

        st.markdown("""
        <div class="glass-card" style="min-height: 180px;">
            <h4 style="margin: 0 0 8px 0;">📊 AI Summary</h4>
            <p style="color: var(--text-secondary); font-size: 0.95rem; margin-bottom: 15px;">Generate short, medium, and detailed summaries, key points, topics, formulas, and definitions.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to AI Summary", key="home_summary"):
            st.session_state.page = "📊 AI Summary"
            st.rerun()

        st.markdown("""
        <div class="glass-card" style="min-height: 180px;">
            <h4 style="margin: 0 0 8px 0;">💡 Explain Simply</h4>
            <p style="color: var(--text-secondary); font-size: 0.95rem; margin-bottom: 15px;">Get a beginner-friendly explanation, real-world examples, analogies, and quick recaps of your notes.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Explain Simply", key="home_explain"):
            st.session_state.page = "💡 Explain Simply"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="glass-card" style="min-height: 180px;">
            <h4 style="margin: 0 0 8px 0;">📝 Paste Notes</h4>
            <p style="color: var(--text-secondary); font-size: 0.95rem; margin-bottom: 15px;">Don't have a document file? Simply paste your lecture notes or paragraphs directly in the text editor.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Paste Notes", key="home_paste"):
            st.session_state.page = "📝 Paste Notes"
            st.rerun()

        st.markdown("""
        <div class="glass-card" style="min-height: 180px;">
            <h4 style="margin: 0 0 8px 0;">💬 Ask AI Chatbot</h4>
            <p style="color: var(--text-secondary); font-size: 0.95rem; margin-bottom: 15px;">Interactive study companion. Chat about your notes. The AI answers only using your loaded notes.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Ask AI", key="home_chat"):
            st.session_state.page = "💬 Ask AI"
            st.rerun()

        st.markdown("""
        <div class="glass-card" style="min-height: 180px;">
            <h4 style="margin: 0 0 8px 0;">📝 Generate Quiz</h4>
            <p style="color: var(--text-secondary); font-size: 0.95rem; margin-bottom: 15px;">Generate exactly 10 MCQs based on your notes. Submit your responses and review incorrect answers.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Quiz", key="home_quiz"):
            st.session_state.page = "📝 Quiz Generator"
            st.rerun()

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("""
        <div class="glass-card" style="min-height: 180px;">
            <h4 style="margin: 0 0 8px 0;">🎴 Flashcards</h4>
            <p style="color: var(--text-secondary); font-size: 0.95rem; margin-bottom: 15px;">Automatically generate 10 customized flashcards to memorize definitions, dates, and core points.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Flashcards", key="home_cards"):
            st.session_state.page = "🎴 Flashcards"
            st.rerun()

# ----------------------------------------------------
# 📁 Page: Upload Notes
# ----------------------------------------------------
elif st.session_state.page == "📁 Upload Notes":
    st.markdown('<h1>📁 Upload Notes</h1>', unsafe_allow_html=True)
    st.write("Upload your lecture notes, documents or syllabus (PDF, DOCX, or TXT) to get started.")

    uploaded_file = st.file_uploader("Choose a study file (Max 10 MB)", type=["pdf", "docx", "txt"])

    if uploaded_file is not None:
        # Validate file
        is_valid, err_msg = utils.validate_file(uploaded_file)
        if not is_valid:
            st.error(f"❌ File validation failed: {err_msg}")
        else:
            # Check if this file is already processed to prevent re-processing on every UI render
            if st.session_state.notes_filename != uploaded_file.name:
                with st.spinner("⏳ Extracting text from document..."):
                    try:
                        ext = os.path.splitext(uploaded_file.name)[1].lower()
                        if ext == ".pdf":
                            raw_text = utils.extract_text_from_pdf(uploaded_file)
                        elif ext == ".docx":
                            raw_text = utils.extract_text_from_docx(uploaded_file)
                        else:  # txt
                            raw_text = utils.extract_text_from_txt(uploaded_file)
                            
                        cleaned = utils.clean_text(raw_text)
                        
                        if not cleaned:
                            st.error("⚠️ The uploaded document seems to have no readable text content.")
                        else:
                            st.session_state.notes = cleaned
                            st.session_state.notes_source = "upload"
                            st.session_state.notes_filename = uploaded_file.name
                            # Clear old AI outputs to generate new ones
                            st.session_state.summaries = None
                            st.session_state.explanations = None
                            st.session_state.quiz = None
                            st.session_state.quiz_answers = {}
                            st.session_state.quiz_submitted = False
                            st.session_state.flashcards = None
                            st.session_state.flashcard_index = 0
                            
                            utils.update_statistic("documents_uploaded")
                            st.success(f"🎉 Successfully extracted {len(cleaned.split())} words from {uploaded_file.name}!")
                    except Exception as e:
                        st.error(f"❌ Error extracting text: {str(e)}")

    if st.session_state.notes and st.session_state.notes_source == "upload":
        st.markdown(f"### Current Document: `{st.session_state.notes_filename}`")
        st.markdown(f'<div class="scroll-container"><pre style="white-space: pre-wrap; font-family: inherit;">{st.session_state.notes}</pre></div>', unsafe_allow_html=True)
        if st.button("Reset Document", key="reset_uploaded_doc"):
            utils.reset_notes_data()
            st.rerun()

# ----------------------------------------------------
# 📝 Page: Paste Notes
# ----------------------------------------------------
elif st.session_state.page == "📝 Paste Notes":
    st.markdown('<h1>📝 Paste Notes</h1>', unsafe_allow_html=True)
    st.write("Paste your study material below. There's no character limit!")

    pasted_text_input = st.text_area(
        "Enter or paste study text here:", 
        value=st.session_state.notes if st.session_state.notes_source == "paste" else "", 
        height=300,
        placeholder="Paste articles, syllabus notes, slide transcriptions..."
    )

    if st.button("💾 Save Pasted Notes"):
        cleaned = utils.clean_text(pasted_text_input)
        if not cleaned:
            st.error("⚠️ Please paste some valid text first.")
        else:
            st.session_state.notes = cleaned
            st.session_state.notes_source = "paste"
            st.session_state.notes_filename = "Pasted Notes"
            # Clear old outputs
            st.session_state.summaries = None
            st.session_state.explanations = None
            st.session_state.quiz = None
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False
            st.session_state.flashcards = None
            st.session_state.flashcard_index = 0
            
            utils.update_statistic("documents_uploaded")
            st.success(f"🎉 Successfully saved notes! ({len(cleaned.split())} words)")
            st.rerun()

    if st.session_state.notes and st.session_state.notes_source == "paste":
        st.markdown("### Saved Text Overview")
        st.markdown(f'<div class="scroll-container"><pre style="white-space: pre-wrap; font-family: inherit;">{st.session_state.notes}</pre></div>', unsafe_allow_html=True)
        if st.button("Clear Pasted Notes"):
            utils.reset_notes_data()
            st.rerun()

# ----------------------------------------------------
# 📊 Page: AI Summary
# ----------------------------------------------------
elif st.session_state.page == "📊 AI Summary":
    st.markdown('<h1>📊 AI Summary</h1>', unsafe_allow_html=True)
    st.write("Generate short, medium, and comprehensive summaries alongside key elements of your notes.")

    if check_notes_loaded():
        if not api_key_valid:
            st.error("API Key not found. Please add your key in Settings to use summaries.")
        else:
            if st.session_state.summaries is None:
                if st.button("✨ Generate AI Summary"):
                    with st.spinner("⏳ Analyzing notes and creating summary structures..."):
                        try:
                            summary_data = ai.summarize_notes(st.session_state.notes)
                            st.session_state.summaries = summary_data
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Summarization failed: {str(e)}")
            else:
                summary = st.session_state.summaries
                
                # Tab layout for summaries
                tab1, tab2, tab3 = st.tabs(["📝 Short Summary", "📄 Medium Summary", "📖 Detailed Summary"])
                
                with tab1:
                    st.markdown(f"""
                    <div class="glass-card">
                        <h3>Short Summary</h3>
                        <p>{summary.get('short_summary', 'Not available.')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with tab2:
                    st.markdown(f"""
                    <div class="glass-card">
                        <h3>Medium Summary</h3>
                        <p>{summary.get('medium_summary', 'Not available.')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with tab3:
                    st.markdown(f"""
                    <div class="glass-card">
                        <h3>Detailed Summary</h3>
                        <div style="line-height: 1.6;">{summary.get('detailed_summary', 'Not available.').replace(chr(10), '<br/><br/>')}</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.subheader("💡 Key Takeaways")
                
                # Double column layout for Key points and Important topics
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown('<div class="glass-card" style="min-height: 250px;"><h4>🔑 Key Points</h4>', unsafe_allow_html=True)
                    points = summary.get('key_points', [])
                    if points:
                        for p in points:
                            st.write(f"- {p}")
                    else:
                        st.write("No key points generated.")
                    st.markdown('</div>', unsafe_allow_html=True)

                with col2:
                    st.markdown('<div class="glass-card" style="min-height: 250px;"><h4>📌 Important Topics</h4>', unsafe_allow_html=True)
                    topics = summary.get('important_topics', [])
                    if topics:
                        tags_html = "".join(f'<span style="background: var(--primary); color: white; padding: 6px 12px; border-radius: 20px; font-size: 13px; margin-right: 8px; margin-bottom: 8px; display: inline-block; font-weight: 500;">{t}</span>' for t in topics)
                        st.markdown(tags_html, unsafe_allow_html=True)
                    else:
                        st.write("No topics extracted.")
                    st.markdown('</div>', unsafe_allow_html=True)

                # Definitions, Dates, Formulas
                st.subheader("📚 Detailed Insights")
                
                col3, col4 = st.columns(2)
                with col3:
                    st.markdown('<div class="glass-card" style="min-height: 250px;"><h4>📘 Definitions</h4>', unsafe_allow_html=True)
                    definitions = summary.get('definitions', [])
                    if definitions:
                        for item in definitions:
                            if isinstance(item, dict):
                                term = item.get('term', '')
                                defn = item.get('definition', '')
                                st.markdown(f"**{term}**: {defn}")
                            else:
                                st.write(f"- {item}")
                    else:
                        st.write("No definitions extracted.")
                    st.markdown('</div>', unsafe_allow_html=True)

                with col4:
                    st.markdown('<div class="glass-card" style="min-height: 250px;"><h4>📅 Key Dates & Formulas</h4>', unsafe_allow_html=True)
                    dates = summary.get('important_dates', [])
                    formulas = summary.get('important_formulas', [])
                    
                    if dates:
                        st.markdown("##### Key Dates / Timeline")
                        for d in dates:
                            if isinstance(d, dict):
                                date_val = d.get('date', '')
                                event_val = d.get('event', '')
                                st.markdown(f"🕒 **{date_val}**: {event_val}")
                            else:
                                st.markdown(f"🕒 {d}")
                                
                    if formulas:
                        st.markdown("<div style='margin-top: 15px;'>##### Key Formulas</div>", unsafe_allow_html=True)
                        for f in formulas:
                            st.code(f)
                            
                    if not dates and not formulas:
                        st.write("No specific dates or formulas found in the notes.")
                    st.markdown('</div>', unsafe_allow_html=True)

                # Re-generate summary
                if st.button("🔄 Regenerate Summary"):
                    st.session_state.summaries = None
                    st.rerun()

# ----------------------------------------------------
# 💬 Page: Ask AI (Chatbot)
# ----------------------------------------------------
elif st.session_state.page == "💬 Ask AI":
    st.markdown('<h1>💬 Ask AI Chatbot</h1>', unsafe_allow_html=True)
    st.write("Chat with your notes. Note: The Study Buddy replies strictly using details from your notes.")

    if check_notes_loaded():
        if not api_key_valid:
            st.error("API Key not found. Please add your key in Settings to use the chat.")
        else:
            # Display Chat History
            chat_container = st.container()
            with chat_container:
                for msg in st.session_state.chat_history:
                    avatar = "🧑‍🎓" if msg["role"] == "user" else "🤖"
                    with st.chat_message(msg["role"], avatar=avatar):
                        st.markdown(f"<div style='line-height:1.5;'>{msg['content']}</div>", unsafe_allow_html=True)

            # Chat Input
            if prompt := st.chat_input("Ask a question about your notes..."):
                # Render User Message immediately
                with st.chat_message("user", avatar="🧑‍🎓"):
                    st.markdown(prompt)
                
                # Call OpenAI
                with st.spinner("Thinking..."):
                    # Record query
                    utils.update_statistic("questions_asked")
                    # Construct call
                    response = ai.ask_ai(st.session_state.notes, prompt, st.session_state.chat_history)
                    
                # Append to session state
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()

            # Clear Chat Button
            if st.session_state.chat_history:
                if st.button("🧹 Clear Chat History"):
                    st.session_state.chat_history = []
                    st.rerun()

# ----------------------------------------------------
# 💡 Page: Explain Simply
# ----------------------------------------------------
elif st.session_state.page == "💡 Explain Simply":
    st.markdown('<h1>💡 Explain Simply</h1>', unsafe_allow_html=True)
    st.write("Deconstruct complex ideas into extremely beginner-friendly concepts, analogies, and practical examples.")

    if check_notes_loaded():
        if not api_key_valid:
            st.error("API Key not found. Please add your key in Settings.")
        else:
            if st.session_state.explanations is None:
                if st.button("💡 Simplify My Notes"):
                    with st.spinner("⏳ Analyzing concepts and rewriting simply..."):
                        try:
                            expl = ai.explain_simple(st.session_state.notes)
                            st.session_state.explanations = expl
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Explanation generation failed: {str(e)}")
            else:
                data = st.session_state.explanations
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    <div class="glass-card" style="min-height: 280px;">
                        <h3 style="color: #2563eb !important;">🧒 Beginner-Friendly Explanation</h3>
                        <p style="line-height: 1.6;">{data.get('beginner_explanation', 'No explanation generated.')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="glass-card" style="min-height: 250px;">
                        <h3 style="color: #059669 !important;">🎢 Easy Analogy</h3>
                        <p style="line-height: 1.6; font-style: italic;">{data.get('easy_analogy', 'No analogy generated.')}</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                    <div class="glass-card" style="min-height: 280px;">
                        <h3 style="color: #7c3aed !important;">🌍 Real-World Example</h3>
                        <p style="line-height: 1.6;">{data.get('real_world_example', 'No example generated.')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="glass-card" style="min-height: 250px;">
                        <h3 style="color: #ea580c !important;">📝 Short Recap</h3>
                        <p style="line-height: 1.6; font-weight: 500;">{data.get('short_recap', 'No recap generated.')}</p>
                    </div>
                    """, unsafe_allow_html=True)

                if st.button("🔄 Regenerate Simplifications"):
                    st.session_state.explanations = None
                    st.rerun()

# ----------------------------------------------------
# 📝 Page: Quiz Generator
# ----------------------------------------------------
elif st.session_state.page == "📝 Quiz Generator":
    st.markdown('<h1>📝 Quiz Generator</h1>', unsafe_allow_html=True)
    st.write("Generate a challenge of exactly 10 multiple-choice questions to test your knowledge.")

    if check_notes_loaded():
        if not api_key_valid:
            st.error("API Key not found. Please add your key in Settings.")
        else:
            if st.session_state.quiz is None:
                if st.button("📝 Generate Quiz"):
                    with st.spinner("⏳ Compiling quiz questions from notes..."):
                        try:
                            quiz_data = ai.generate_quiz(st.session_state.notes)
                            st.session_state.quiz = quiz_data
                            st.session_state.quiz_answers = {}
                            st.session_state.quiz_submitted = False
                            utils.update_statistic("quizzes_generated")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Quiz generation failed: {str(e)}")
            else:
                quiz = st.session_state.quiz
                
                # Show instructions
                st.info("💡 Answer all 10 questions and click 'Submit Quiz' at the bottom to see your score and explanations.")

                # Render Questions
                for idx, q in enumerate(quiz):
                    st.markdown(f"#### Q{idx + 1}: {q['question']}")
                    
                    # Selected answer tracker
                    current_selected = st.session_state.quiz_answers.get(idx)
                    current_idx = None
                    if current_selected in q["options"]:
                        current_idx = q["options"].index(current_selected)
                        
                    selected_ans = st.radio(
                        f"Select your answer for Q{idx + 1}:",
                        q["options"],
                        index=current_idx,
                        key=f"quiz_radio_q_{idx}",
                        disabled=st.session_state.quiz_submitted,
                        label_visibility="collapsed"
                    )
                    
                    if selected_ans != current_selected:
                        st.session_state.quiz_answers[idx] = selected_ans

                    # If submitted, show feedback immediately below the question
                    if st.session_state.quiz_submitted:
                        user_ans = st.session_state.quiz_answers.get(idx)
                        correct_ans = q["correct_answer"]
                        
                        if user_ans == correct_ans:
                            st.success(f"✅ Correct! Answer is: {correct_ans}")
                        else:
                            st.error(f"❌ Incorrect! You selected: '{user_ans or 'No Answer'}'. Correct answer: '{correct_ans}'")
                        
                        st.markdown(f"""
                        <div style="background-color: rgba(255,255,255,0.05); padding: 10px 15px; border-radius: 8px; border-left: 4px solid var(--primary); margin-bottom: 20px;">
                            <strong>Explanation:</strong> {q['explanation']}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.write("") # Margin spacing

                # Submit Actions
                if not st.session_state.quiz_submitted:
                    if st.button("Submit Quiz"):
                        # Check if all questions are answered
                        unanswered = [i for i in range(10) if i not in st.session_state.quiz_answers]
                        if unanswered:
                            st.warning(f"⚠️ Please complete all questions before submitting. Unanswered: {', '.join(str(u + 1) for u in unanswered)}")
                        else:
                            st.session_state.quiz_submitted = True
                            st.rerun()
                else:
                    # Renders score metrics at the bottom if submitted
                    score = sum(1 for i, q in enumerate(quiz) if st.session_state.quiz_answers.get(i) == q["correct_answer"])
                    percentage = int((score / 10) * 100)
                    
                    # Score color coding
                    if score >= 8:
                        result_emoji = "🏆 Excellence!"
                        alert_func = st.success
                    elif score >= 5:
                        result_emoji = "👍 Good job!"
                        alert_func = st.info
                    else:
                        result_emoji = "📚 Keep studying!"
                        alert_func = st.warning

                    st.markdown("---")
                    st.markdown(f"""
                    <div class="glass-card" style="text-align: center;">
                        <h2>Quiz Results Summary</h2>
                        <div style="font-size: 40px; font-weight: 800; color: var(--primary); margin: 15px 0;">{score} / 10</div>
                        <h4 style="margin: 0;">{percentage}% — {result_emoji}</h4>
                    </div>
                    """, unsafe_allow_html=True)

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🔄 Reset Quiz & Retry"):
                            st.session_state.quiz_answers = {}
                            st.session_state.quiz_submitted = False
                            st.rerun()
                    with col2:
                        if st.button("✨ Generate New Questions"):
                            st.session_state.quiz = None
                            st.session_state.quiz_answers = {}
                            st.session_state.quiz_submitted = False
                            st.rerun()

# ----------------------------------------------------
# 🎴 Page: Flashcards
# ----------------------------------------------------
elif st.session_state.page == "🎴 Flashcards":
    st.markdown('<h1>🎴 Flashcards</h1>', unsafe_allow_html=True)
    st.write("Memorize core terms and definitions with generated interactive flipcards.")

    if check_notes_loaded():
        if not api_key_valid:
            st.error("API Key not found. Please add your key in Settings.")
        else:
            if st.session_state.flashcards is None:
                if st.button("🎴 Generate Flashcards"):
                    with st.spinner("⏳ Creating study cards..."):
                        try:
                            cards = ai.generate_flashcards(st.session_state.notes)
                            st.session_state.flashcards = cards
                            st.session_state.flashcard_index = 0
                            st.session_state.flashcard_flipped = False
                            utils.update_statistic("flashcards_generated")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Flashcard generation failed: {str(e)}")
            else:
                cards = st.session_state.flashcards
                idx = st.session_state.flashcard_index
                card = cards[idx]

                # Render progress text
                st.write(f"**Card {idx + 1} of {len(cards)}**")
                
                # Active card layout
                side = "back" if st.session_state.flashcard_flipped else "front"
                text = card[side]
                label = "💡 Answer" if st.session_state.flashcard_flipped else "❓ Question"
                c_class = "flashcard-back" if st.session_state.flashcard_flipped else "flashcard-front"

                st.markdown(f"""
                <div class="flashcard-inner {c_class}">
                    <div>
                        <div style="font-size: 13px; font-weight: 700; text-transform: uppercase; opacity: 0.75; letter-spacing: 1px; margin-bottom: 12px;">{label}</div>
                        <div class="flashcard-text">{text}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Horizontal navigation buttons
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    prev_disabled = idx == 0
                    if st.button("⬅️ Previous", disabled=prev_disabled, key="btn_fc_prev"):
                        st.session_state.flashcard_index -= 1
                        st.session_state.flashcard_flipped = False
                        st.rerun()

                with col2:
                    if st.button("🔄 Flip Card", key="btn_fc_flip"):
                        st.session_state.flashcard_flipped = not st.session_state.flashcard_flipped
                        st.rerun()

                with col3:
                    next_disabled = idx == len(cards) - 1
                    if st.button("Next ➡️", disabled=next_disabled, key="btn_fc_next"):
                        st.session_state.flashcard_index += 1
                        st.session_state.flashcard_flipped = False
                        st.rerun()

                # Re-generate action
                st.markdown("---")
                if st.button("✨ Generate New Flashcards"):
                    st.session_state.flashcards = None
                    st.rerun()

# ----------------------------------------------------
# ⚙️ Page: Settings
# ----------------------------------------------------
elif st.session_state.page == "⚙️ Settings":
    st.markdown('<h1>⚙️ Settings</h1>', unsafe_allow_html=True)
    st.write("Customize your study environment and manage session states.")

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🎨 Appearance Settings")
    
    # Theme configuration
    theme_opt = st.selectbox(
        "Application Theme Mode",
        ["Light Mode", "Dark Mode"],
        index=0 if theme == "light" else 1
    )
    new_theme = "light" if theme_opt == "Light Mode" else "dark"
    if new_theme != theme:
        st.session_state.settings["theme"] = new_theme
        st.rerun()

    # Font size slider
    new_font_size = st.slider(
        "Application Font Size (px)",
        min_value=12,
        max_value=24,
        value=font_size,
        step=1
    )
    if new_font_size != font_size:
        st.session_state.settings["font_size"] = new_font_size
        st.rerun()
        
    st.markdown('</div>', unsafe_allow_html=True)

    # API key setup panel
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🔑 OpenAI API Key Configuration")
    api_key_input = st.text_input("Enter OpenAI API Key", value=os.getenv("OPENAI_API_KEY", ""), type="password")
    
    if st.button("Save API Key"):
        os.environ["OPENAI_API_KEY"] = api_key_input
        try:
            with open(".env", "w") as f:
                f.write(f"OPENAI_API_KEY={api_key_input}\n")
            st.success("API key written to .env file successfully!")
        except Exception:
            st.success("API key set in application memory for this session.")
        time.sleep(1)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Manage Active Notes
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📁 Session Management")
    if st.session_state.notes:
        st.write(f"**Loaded Source**: `{st.session_state.notes_filename}`")
        st.write(f"**Character Count**: `{len(st.session_state.notes)}` characters")
        st.write(f"**Word Count**: `{len(st.session_state.notes.split())}` words")
        
        if st.button("Reset Active Notes & History", key="settings_reset_notes"):
            utils.reset_notes_data()
            st.success("Active session notes and history cleared!")
            time.sleep(1)
            st.rerun()
    else:
        st.info("No study notes are currently loaded in the active session state.")
    
    # Manage stats
    if st.button("Reset Study Statistics", key="settings_reset_stats"):
        utils.reset_statistics()
        st.success("Statistics reset to initial values!")
        time.sleep(1)
        st.rerun()
        
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------
# ℹ️ Page: About
# ----------------------------------------------------
elif st.session_state.page == "ℹ️ About":
    st.markdown('<h1>ℹ️ About AI Study Buddy</h1>', unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
        <h3>AI Study Buddy — Version 1.0</h3>
        <p style="line-height: 1.6;">
            <strong>AI Study Buddy</strong> is a comprehensive, production-grade interactive learning companion designed 
            to maximize study efficiency. By parsing your documents or pasted notes, the application uses advanced language 
            models to extract summaries, structure custom study guides, answer targeted context-bound questions, create 
            custom multi-choice quizzes, and compile flashcards.
        </p>
        <p style="line-height: 1.6;">
            <strong>Core Stack:</strong>
            <ul>
                <li><strong>Frontend:</strong> Streamlit Framework with customized styling</li>
                <li><strong>Natural Language Engine:</strong> OpenAI GPT API Integration</li>
                <li><strong>File Utilities:</strong> pdfplumber, python-docx, and core Python text tools</li>
            </ul>
        </p>
        <hr style="border-top: 1px solid var(--card-border); margin: 20px 0;"/>
        <p style="font-size: 0.9rem; color: var(--text-secondary); text-align: center;">
            Built with ❤️ using Streamlit & OpenAI.
        </p>
    </div>
    """, unsafe_allow_html=True)
