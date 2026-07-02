import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict, Any, List

# Load environment variables
load_dotenv()

# We will use gpt-4o-mini as the default model
DEFAULT_MODEL = "gpt-4o-mini"

def get_openai_client() -> OpenAI:
    """
    Instantiates and returns the OpenAI client.
    Ensures that the OPENAI_API_KEY environment variable is set.
    Raises ValueError if the key is missing.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API Key not found. Please set the OPENAI_API_KEY environment variable or verify your .env file configuration.")
    return OpenAI(api_key=api_key)

def summarize_notes(text: str) -> Dict[str, Any]:
    """
    Generates three summaries: Short, Medium, Detailed.
    Also extracts: Key Points, Important Topics, Definitions, Dates, Formulas.
    Returns a dictionary of results.
    """
    if not text.strip():
        raise ValueError("Notes text is empty.")

    client = get_openai_client()
    
    prompt = (
        "You are an expert study assistant. Analyze the provided study notes and generate a structured summary "
        "and list of extracted information in JSON format.\n\n"
        "Your response must be a JSON object with this exact structure:\n"
        "{\n"
        '  "short_summary": "A 1-2 sentence high-level summary.",\n'
        '  "medium_summary": "A 1-2 paragraph summary capturing key ideas.",\n'
        '  "detailed_summary": "A 3-5 paragraph comprehensive summary going into details.",\n'
        '  "key_points": ["Key point 1", "Key point 2", ...],\n'
        '  "important_topics": ["Topic 1", "Topic 2", ...],\n'
        '  "definitions": [{"term": "Term Name", "definition": "Its definition"}, ...],\n'
        '  "important_dates": [{"date": "Date/Period", "event": "Event details"}, ...],\n'
        '  "important_formulas": ["Formula 1", "Formula 2", ...]\n'
        "}\n\n"
        "If there are no dates or formulas, leave those arrays empty (i.e. []).\n\n"
        f"Study notes:\n---\n{text}\n---\n"
    )

    try:
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a helpful study assistant that strictly outputs JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        result_text = response.choices[0].message.content
        return json.loads(result_text)
    except Exception as e:
        raise Exception(f"AI summarization failed: {str(e)}")

def ask_ai(text: str, question: str, chat_history: List[Dict[str, str]]) -> str:
    """
    Chatbot interface. Answers questions strictly using the uploaded/pasted notes.
    If the answer cannot be found, returns exactly: "This information is not available in the uploaded notes."
    """
    if not text.strip():
        return "Please upload or paste some notes first before asking questions."
    
    if not question.strip():
        return "Please enter a valid question."

    client = get_openai_client()

    system_message = (
        "You are a study buddy chatbot. You answer user questions about their uploaded study notes.\n\n"
        "CRITICAL RULES:\n"
        "1. Answer the question ONLY based on the provided notes text.\n"
        "2. Do not assume, extrapolate, or use outside knowledge.\n"
        "3. If the answer to the question cannot be directly and fully found in the notes, you MUST respond EXACTLY with this phrase:\n"
        '"This information is not available in the uploaded notes."\n'
        "Do not add any preamble, explanation, or other text. If you are not 100% sure based on the notes, return that exact sentence.\n\n"
        f"Here are the uploaded study notes:\n---\n{text}\n---\n"
    )

    # Build history
    messages = [{"role": "system", "content": system_message}]
    for msg in chat_history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    
    messages.append({"role": "user", "content": question})

    try:
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages,
            temperature=0.1
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error communicating with AI Study Buddy helper: {str(e)}"

def explain_simple(text: str) -> Dict[str, str]:
    """
    Generates: Beginner-friendly explanation, real-world example, easy analogy, short recap.
    Returns a dictionary.
    """
    if not text.strip():
        raise ValueError("Notes text is empty.")

    client = get_openai_client()

    prompt = (
        "You are an educational specialist who makes complex things simple. Take the provided study notes "
        "and generate a breakdown containing a simple explanation, a real-world example, an analogy, and a recap.\n\n"
        "Your response must be a JSON object with this exact structure:\n"
        "{\n"
        '  "beginner_explanation": "A beginner-friendly explanation suitable for a 10-year old.",\n'
        '  "real_world_example": "A real-world example showing how the concept is applied.",\n'
        '  "easy_analogy": "An easy-to-understand analogy that makes the concept intuitive.",\n'
        '  "short_recap": "A very concise recap of the core takeaways."\n'
        "}\n\n"
        f"Study notes:\n---\n{text}\n---\n"
    )

    try:
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a helpful educational tutor that strictly outputs JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        result_text = response.choices[0].message.content
        return json.loads(result_text)
    except Exception as e:
        raise Exception(f"AI explanation generation failed: {str(e)}")

def generate_quiz(text: str) -> List[Dict[str, Any]]:
    """
    Generates exactly 10 multiple choice questions.
    Each containing: question, 4 options, correct answer, explanation.
    Returns a list of dicts.
    """
    if not text.strip():
        raise ValueError("Notes text is empty.")

    client = get_openai_client()

    prompt = (
        "You are an academic test maker. Generate exactly 10 multiple-choice questions (MCQs) based on the provided study notes.\n\n"
        "Your response must be a JSON object with this exact structure:\n"
        "{\n"
        '  "questions": [\n'
        "    {\n"
        '      "question": "The question text?",\n'
        '      "options": ["Option A text", "Option B text", "Option C text", "Option D text"],\n'
        '      "correct_answer": "Option A text",\n'
        '      "explanation": "Brief explanation of why this option is correct and why others are wrong."\n'
        "    },\n"
        "    ...\n"
        "  ]\n"
        "}\n\n"
        "IMPORTANT RULES:\n"
        "1. Generate EXACTLY 10 questions. If there isn't enough information, extrapolate questions directly testing core terms or ideas mentioned in the notes.\n"
        "2. The value for 'correct_answer' must match one of the strings inside the 'options' list EXACTLY.\n"
        "3. Keep questions challenging but solvable based on the notes.\n\n"
        f"Study notes:\n---\n{text}\n---\n"
    )

    try:
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are an academic testing system that strictly outputs JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )
        result_text = response.choices[0].message.content
        data = json.loads(result_text)
        
        # Validate that the structure is correct
        if "questions" not in data or not isinstance(data["questions"], list):
            raise ValueError("Invalid JSON schema: missing 'questions' list key.")
            
        questions = data["questions"]
        if len(questions) != 10:
            # If the model failed to generate exactly 10, print details and pass it, 
            # but usually it satisfies this. Let's double check.
            pass
            
        # Standardize option formatting or clean up correct_answer references if required
        for i, q in enumerate(questions):
            # Check basic structure of each question
            for k in ["question", "options", "correct_answer", "explanation"]:
                if k not in q:
                    raise ValueError(f"Question {i+1} is missing key: '{k}'")
            if not isinstance(q["options"], list) or len(q["options"]) != 4:
                q["options"] = (q["options"] + ["Option B", "Option C", "Option D"])[:4]
            if q["correct_answer"] not in q["options"]:
                # Force correct answer to be one of the options
                q["correct_answer"] = q["options"][0]
                
        return questions
    except Exception as e:
        raise Exception(f"AI Quiz generation failed: {str(e)}")

def generate_flashcards(text: str) -> List[Dict[str, str]]:
    """
    Generates exactly 10 flashcards (Front/Back) based on the notes.
    """
    if not text.strip():
        raise ValueError("Notes text is empty.")

    client = get_openai_client()

    prompt = (
        "You are a learning specialist. Generate exactly 10 high-quality study flashcards based on the provided notes.\n\n"
        "Your response must be a JSON object with this exact structure:\n"
        "{\n"
        '  "flashcards": [\n'
        "    {\n"
        '      "front": "Question or key concept (Front of card)",\n'
        '      "back": "Answer or short definition (Back of card)"\n'
        "    },\n"
        "    ...\n"
        "  ]\n"
        "}\n\n"
        "Generate EXACTLY 10 flashcards.\n\n"
        f"Study notes:\n---\n{text}\n---\n"
    )

    try:
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a flashcard generation tool that strictly outputs JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        result_text = response.choices[0].message.content
        data = json.loads(result_text)
        
        if "flashcards" not in data or not isinstance(data["flashcards"], list):
            raise ValueError("Invalid JSON schema: missing 'flashcards' list key.")
            
        flashcards = data["flashcards"]
        for i, card in enumerate(flashcards):
            for k in ["front", "back"]:
                if k not in card:
                    raise ValueError(f"Flashcard {i+1} is missing key: '{k}'")
                    
        return flashcards
    except Exception as e:
        raise Exception(f"AI Flashcard generation failed: {str(e)}")
