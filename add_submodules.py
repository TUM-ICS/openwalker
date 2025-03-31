import os
import subprocess
from github import Github

# GitHub API configuration
GITHUB_ORG = "TUM-ICS"
GITHUB_ACCESS_TOKEN = "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"

# Initialize GitHub API client
gh = Github(GITHUB_ACCESS_TOKEN)

def check_git_repo():
    """Ensure the script runs inside a Git repository."""
    if not os.path.isdir(".git"):
        print("Error: This script must be run inside a Git repository.")
        exit(1)

def ensure_src_directory():
    """Create 'src' directory if it doesn't exist."""
    os.makedirs("src", exist_ok=True)

def fetch_repositories():
    """Fetch all repositories from the GitHub organization and filter ones starting with 'ow_'."""
    org = gh.get_organization(GITHUB_ORG)
    repos = [repo.ssh_url for repo in org.get_repos() if repo.name.startswith("ow_")]
    
    if not repos:
        print("Error: No repositories found with prefix 'ow_'.")
        exit(1)
    
    return repos

def add_submodules(repos):
    """Add repositories as Git submodules in the 'src' directory."""
    for repo in repos:
        repo_name = os.path.basename(repo).replace(".git", "")
        if repo_name in ["ow_videos", "ow_docker"]:
            continue
        print(f"Adding submodule: {repo_name}")
        subprocess.run(["git", "submodule", "add", repo, f"src/{repo_name}"], check=True)
    
    subprocess.run(["git", "submodule", "update", "--init", "--recursive"], check=True)
    print("All submodules added successfully!")

if __name__ == "__main__":
    check_git_repo()
    ensure_src_directory()
    repositories = fetch_repositories()
    add_submodules(repositories)
