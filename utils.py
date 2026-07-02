import os
import time
import pathlib
import pdfplumber
import docx
import streamlit as st
from typing import Tuple, Dict, Any

# Define limits
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

def validate_file(uploaded_file) -> Tuple[bool, str]:
    """
    Validates the uploaded file.
    Checks:
    - If file is uploaded.
    - File extension (must be PDF, DOCX, TXT).
    - File size (must not exceed 10 MB).
    
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if uploaded_file is None:
        return False, "No file uploaded."
        
    filename = uploaded_file.name
    file_ext = pathlib.Path(filename).suffix.lower()
    
    if file_ext not in [".pdf", ".docx", ".txt"]:
        return False, f"Unsupported file format: {file_ext}. Please upload .pdf, .docx, or .txt files."
        
    # Check size
    # Check file size from Streamlit's size attribute
    if uploaded_file.size > MAX_FILE_SIZE_BYTES:
        max_size_mb = MAX_FILE_SIZE_BYTES / (1024 * 1024)
        return False, f"File size exceeds the limit of {max_size_mb} MB."
        
    return True, ""

def extract_text_from_pdf(file) -> str:
    """
    Extracts text from a PDF file object using pdfplumber.
    """
    text_content = []
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)
        return "\n".join(text_content)
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")

def extract_text_from_docx(file) -> str:
    """
    Extracts text from a DOCX file object using python-docx.
    """
    try:
        doc = docx.Document(file)
        text_content = []
        for paragraph in doc.paragraphs:
            text_content.append(paragraph.text)
        return "\n".join(text_content)
    except Exception as e:
        raise Exception(f"Failed to extract text from DOCX: {str(e)}")

def extract_text_from_txt(file) -> str:
    """
    Extracts text from a TXT file object.
    """
    try:
        # Read and decode
        return file.read().decode("utf-8", errors="ignore")
    except Exception as e:
        raise Exception(f"Failed to extract text from TXT: {str(e)}")

def clean_text(text: str) -> str:
    """
    Cleans raw extracted text by stripping surrounding whitespace,
    collapsing multiple empty lines, and ensuring basic format consistency.
    """
    if not text:
        return ""
    lines = text.splitlines()
    cleaned_lines = [line.strip() for line in lines]
    # Filter out excessive empty lines
    non_empty_lines = []
    consecutive_empty = 0
    for line in cleaned_lines:
        if line == "":
            consecutive_empty += 1
            if consecutive_empty <= 1:
                non_empty_lines.append(line)
        else:
            consecutive_empty = 0
            non_empty_lines.append(line)
            
    return "\n".join(non_empty_lines).strip()

def init_session_state() -> None:
    """
    Initializes all Streamlit session state keys if they do not exist.
    """
    if "notes" not in st.session_state:
        st.session_state.notes = ""
    if "notes_source" not in st.session_state:
        st.session_state.notes_source = None  # 'upload', 'paste', or None
    if "notes_filename" not in st.session_state:
        st.session_state.notes_filename = ""
        
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        
    if "stats" not in st.session_state:
        st.session_state.stats = {
            "documents_uploaded": 0,
            "questions_asked": 0,
            "quizzes_generated": 0,
            "flashcards_generated": 0,
            "session_start_time": time.time()
        }
        
    if "settings" not in st.session_state:
        st.session_state.settings = {
            "theme": "light",       # 'light' or 'dark'
            "font_size": 16,        # between 12 and 24
        }
        
    if "quiz" not in st.session_state:
        st.session_state.quiz = None  # Will hold list of 10 dicts
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}  # {q_index: selected_option}
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
        
    if "flashcards" not in st.session_state:
        st.session_state.flashcards = None  # Will hold list of dicts
    if "flashcard_index" not in st.session_state:
        st.session_state.flashcard_index = 0
    if "flashcard_flipped" not in st.session_state:
        st.session_state.flashcard_flipped = False
        
    if "summaries" not in st.session_state:
        st.session_state.summaries = None  # dict with keys: short, medium, detailed, etc.
        
    if "explanations" not in st.session_state:
        st.session_state.explanations = None  # dict with keys: simple_explanation, real_world_example, analogy, recap

def update_statistic(stat_name: str, amount: int = 1) -> None:
    """
    Safely increments a study statistic.
    """
    if "stats" in st.session_state and stat_name in st.session_state.stats:
        st.session_state.stats[stat_name] += amount

def reset_notes_data() -> None:
    """
    Resets the uploaded notes data and relevant generated content.
    """
    st.session_state.notes = ""
    st.session_state.notes_source = None
    st.session_state.notes_filename = ""
    st.session_state.chat_history = []
    st.session_state.quiz = None
    st.session_state.quiz_answers = {}
    st.session_state.quiz_submitted = False
    st.session_state.flashcards = None
    st.session_state.flashcard_index = 0
    st.session_state.flashcard_flipped = False
    st.session_state.summaries = None
    st.session_state.explanations = None

def reset_statistics() -> None:
    """
    Resets the statistics counters and session timer.
    """
    if "stats" in st.session_state:
        st.session_state.stats = {
            "documents_uploaded": 0,
            "questions_asked": 0,
            "quizzes_generated": 0,
            "flashcards_generated": 0,
            "session_start_time": time.time()
        }
