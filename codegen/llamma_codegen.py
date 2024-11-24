from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st

#Step 1 Instantiate the model
model_id = "codellama"
model = Ollama(model=model_id)


#Step 2 Create the prompt and generate code
def generate_code(input_text: str):
    # Step 1: Prepare the  prompt
    prompt_template = """
    You are an advanced code generation model. Generate Java code for following need:

    {text}

    Generate sufficient documentation for every method
    """
    prompt = ChatPromptTemplate.from_template(prompt_template)

    # Step 2: Inject the whole document into the prompt
    input_prompt = prompt.format(text=input_text)

    # Step 3: Generate the summary
    result = model(input_prompt)
    return result.strip()


#Step 3 Set up Streamlit
st.title("Code generation with Code Llama:13b")
input_query = st.text_input("What do you want to generate?", "")
if st.button("Generate code"):
    with st.spinner("Generating code..."):
        mycode = generate_code(input_query)
    st.subheader("Response")
    st.markdown(mycode)