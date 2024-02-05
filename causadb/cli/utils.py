import os
import dotenv
import toml
from rich.console import Console
from rich.table import Table
dotenv.load_dotenv()


CAUSADB_API_URL = os.getenv("CAUSADB_API_URL", "https://api.causadb.com/v1")


def load_config():
    # Get config from ~/.causadb/config.toml
    dir_name = os.path.expanduser("~/.causadb")
    config_filepath = os.path.join(dir_name, "config.toml")

    if not os.path.exists(config_filepath):
        return None

    with open(config_filepath, "r") as f:
        config = toml.load(f)

    return config


def show_table(data, columns=None):
    table = Table(show_header=True, header_style="bold turquoise4")

    if columns is None:
        columns = list(data[0].keys())

    for column in columns:
        table.add_column(column)

    for item in data:
        table.add_row(*[str(item[column]) for column in columns])

    console = Console()
    console.print(table)
