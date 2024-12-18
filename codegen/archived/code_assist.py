#from langchain_community.llms.ollama import Ollama

#pip install -U langchain-ollama
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st
from langchain.load.dump import dumps


#Step 1 Instantiate the model
model_id = "codellama"
model = OllamaLLM(model=model_id)
print(model)


#Step 2 Create the prompt and generate code
def code_assist(input_task: str, input_code: str):
    # Step 1: Prepare the  prompt
    prompt_template = """
    You are an advanced code generation model. 
    {prompt_task}
    {payload}
    """
    prompt = ChatPromptTemplate.from_template(prompt_template)
    # Step 2: Inject the whole document into the prompt
    input_prompt = prompt.format(prompt_task=input_task, payload=input_code)
    print(input_prompt)
    # Step 3: Generate the output
    print(model)
    result = model(input_prompt)
    return result.strip()


def code_assist_json(task: str, code_snippet: str):
    chat_template = ChatPromptTemplate.from_messages([
        ("system", "You are an advanced code generation model"),
        ("user", "{requested_task}"),
        ("user", "generate 2 unit tests to test the new method that you generated"),
        ("user", "{code_block}")
    ])
    messages = chat_template.format_messages(requested_task=task, code_block=code_snippet)
    print(messages)
    print(model)
    result = model(dumps(messages))
    return result.strip()


#Step 3 Set up Streamlit
st.title("Code assist with Code Llama:13b")
input_task = st.text_input("What do you want to do?", "")
input_code = st.text_area("Paste the code here", "")
if st.button("Run code assist task"):
    with st.spinner("Performing task: " + input_task):
        mycode = code_assist_json(input_task, input_code)
    st.subheader("Response")
    print(mycode)
    st.markdown(mycode)