# References: https://github.com/meta-llama/llama-recipes
import os
from langchain_community.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate
import tiktoken
from langchain.chains.summarize import load_summarize_chain
import textwrap
from time import monotonic




#load the file
with open( os.getcwd() + "/../data/ent_arch.chap5.txt") as f:
    source_text = f.read()

model_name = "llama3.2"
text_splitter = CharacterTextSplitter.from_tiktoken_encoder (model_name=model_name)
texts = text_splitter.split_text(source_text)
docs = [Document(page_content=t) for t in texts]
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name=model_name)


prompt_template = """write a summary using bullet points of the following:
{text}"""
prompt = PromptTemplate(template=prompt_template, input_variables=["text"])


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


num_tokens = num_tokens_from_string(source_text, model_name)
print("Number of tokens " + str(num_tokens))
gpt35_turbo_max_tokens = 4097
verbose = True
if num_tokens < gpt35_turbo_max_tokens:
    chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt, verbose=verbose)
else:
    chain = load_summarize_chain(llm, chain_type="map_reduce", map_prompt=prompt, combine_prompt=prompt, verbose=verbose)

start_time = monotonic()
summary = chain.run(docs)

#print(f"Chain type: {chain.__class__.__name__}")
#print(f"Run time: {monotonic() - start_time}")
print(f"Summary: {textwrap.fill(summary, width=100)}")