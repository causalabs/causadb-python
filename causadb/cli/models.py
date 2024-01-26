import typer
import requests
from causadb.cli.utils import load_config, show_table, CAUSADB_API_URL

app = typer.Typer()


@app.command()
def list():
    """
    List models.
    """
    config = load_config()
    token_secret = config["default"]["token_secret"]

    headers = {"token": token_secret}

    data = requests.get(
        f"{CAUSADB_API_URL}/models", headers=headers
    ).json()

    show_table(data["models"], columns=["id", "model_name", "created_at"])


@app.command()
def create():
    """
    Create a model.
    """

    typer.echo("Creating a model")


@app.command()
def delete():
    """
    Delete a model.
    """

    typer.echo("Deleting a model")


@app.command()
def view():
    """
    View a model.
    """

    typer.echo("Viewing a model")
