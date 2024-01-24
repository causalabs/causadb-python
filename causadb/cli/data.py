import typer
import requests
from causadb.cli.utils import load_config, show_table, CAUSADB_API_URL
import json

from rich.console import Console
from rich.table import Table

app = typer.Typer()


@app.command()
def list():
    """
    List linked datasources.
    """
    config = load_config()
    token_id = config["default"]["token_id"]
    token_secret = config["default"]["token_secret"]

    headers = {"token": token_secret}

    data = requests.get(
        f"{CAUSADB_API_URL}/cli/list-data", headers=headers
    ).json()

    show_table(data["data"], columns=["id", "name", "type"])


@app.command()
def link():
    """
    Link a datasource.
    """
    typer.echo("Linking a datasource")


@app.command()
def unlink():
    """
    Unlink a datasource.
    """
    typer.echo("Unlinking a datasource")
