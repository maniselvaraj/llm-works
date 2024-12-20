#streamlit based portal to accept a github repo url, show progress of code analysis and show status
import streamlit as st

from code_analysis_main import analyze_code

#streamlit based portal to accept a github repo url, show progress of code analysis and show status

def launch_ui():
    """
    Launches the Streamlit UI for accepting a GitHub repository URL.
    """
    st.title("Brownfield Java Code Analyzer")
    github_url = st.text_input("Enter the GitHub Repository URL:", "maniselvaraj/springboot-demo")
    if st.button("Start Analysis"):
        if github_url:
            st.write(f"Analyzing repository: {github_url}")
            analyze_code()


if __name__ == "__main__":
    launch_ui()
