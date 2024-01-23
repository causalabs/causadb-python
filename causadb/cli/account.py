import typer
import click
import requests
import toml
import os
import causadb.cli.utils as utils

CAUSADB_API_URL = utils.CAUSADB_API_URL

app = typer.Typer()


@app.command()
def setup():
    """
    Set up a CausaDB account on this device
    """
    org_id = typer.prompt("Organization ID", default="causa-test")
    token = typer.prompt("Token", default="12345")

    data = requests.post(
        f"{CAUSADB_API_URL}/cli/verify-org",
        json={"org_id": org_id, "token": token},
    )

    if data.status_code == 200:
        typer.echo(
            "Setup successful, saving credentials to ~/.causadb/config.toml.")

        # Save the token to ~/.causadb/config.toml. If the file doesn't exist, create it.
        dir_name = os.path.expanduser("~/.causadb")
        config_filepath = os.path.join(dir_name, "config.toml")

        config = {}
        if os.path.exists(config_filepath):
            with open(config_filepath, "r") as f:
                config = toml.load(f)

        profile_name = org_id + ":" + data.json()["token_name"]

        config[profile_name] = {
            "org_id": org_id,
            "token": token,
        }

        with open(config_filepath, "w") as f:
            toml.dump(config, f)

    else:
        typer.echo("Setup failed, please check your credentials and try again.")


@app.command()
def remove():
    """
    Remove CausaDB account from this device
    """
    # Get config from ~/.causadb/config.toml
    dir_name = os.path.expanduser("~/.causadb")
    config_filepath = os.path.join(dir_name, "config.toml")

    if not os.path.exists(config_filepath):
        typer.echo(
            "No profiles found in ~/.causadb/config.toml.")
        return 1

    # Confirm removal
    confirm = typer.confirm(
        f"Are you sure you want to remove your account from this device? (The account will not be deleted from the cloud.)")

    if confirm:
        # Delete the token from ~/.causadb/config.toml.

        with open(config_filepath, "w") as f:
            toml.dump({}, f)

        typer.echo(
            f"Account successfully removed from this device. You can add it again with `causadb account setup`.")


@app.command()
def info():
    """
    Show information about the account
    """
    # Get config from ~/.causadb/config.toml
    dir_name = os.path.expanduser("~/.causadb")
    config_filepath = os.path.join(dir_name, "config.toml")

    if not os.path.exists(config_filepath):
        typer.echo(
            "No config found in ~/.causadb/config.toml.")
        return 1

    # Get the token from ~/.causadb/config.toml.
    with open(config_filepath, "r") as f:
        config = toml.load(f)

    org_id = config[list(config.keys())[0]]["org_id"]
    token = config[list(config.keys())[0]]["token"]

    typer.echo(f"Organization ID: {org_id}")
    typer.echo(f"Token: {token}")
