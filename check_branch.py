import os
import subprocess


def get_current_branch():
    """Get the current branch name."""
    try:
        # Run the git command to get the current branch name
        branch_name = subprocess.check_output(['git', 'branch', '--show-current'], stderr=subprocess.STDOUT)
        return branch_name.decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        print(f"Error fetching current branch: {e.output.decode('utf-8')}")
        return None


def get_last_commit():
    """Get the details of the last commit."""
    try:
        # Run the git log command to get the last commit details
        commit_details = subprocess.check_output(
            ['git', 'log', '-1', '--pretty=format:%H%n%an%n%ar%n%s'], stderr=subprocess.STDOUT
        )
        # Decode and split the output into parts
        commit_hash, author, timestamp, message = commit_details.decode('utf-8').strip().split('\n')
        return {
            "hash": commit_hash,
            "author": author,
            "timestamp": timestamp,
            "message": message
        }
    except subprocess.CalledProcessError as e:
        print(f"Error fetching last commit: {e.output.decode('utf-8')}")
        return None


if __name__ == "__main__":
    # Check if the current directory is a Git repository
    if not os.path.exists('.git'):
        print("Error: This is not a Git repository.")
    else:
        # Get the current branch
        current_branch = get_current_branch()
        if current_branch:
            print(f"You are currently on branch: {current_branch}")
        else:
            print("Unable to determine the current branch.")

        # Get the last commit details
        last_commit = get_last_commit()
        if last_commit:
            print("\nLast Commit Details:")
            print(f"  Commit Hash: {last_commit['hash']}")
            print(f"  Author: {last_commit['author']}")
            print(f"  Timestamp: {last_commit['timestamp']}")
            print(f"  Message: {last_commit['message']}")
        else:
            print("Unable to fetch the last commit details.")
