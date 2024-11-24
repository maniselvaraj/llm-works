# https://github.com/vashAI/ollama-llama3-financial-document-summarizer/blob/main/README.md


import streamlit as st
import PyPDF2
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
# pip install python-docx
from docx import Document


#initialize LLaMa via Ollama
model_id  = "llama3.5"
model = Ollama(model=model_id)

#extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in enumerate(reader.pages):
        text += reader.pages[page].extract_text()
    return text


'''
Summarize a given text using Llama3.2
'''
def summarize_text(input_text: str):
    #Step 1: Prepare the summarization prompt
    prompt_template = """
    You are an advanced summarization model. Summarize the following text:
    
    {text}
    
    Provide an information summary and extract action items
    """
    prompt = ChatPromptTemplate.from_template(prompt_template)

    #Step 2: Inject the whole document into the prompt
    input_prompt = prompt.format(text=input_text)

    #Step 3: Generate the summary
    result = model(input_prompt)
    return result.strip()


#Streamlit UI
# Run command:
# streamlit run summarize.py
st.title("Summarize with LLama 3.2")
uploaded_file = st.file_uploader("Choose a docx file", type="docx")
if uploaded_file is not None:
    doc = Document(uploaded_file)
    full_text = ""
    for para in doc.paragraphs:
        full_text += para.text

if st.button("Summarize text"):
    with st.spinner("Generating summary..."):
        summary = summarize_text(full_text)

    st.subheader("Summary")
    st.markdown(summary)


