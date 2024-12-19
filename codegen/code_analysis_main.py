import warnings
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from github_loader import fetch_java_files
from utils import save_contents

os.environ["LANGCHAIN_TRACING_V2"] = "false"
open_ai_key = os.getenv("OPENAI_API_KEY")
warnings.filterwarnings("ignore")


def advanced_openai_call(source_code):
    llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))
    prompt = ChatPromptTemplate.from_messages([
        ("system", "you are a helpful ai based code generator"),
        ("user", "review the below java class and produce improved and efficient version of the same."),
        ("user", "generate method comments for improved code"),
        ("user", "return java code only"),
        ("user", "{input_java_class}"),
    ])
    chain = prompt | llm
    chain_result = chain.invoke({"input_java_class": source_code})
    return chain_result


def main():
    #get list of java files
    java_files = fetch_java_files('src/main')

    #iterate through each file and hit LLM
    for java_file in java_files:
        print("Processing file:" + java_file['file_source'])
        source_code = java_file['page_content'].split('\n')[1:-1]
        improved_code = advanced_openai_call(source_code)
        print('=' * 80)
        print(improved_code.content)
        save_contents(improved_code.content, java_file['file_source'] )
        print('*' * 80)

main()