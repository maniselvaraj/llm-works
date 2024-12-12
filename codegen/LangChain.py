import warnings
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from langchain_community.document_loaders import GithubFileLoader



os.environ["LANGCHAIN_TRACING_V2"] = "true"

open_ai_key = os.getenv("OPENAI_API_KEY")
#print(open_ai_key)

warnings.filterwarnings("ignore")


def simple_openai_call():
    llm = ChatOpenAI(api_key=os.environ["OPENAI_API_KEY"])
    #answer = llm.invoke("generate java method to check if string has unique characters. return the code alone")
    answer = llm.invoke("write a welcome email for a new hire")
    print(answer)


def advanced_openai_call():
    llm = ChatOpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = ChatPromptTemplate.from_messages([
        ("system", "you are a helpful ai based code generator"),
        ("user", "review the below java class and produce improved and efficient version of the same."),
        ("user", "return java code only"),
        ("user", "{input_java_class}"),
    ])
    chain = prompt | llm
    chain_result = chain.invoke({"input_java_class": "test"})
    print(chain_result)

def load_java_class():
   #print(os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"))
    loader = GithubFileLoader(
        repo="maniselvaraj/springboot-demo",  # the repo name
        branch="main",  # the branch name
        access_token=os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"),
        github_api_url="https://api.github.com",
        file_filter=lambda file_path: file_path.endswith(
            ".java"
        ),  # load all markdowns files.
    )
    documents = loader.load()
    print(documents)


load_java_class()