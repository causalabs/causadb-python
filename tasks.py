from invoke import task


@task
def increment_version_number(c):
    """
    Increment the build number in _version.py by 1. Used for CI/CD.
    """
    # Task implementation goes here
    from causadb._version import major, minor, patch
    new_patch = patch + 1

    # Get SHA of commit and comment on the same line to trigger merge conflicts if necessary.
    commit_sha = c.run("git rev-parse HEAD", hide=True).stdout.strip()

    # Update build number in _version.py
    with open("causadb/_version.py", "w") as f:
        f.write("# Reset to -1 for new minor/major version\n")
        f.write(f"major = {major}\n")
        f.write(f"minor = {minor}\n")
        f.write(f"patch = {new_patch}  # {commit_sha}\n")

    # Use poetry version to update the version in pyproject.toml
    c.run(f"poetry version {major}.{minor}.{new_patch}")
