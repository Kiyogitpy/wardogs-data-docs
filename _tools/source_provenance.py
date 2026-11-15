"""Read-only source tree provenance for generated data previews."""
import subprocess


def source_data_tree(root):
    """Return HEAD:data, marked dirty when the working data tree differs from HEAD."""
    try:
        rev = subprocess.run(
            ["git", "rev-parse", "--verify", "-q", "HEAD:data"], cwd=root,
            capture_output=True, text=True, check=False)
        if rev.returncode or not rev.stdout.strip():
            return None
        status = subprocess.run(
            ["git", "status", "--porcelain", "-z", "--untracked-files=all", "--", "data"], cwd=root,
            capture_output=True, check=False)
        if status.returncode:
            return None
        return rev.stdout.strip() + ("+dirty" if status.stdout else "")
    except (OSError, subprocess.SubprocessError):
        return None
