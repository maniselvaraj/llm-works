#langchain github toolkit based pull request creator

import getpass
import os
from langchain_community.agent_toolkits.github.toolkit import GitHubToolkit
from langchain_community.utilities.github import GitHubAPIWrapper

from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, Tool
from langchain.prompts import ChatPromptTemplate

from utils import utc_time

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


def initialize_agent():
    llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful github assistant. Use the GitHubToolkit tool for command execution.",
            ),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )
    agent = create_tool_calling_agent(llm=llm,
                                      tools=tools,
                                      prompt=prompt)
    from langchain.agents import AgentExecutor
    # # Create an agent executor by passing in the agent and tools
    agent_exec = AgentExecutor.from_agent_and_tools(agent=agent,
                                                    tools=tools,
                                                    verbose=True)
    return agent_exec


def initialize_branch(agent_exec, branch_name):
    # Step 1: Create a new branch
    input_data = {"input": "Create a new branch named " + branch_name}  # Example input
    create_branch_response = agent_exec.invoke(input_data)
    print(create_branch_response)

def update_file(agent_exec, file_path, file_content_update):
    # Step 2: Update the file
    # print("="*80)
    # print(file_content_update)
    # print("=" * 80)
    input_data = {"input": "Update file " + file_path + " with the following content : \n" + file_content_update}
    update_file_response = agent_exec.invoke(input_data)
    print(update_file_response)

def create_pr(agent_exec, pull_request_title, branch_name, main_branch, pull_request_body = ""):
    # # Step 4: Create a pull request
    input_data = {
        "input": f"Create a pull request with the title {pull_request_title} from "
                 f"source branch {branch_name}  to target branch {main_branch} with the body {pull_request_body}"}
    create_pr_response = agent_exec.invoke(input_data)
    print(create_pr_response)


def pull_request_workflow():
    # llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0)
    # prompt = ChatPromptTemplate.from_messages(
    #     [
    #         (
    #             "system",
    #             "You are a helpful github assistant. Use the GitHubToolkit tool for command execution.",
    #         ),
    #         ("placeholder", "{chat_history}"),
    #         ("human", "{input}"),
    #         ("placeholder", "{agent_scratchpad}"),
    #     ]
    # )
    # agent = create_tool_calling_agent(llm=llm,
    #                                   tools=tools,
    #                                   prompt=prompt)
    # from langchain.agents import AgentExecutor
    # # # Create an agent executor by passing in the agent and tools
    # agent_exec = AgentExecutor.from_agent_and_tools(agent=agent,
    #                                                 tools=tools,
    #                                                 verbose=True)
    # Example usage
    # input_text = "What is the name of the current branch in the repository?"
    # input_data = {"input": "What is the name of the current branch in the repository?"}  # Example input
    # input_data = {"input": "Create branch called code_review based out of main branch"}  # Example input
    # output = agent_exec.invoke(input_data)
    # print(f"Output: {output}")
    agent_exec = initialize_agent()
    time = utc_time()
    branch_name = f"feature-branch-{time}"
    main_branch = "main"
    file_path = "README.adoc"  # File to be updated
    file_content_update = f"This is the updated content for the file. changing it using langchain {time}"
    commit_message = "Updated " + file_path + " with new content"
    pull_request_title = "Update " + file_path + " and README.md"
    pull_request_body = "This pull request updates " + file_path + " and README.md with new content."

    # Step 1: Create a new branch
    initialize_branch(agent_exec, branch_name)
    # input_data = {"input": "Create a new branch named " + branch_name}  # Example input
    # create_branch_response = agent_exec.invoke(input_data)
    # print(create_branch_response)

    # Step 2: Update the file
    # print("="*80)
    # print(file_content_update)
    # print("=" * 80)
    update_file(agent_exec, file_path, file_content_update)
    file_path = "README.md"
    update_file(agent_exec,  file_path, file_content_update)
    # input_data = {"input": "Update the file " + file_path + " with the following content : \n" + file_content_update}
    # update_file_response = agent_exec.invoke(input_data)
    # print(update_file_response)


    # # Step 3: Commit the changes
    # input_data = {"input": "Commit the changes"}  # Example input
    # commit_response = agent_exec.invoke(input_data)
    # print(commit_response)
    #

    create_pr(agent_exec, pull_request_title, branch_name, main_branch, pull_request_body)

    # # # Step 4: Create a pull request
    # input_data = {
    #     "input": f"Create a pull request with the title {pull_request_title} from source branch {branch_name}  to target branch {main_branch} with the body {pull_request_body}"}
    # create_pr_response = agent_exec.invoke(input_data)
    # print(create_pr_response)


pull_request_workflow()


