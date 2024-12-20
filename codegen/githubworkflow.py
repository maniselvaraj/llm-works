from datetime import datetime

import requests
import base64

import os

# Replace these with your repository details and access token
GITHUB_TOKEN = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
OWNER = "maniselvaraj"
REPO = "springboot-demo"
BASE_BRANCH = "main"
FILE_PATH = "src/main/java/com/mani/llm/springboot/Application.java"
COMMIT_MESSAGE = "Update code in file"
PR_BODY = "This PR updates the file with new features."

# GitHub API base URL
GITHUB_API_URL = "https://api.github.com"

# Headers for authentication
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

def utc_time():
    # Get the current date and time
    current_time = datetime.now()
    # Format the datetime in YYYY-MM-DD-HH-MIN-SS format
    formatted_time = current_time.strftime("%Y%m%d-%H%M%S")
    # Print the formatted datetime
    print("Formatted datetime:", formatted_time)
    return formatted_time

current_time = utc_time()
NEW_BRANCH = "new-feature-branch-" + current_time
PR_TITLE = "New Feature Update at " + current_time

def get_branch_sha(branch_name):
    """Fetch the SHA of the branch."""
    url = f"{GITHUB_API_URL}/repos/{OWNER}/{REPO}/git/ref/heads/{branch_name}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()["object"]["sha"]

def create_branch(base_sha, branch_name):
    """Create a new branch from the base SHA."""
    url = f"{GITHUB_API_URL}/repos/{OWNER}/{REPO}/git/refs"
    data = {
        "ref": f"refs/heads/{branch_name}",
        "sha": base_sha
    }
    response = requests.post(url, json=data, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def update_file(branch_name, file_path, content):
    """Update the file with new content."""
    url = f"{GITHUB_API_URL}/repos/{OWNER}/{REPO}/contents/{file_path}"
    # Get the file's current SHA
    response = requests.get(url, headers=HEADERS, params={"ref": branch_name})
    response.raise_for_status()
    file_sha = response.json()["sha"]

    # Update the file content
    new_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    data = {
        "message": COMMIT_MESSAGE,
        "content": new_content,
        "sha": file_sha,
        "branch": branch_name
    }
    response = requests.put(url, json=data, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def create_pull_request(branch_name):
    """Create a pull request."""
    url = f"{GITHUB_API_URL}/repos/{OWNER}/{REPO}/pulls"
    data = {
        "title": PR_TITLE,
        "body": PR_BODY,
        "head": branch_name,
        "base": BASE_BRANCH
    }
    response = requests.post(url, json=data, headers=HEADERS)
    response.raise_for_status()
    return response.json()

# def main():
#     try:
#         # Step 1: Get the SHA of the base branch
#         base_sha = get_branch_sha(BASE_BRANCH)
#         print(f"Base branch SHA: {base_sha}")
#
#         # Step 2: Create a new branch
#         create_branch(base_sha, NEW_BRANCH)
#         print(f"Created branch: {NEW_BRANCH}")
#
#         # Step 3: Update the file
#         new_content = "This is the updated content of the file."
#         update_file(NEW_BRANCH, FILE_PATH, new_content)
#         print(f"Updated file: {FILE_PATH}")
#
#         # Step 4: Create a pull request
#         pr = create_pull_request(NEW_BRANCH)
#         print(f"Pull request created: {pr['html_url']}")
#
#     except requests.exceptions.RequestException as e:
#         print(f"An error occurred: {e}")

def raise_pr(java_content_map):
    try:
        # Step 1: Get the SHA of the base branch
        base_sha = get_branch_sha(BASE_BRANCH)
        print(f"Base branch SHA: {base_sha}")

        # Step 2: Create a new branch
        create_branch(base_sha, NEW_BRANCH)
        print(f"Created branch: {NEW_BRANCH}")

        # Step 3: Update the files
        for file_path, file_content_update in java_content_map.items():
            print(">>>>Updating file : ", file_path)
            update_file(NEW_BRANCH, file_path, file_content_update)

        # new_content = "This is the updated content of the file."
        # update_file(NEW_BRANCH, FILE_PATH, new_content)
        # print(f"Updated file: {FILE_PATH}")

        # Step 4: Create a pull request
        pr = create_pull_request(NEW_BRANCH)
        print(f"Pull request created: {pr['html_url']}")
        return pr['html_url']
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

