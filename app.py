import streamlit as st
import google.generativeai as genai
import PyPDF2
from docx import Document

st.set_page_config(page_title="AI Text Summarizer", page_icon="✨", layout="wide")

st.title("✨ AI Text Summarizer")
st.write("Upload file or paste text, then generate summary.")

api_key = st.secrets["GEMINI_API_KEY"]

uploaded_file = st.file_uploader("Upload TXT, PDF, DOCX", type=["txt", "pdf", "docx"])
text_input = st.text_area("Or paste your text here", height=200)

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".txt"):
            text_input = uploaded_file.read().decode("utf-8")
        elif uploaded_file.name.endswith(".pdf"):
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text_input = "".join([page.extract_text() or "" for page in pdf_reader.pages])
        elif uploaded_file.name.endswith(".docx"):
            doc = Document(uploaded_file)
            text_input = "\n".join([p.text for p in doc.paragraphs])
        st.success("File loaded successfully.")
    except Exception as e:
        st.error(f"File error: {e}")

style = st.selectbox("Summary Style", ["Short", "Bullet Points", "Detailed"])
lang = st.selectbox("Language", ["English", "Bangla", "Auto Detect"])

if st.button("Generate Summary"):
    if not text_input.strip():
        st.error("Please enter or upload text.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")

            lang_instruction = ""
            if lang == "Bangla":
                lang_instruction = "Respond in Bangla."
            elif lang == "English":
                lang_instruction = "Respond in English."
            else:
                lang_instruction = "Respond in the same language as input."

            if style == "Short":
                style_instruction = "Summarize in 2-3 short sentences."
            elif style == "Bullet Points":
                style_instruction = "Summarize in bullet points."
            else:
                style_instruction = "Give a detailed summary."

            prompt = f"{lang_instruction}\n{style_instruction}\n\n{text_input}"
            response = model.generate_content(prompt)

            st.subheader("Summary")
            st.write(response.text)

        except Exception as e:
            st.error(f"API error: {e}")