from invoke import task
import os
import re


@task
def sync_version_py(c):
    # Set causadb.__version__ to the version in pyproject.toml
    with open("pyproject.toml", "r") as f:
        for line in f:
            if "version" in line:
                version = line.split("=")[1].strip().strip('"')
                break

    with open("causadb/__version__.py", "w") as f:
        f.write(f"__version__ = '{version}'\n")


def parse_markdown(file_path):
    current_h2_dir = None
    current_h4_file = None
    current_content = []

    def write_content():
        if current_h4_file and current_content:
            with open(f"docs/{current_h4_file}", 'w', encoding='utf-8') as f:
                f.writelines(current_content)
            current_content.clear()

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Make MDX3 compatible by escaping curly braces
            line = line.replace("{", "\{").replace("}", "\}")
            # Replace __init__ with "init" in H2 titles
            line = re.sub(r'\\_\\_init\\_\\_', 'Constructor', line)

            if line.startswith('## '):  # H2 header
                write_content()  # Write content of the previous H4 section if exists
                current_h2_dir = line.strip('# ').strip()
                # Remove the word "Objects" from the H2 title
                current_h2_dir = current_h2_dir.replace("Objects", "")
                # Strip leading and trailing whitespaces
                current_h2_dir = current_h2_dir.strip()
                os.makedirs(f"docs/{current_h2_dir}", exist_ok=True)
                current_h4_file = None  # Reset current H4 file as we're now in a new H2 section
            elif line.startswith('#### '):  # H4 header
                write_content()  # Write content of the previous H4 section
                h4_title = line.strip('# ').strip()
                # Sanitize title to make it a valid filename
                h4_filename = re.sub(r'[\\/*?:"<>|]', "", h4_title) + '.md'
                if current_h2_dir:
                    current_h4_file = os.path.join(
                        current_h2_dir, h4_filename)
                else:
                    print(
                        "H4 header found without preceding H2 header, skipping:", line)

                # Replace __init__ with "Constructor" in H4 titles
                h4_title = re.sub(r'__init__', 'Constructor', h4_title)

                # Change to H1 header, replace \_ with space
                h4_title = h4_title.replace("\_", " ")

                # Uppercase the first letter of each word in H4 titles
                h4_title = h4_title.title()

                # Uppercase "CSV" in H4 titles
                h4_title = re.sub(r'Csv', 'CSV', h4_title)

                # Convert H4 title to H1
                current_content.append(f"# {h4_title}\n")
            else:
                current_content.append(line)

        write_content()  # Write content for the last section


def parse_markdown_cli(file_path):
    # Load the markdown from filepath
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()

    # Split the content into sections based on any header
    sections = []
    current_section = []
    for line in content:
        if line.startswith("#"):
            if current_section:
                sections.append(current_section)
                current_section = []
        # If the line is a header, convert it to H1 and remove backticks
        if line.startswith("#"):
            line = f"# {line.strip('# ')}"
            # if the line isn't just causadb, remove causadb from the line
            if line != "# causadb":
                line = line.replace("causadb ", "")
        current_section.append(line)
    sections.append(current_section)

    # Write the content to separate files
    for section in sections:
        if len(section) > 1:
            h1 = section[0].strip("# ").strip()
            h1 = h1.replace(" ", "_")
            h1 = h1.lower()
            h1 = h1.replace("objects", "")
            h1 = h1.strip()
            h1 = h1.replace("__init__", "constructor")
            h1 = h1.replace("`", "")

            with open(f"cli_docs/{h1}.md", 'w', encoding='utf-8') as f:
                f.writelines(section)


@task
def build_docs(c):
    """
    Build the documentation.
    """
    c.run("poetry run pydoc-markdown pydoc-markdown.yml")

    parse_markdown("build/docs/content/generated.md")


@task
def build_cli_docs(c):
    """
    Build the CLI documentation.
    """
    c.run("poetry run typer causadb/cli/main.py utils docs --name causadb --output cli_docs.md")

    if not os.path.exists("cli_docs"):
        os.makedirs("cli_docs")

    parse_markdown_cli("cli_docs.md")

    # Clean up the markdown file
    os.remove("cli_docs.md")
