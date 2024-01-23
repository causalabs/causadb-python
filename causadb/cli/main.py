import typer
import requests
import toml
import os

import causadb.cli.data as data
import causadb.cli.models as models

app = typer.Typer()
app.add_typer(data.app, name="data", help="Manage linked datasources")
app.add_typer(models.app, name="models", help="Manage models")


@app.command()
def login():
    """
    Log in to the CausaDB cloud on this device
    """
    org_id = typer.prompt("Organization ID", default="causa-test")
    token = typer.prompt("Token", default="12345")

    data = requests.post(
        "http://localhost:8000/cli/verify-org",
        json={"org_id": org_id, "token": token},
    )

    if data.status_code == 200:
        typer.echo(
            "Login successful, saving credentials to ~/.causadb/config.toml.")

        # Save the token to ~/.causadb/config.toml. If the file doesn't exist, create it.
        dir_name = os.path.expanduser("~/.causadb")
        file_path = os.path.join(dir_name, "config.toml")

        config = {}
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                config = toml.load(f)

        token_name = "default"
        config[token_name] = {
            "org_id": org_id,
            "token": token,
        }

        with open(file_path, "w") as f:
            toml.dump(config, f)

    else:
        typer.echo("Login failed, please check your credentials and try again.")


@app.command()
def logout():
    """
    Log out of the CausaDB cloud on this device
    """
    typer.echo("Logging out")


@app.command()
def info():
    """
    Show information about the current user
    """
    typer.echo("Showing user info")
