from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st

#Step 1 Instantiate the model
model_id = "codellama"
model = Ollama(model=model_id)


#Step 2 Create the prompt and generate code
def review_code(input_text: str):
    # Step 1: Prepare the  prompt
    prompt_template = """
    You are an advanced code generation model. Review below code and Generate more efficient method with documentation:

    {text}

    Generate more efficient method with documentation
    """
    prompt = ChatPromptTemplate.from_template(prompt_template)

    # Step 2: Inject the whole document into the prompt
    input_prompt = prompt.format(text=input_text)

    # Step 3: Generate the summary
    result = model(input_prompt)
    return result.strip()


#Step 3 Set up Streamlit
st.title("Code review with Code Llama:13b")
input_query = st.text_area("What do you want to review?", "")
if st.button("Review code"):
    with st.spinner("Reviewing code..."):
        mycode = review_code(input_query)
    st.subheader("Response")
    print(mycode)
    st.markdown(mycode)