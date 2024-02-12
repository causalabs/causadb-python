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


@task
def build_docs(c):
    """
    Build the documentation.
    """
    c.run("poetry run pydoc-markdown pydoc-markdown.yml")

    parse_markdown("build/docs/content/generated.md")
