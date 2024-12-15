import os
github_token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")  #"your-github-personal-access-token"
# Initialize the GitHubAPIWrapper
github_wrapper = GitHubAPIWrapper(github_access_token=github_token)

# Example usage: List repositories for the authenticated user
response = github_wrapper.run("list_repos")
print(response)