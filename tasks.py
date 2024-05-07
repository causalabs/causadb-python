from invoke import task
import os
import re
from tqdm import tqdm


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


@task
def migrate_node(c):
    """
    Migrate the node to the new version.
    """
    from openai import OpenAI
    client = OpenAI()

    # Load all the .py files in the causadb directory and form a single prompt
    python_codebase = ""
    for root, dirs, files in os.walk("causadb"):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file), 'r') as f:
                    # Add the file name to the prompt
                    python_codebase += f"Filename: {file}\n"
                    python_codebase += "```python\n"
                    python_codebase += f.read()
                    python_codebase += "\n```\n\n"

    # Load existing Node.js codebase that needs to be updated based on the Python code
    node_codebase = ""
    for root, dirs, files in os.walk("../causadb-node/src"):
        for file in files:
            if file.endswith(".ts"):
                with open(os.path.join(root, file), 'r') as f:
                    # Add the file name to the prompt
                    node_codebase += f"Filename: {file}\n"
                    node_codebase += "```typescript\n"
                    node_codebase += f.read()
                    node_codebase += "\n```\n\n"

    user_prompt = f"""
    === Up to date Python codebase ===
    {python_codebase}

    === Existing Node.js codebase ===
    {node_codebase}
    """

    # Define a prompt for converting the Python code to Node.js
    system_prompt = """
    You are a Python to Node.js code converter. Convert the following Python codebase to Node.js. 
    The Python codebase is up to date, and the Node.js codebase is out of date.
    Your task is to bring the Node.js codebase up to date with the Python codebase.
    Keep the code structure and comments the same, unless they are specific to Python syntax or there is a mistake in the code.
    Use TypeScript syntax. Use the existing Node.js codebase as a reference.
    Produce the Node.js codebase in full, including all files and their contents.
    I have an existing Node.js codebase that you should update based on the Python code.
    The Node.js codebase is provided in the prompt under the "=== Existing Node.js codebase ===" section.
    The Python codebase is provided in the prompt under the "=== Up to date Python codebase ===" section.
    Don't include Python-specific comments, code, or files in the output. (e.g. no __init__.py files, etc)
    I will be using a parser to convert your code to actual files. Please ensure that your output and code is correct and complete.
    I'll be checking git diffs to see what you've changed, so make sure to keep the changes clean and organized.
    Include the entire Node.js codebase in the output, including all files and their contents. Even if the file has not changed, include it in the output.
    Don't add any extra information in the output, as I need a clean output so I can easily parse it.
    Use modern Node.js features and best practices where applicable.
    Files should be named the same as the Python files, but with a .ts extension. They
    should be encoded as Filename: <filename>.ts., and the code should be enclosed in triple backticks, as follows:
    Filename: <filename>.ts
    ```typescript
    <code here>
    ```
    Keep to this format for each file in the codebase.
    """

    print(user_prompt)

    print("Generating response...")

    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        stream=True
    )

    existing_lines = node_codebase.count("\n")

    pbar = tqdm(total=existing_lines)

    line_count = 0
    response = ""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            response += chunk.choices[0].delta.content
            new_lines = chunk.choices[0].delta.content.count("\n")
            line_count += new_lines
            pbar.update(new_lines)

    pbar.close()

    print("Response generated. Saving to file...")

    # Save the response to a file
    with open("migrate_node_response.txt", 'w') as f:
        f.write(response)

    print("Response saved to migrate_node_response.txt")


@task
def convert_node_to_codebase(c):
    with open("migrate_node_response.txt", 'r') as f:
        response = f.read()

    # # Split the response into sections based on the file names
    # sections = response.split("Filename: ")

    # # Remove the first empty section
    # sections = sections[1:]

    # Create the causadb-node directory if it doesn't exist
    # if not os.path.exists("../causadb-node"):
    #     os.makedirs("../causadb-node")

    # # Create the src directory if it doesn't exist
    # if not os.path.exists("../causadb-node/src"):
    #     os.makedirs("../causadb-node/src")

    if not os.path.exists("test_node_output"):
        os.makedirs("test_node_output")

    # # Write the sections to files
    # for section in sections:
    #     # Split the section into the filename and the code
    #     lines = section.split("\n")
    #     filename = lines[0].strip()
    #     code = "\n".join(lines[2:])

    #     # Write the code to the file
    #     with open(f"../causadb-node/src/{filename}", 'w') as f:
    #         f.write(code)

    import re
    pattern = r'Filename: ([^\.]+\.ts)\s*```typescript\s*([^`]+)```'
    matches = re.findall(pattern, response, re.DOTALL)

    for filename, code in matches:
        print(f"Filename: {filename}")
        print("Code:")
        print(code)
        print("-" * 40)

    print("Node.js codebase written to causadb-node/src directory")
