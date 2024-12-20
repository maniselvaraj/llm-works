#python method to fetch all java files from github repo
import os
from langchain_community.document_loaders import GithubFileLoader

def fetch_java_files(file_type="src/main"):
    # print(os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"))
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
    #print(documents)
    # Create the data structure while ignoring src/test paths
    java_files_data = [
        {
            'file_source': doc.metadata['source'],  # Java file path
            'file_path': doc.metadata['path'],
            'page_content': doc.page_content  # Corresponding file content
        }
        for doc in documents
        if doc.metadata['path'].endswith('.java') and doc.metadata['path'].startswith(file_type)
        # Ignore src/test paths
    ]
    return java_files_data


#fetch_java_files('/src/main')

