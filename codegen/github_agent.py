#langchain github toolkit based pull request creator

import getpass
import os
from langchain_community.agent_toolkits.github.toolkit import GitHubToolkit
from langchain_community.utilities.github import GitHubAPIWrapper

from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, Tool
from langchain.prompts import ChatPromptTemplate


for env_var in [
    "GITHUB_APP_ID",
    "GITHUB_APP_PRIVATE_KEY",
    "GITHUB_REPOSITORY",
]:
    if not os.getenv(env_var):
        os.environ[env_var] = getpass.getpass()

for env_var in [
    "GITHUB_APP_ID",
    "GITHUB_APP_PRIVATE_KEY",
    "GITHUB_REPOSITORY",
]:
    print(os.getenv(env_var))

# Define your GitHub token (Ensure this token has proper scopes for the operations you need)
github_token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
# Initialize the GitHubAPIWrapper
github = GitHubAPIWrapper(github_repository=os.getenv("GITHUB_REPOSITORY"),
                            github_app_id=os.getenv("GITHUB_APP_ID"))
toolkit = GitHubToolkit.from_github_api_wrapper(github)
tools = toolkit.get_tools()

# from langchain_openai import ChatOpenAI
# from langgraph.prebuilt import create_react_agent
# # Select example tool
# tools = [tool for tool in toolkit.get_tools() if tool.name == "Get Issue"]
# assert len(tools) == 1
# tools[0].name = "get_issue"
# llm = ChatOpenAI(model="gpt-4o-mini")
# agent_executor = create_react_agent(llm, tools)
# example_query = "What is the title of issue 24888?"
# events = agent_executor.stream(    {"messages": [("user", example_query)]},    stream_mode="values",)for event in events:    event["messages"][-1].pretty_print()


#Below was an important fix
for tool in tools:
    tool.name = tool.mode
    print(tool.name)


llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful github assistant. Make sure to use the GitHubToolkit tool for command execution.",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# prompt = ChatPromptTemplate.from_messages([
#     {"role": "system", "content": "You are a helpful assistant specialized in managing GitHub repositories and answering developer queries."},
#     {"role": "user", "content": "{input}"}
# ])

# Step 4: Create tools to support GitHub-related actions
# Add specific tools to allow functionality like listing issues, creating pull requests, etc.
# github_tools = [
#     Tool(
#         name="List GitHub Issues",
#         func=toolkit.list_issues,
#         description="Lists issues in a GitHub repository."
#     ),
#     Tool(
#         name="Create GitHub Issue",
#         func=toolkit.create_issue,
#         description="Creates a new issue in a GitHub repository."
#     ),
#     Tool(
#         name="Get Repository Details",
#         func=toolkit.get_repo,
#         description="Fetches details about a specific repository."
#     )
# ]

agent = create_tool_calling_agent(llm=llm,
                                  tools=tools,
                                  prompt=prompt)
from langchain.agents import AgentExecutor
# # Create an agent executor by passing in the agent and tools
agent_exec = AgentExecutor.from_agent_and_tools(agent=agent,
                                               tools=tools,
                                               verbose=True)

# Example usage
#input_text = "What is the name of the current branch in the repository?"
#input_data = {"input": "What is the name of the current branch in the repository?"}  # Example input
#input_data = {"input": "Create branch called code_review based out of main branch"}  # Example input

# output = agent_exec.invoke(input_data)
# print(f"Output: {output}")

branch_name = "new-feature-branch4"
file_path = "README.adoc"  # File to be updated
file_content_update = "This is the updated content for the file. changing it using langchain\n"
commit_message = "Updated " + file_path + " with new content"
pull_request_title = "Update " + file_path
pull_request_body = "This pull request updates " + file_path + " with new content."

# Step 1: Create a new branch
input_data = {"input": "Create a new branch named " + branch_name}  # Example input
create_branch_response = agent_exec.invoke(input_data)
print(create_branch_response)

# Step 2: Update the file
input_data = {"input": "Update the file " + file_path + " with the following content : \n" + file_content_update}
update_file_response = agent_exec.invoke(input_data)
print(update_file_response)

# Step 3: Commit the changes
input_data = {"input": "Commit the changes with message committed"}  # Example input
commit_response = agent_exec.invoke(input_data)
print(commit_response)

# Step 4: Create a pull request
input_data = {"input": "Create a pull request with the title " + pull_request_title + " and from source branch " + branch_name + " to target branch main with the body " + pull_request_body }
create_pr_response = agent_exec.invoke(input_data)
print(create_pr_response)


