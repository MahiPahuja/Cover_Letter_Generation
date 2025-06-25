import streamlit as st
import fitz  # PyMuPDF
import asyncio
from resume_pipeline import main
from memory_store import set_tone

# Function to extract text from uploaded PDF
def extract_text_from_pdf(uploaded_file):
    if uploaded_file is not None:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            return text
    return ""

# Streamlit app configuration
st.set_page_config(page_title="Resume Optimizer", layout="wide")
st.title("📄 Resume and Job Description Optimizer")

# ---------------- Resume Input ----------------
st.subheader("Upload Resume")
resume_input_type = st.radio("Choose input type for Resume", ["Upload PDF", "Enter Text"])

if resume_input_type == "Upload PDF":
    resume_file = st.file_uploader("Upload Resume PDF", type=["pdf"], key="resume")
    resume_text = extract_text_from_pdf(resume_file) if resume_file else ""
else:
    resume_text = st.text_area("Paste Resume Text", height=200, key="resume_text")

# ---------------- Job Description Input ----------------
st.subheader("Upload Job Description")
jd_input_type = st.radio("Choose input type for Job Description", ["Upload PDF", "Enter Text"])

if jd_input_type == "Upload PDF":
    jd_file = st.file_uploader("Upload Job Description PDF", type=["pdf"], key="jd")
    jd_text = extract_text_from_pdf(jd_file) if jd_file else ""
else:
    jd_text = st.text_area("Paste Job Description Text", height=200, key="jd_text")

# ---------------- Tone Input ----------------
st.subheader("Choose Tone for Cover Letter")
tone = st.selectbox(
    "Select tone of writing",
    ["professional", "formal", "informal", "friendly", "enthusiastic"],
    index=0  # Default to "professional"
)

# Display selected tone
st.info(f"Selected tone: **{tone}**")

# ---------------- Submit Button ----------------
if st.button("Run Resume Optimization 🚀"):
    if resume_text.strip() and jd_text.strip():
        st.success("Processing your resume and job description. Please wait...")

        # Create a wrapper function to handle async operations
        async def run_optimization():
            # Set the tone in memory before running the main pipeline
            await set_tone(user_id="default_user", tone=tone)
            # Run the main pipeline with tone passed
            await main(resume_text, jd_text, tone)

        # Run the async function
        try:
            asyncio.run(run_optimization())
            st.success("✅ Resume optimization completed!")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Please provide both resume and job description.")

# Display current selections in sidebar for reference
with st.sidebar:
    st.header("Current Selections")
    st.write(f"**Resume Input:** {resume_input_type}")
    st.write(f"**JD Input:** {jd_input_type}")
    st.write(f"**Tone:** {tone}")

    if resume_text:
        st.write(f"**Resume Length:** {len(resume_text)} characters")
    if jd_text:
        st.write(f"**JD Length:** {len(jd_text)} characters")
