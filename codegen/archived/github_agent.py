#langchain github toolkit based pull request creator

import getpass
import os
from langchain_community.agent_toolkits.github.toolkit import GitHubToolkit
from langchain_community.utilities.github import GitHubAPIWrapper

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_tool_calling_agent, Tool
from langchain.prompts import ChatPromptTemplate

from utils import utc_time


def check_env():
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


def init_github():
    global tools
    # Define your GitHub token (Ensure this token has proper scopes for the operations you need)
    github_token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    # Initialize the GitHubAPIWrapper
    github = GitHubAPIWrapper(github_repository=os.getenv("GITHUB_REPOSITORY"),
                              github_app_id=os.getenv("GITHUB_APP_ID"))
    toolkit = GitHubToolkit.from_github_api_wrapper(github)
    tools = toolkit.get_tools()
    # Below was an important fix
    for tool in tools:
        tool.name = tool.mode
        print(tool.name)



def initialize_agent():
    llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0)
    #llm = ChatAnthropic(model="claude-3-opus-20240229", temperature=0)
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
    agent_exec = initialize_agent()
    time = utc_time()
    branch_name = f"feature-branch-{time}"
    main_branch = "main"
    file_path = "src/main/java/com/mani/llm/springboot/LLMMainController.java"  # File to be updated
    file_content_update = f"lorem ipsum dfdfd fdfdfd This is the updated content for the file. changing it using langchain {time}"
    commit_message = "Updated " + file_path + " with new content"
    pull_request_title = "Updating " + file_path
    pull_request_body = "This pull request updates " + file_path + " with new content."

    # Step 1: Create a new branch
    initialize_branch(agent_exec, branch_name)
    update_file(agent_exec, file_path, file_content_update)
    #file_path = "src/main/java/com/mani/llm/springboot/LLMMainController.java"
    #update_file(agent_exec,  file_path, file_content_update)
    create_pr(agent_exec, pull_request_title, branch_name, main_branch, pull_request_body)


def raise_pr(java_content_map):
    init_github()
    agent_exec = initialize_agent()
    time = utc_time()
    branch_name = f"feature-branch-{time}"
    main_branch = "main"
    pull_request_title = "Update Java files"
    pull_request_body = "This pull request updates Java files with new content."
    initialize_branch(agent_exec, branch_name)
    for file_path, file_content_update in java_content_map.items():
        print(">>>>Updating file : ", file_path)
        update_file(agent_exec, file_path, file_content_update)
    create_pr(agent_exec, pull_request_title, branch_name, main_branch, pull_request_body)



init_github()
pull_request_workflow()
