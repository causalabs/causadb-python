import typer
import requests
from causadb.cli.utils import load_config, show_table, CAUSADB_API_URL
import pandas as pd
from typing import Annotated

app = typer.Typer()


@app.command()
def list():
    """
    List linked datasources.
    """
    config = load_config()
    token_secret = config["default"]["token_secret"]

    headers = {"token": token_secret}

    data = requests.get(
        f"{CAUSADB_API_URL}/data", headers=headers
    ).json()

    show_table(data["data"], columns=["id", "name", "type"])


@app.command()
def add(
    filepath: Annotated[str, typer.Option(
        help="The path to your data file.")] = None,
    name: Annotated[str, typer.Option(
        "--data",
        help="The name to give your new data source.")] = None
):
    """
    Add a datasource.
    """

    # If filepath is None, prompt the user for a filepath.
    if filepath is None:
        typer.echo(
            "Note: We only support CSV files at the moment, but more formats will be supported soon.")
        filepath = typer.prompt(
            "Enter the path to your datasource file (e.g. /path/to/file.csv)")

    # Read the file into a pandas dataframe.
    try:
        dataset = pd.read_csv(filepath).to_dict()
    except:
        typer.echo("Failed to read file.")
        return 1

    # If dataset name is None, prompt the user for a name.
    data_name = name
    if data_name is None:
        default_name = filepath.split("/")[-1].split(".")[0]

        data_name = typer.prompt(
            "Enter a name for your datasource", default=default_name)

    config = load_config()
    token_secret = config["default"]["token_secret"]

    headers = {"token": token_secret}

    data = requests.post(
        f"{CAUSADB_API_URL}/data/{data_name}",
        headers=headers,
        json=dataset,
    ).json()

    if data["status"] == "success":
        typer.echo("Successfully added datasource.")

    else:
        typer.echo("Failed to add datasource.")


@app.command()
def remove(
    name: Annotated[str, typer.Option(
        "--data",
        help="Name of the data source you want to remove.")] = None
):
    """
    Remove a datasource.
    """

    if name is None:
        # Prompt the user for the name of the datasource to remove
        name = typer.prompt(
            "Enter the name of the datasource you want to remove")

    # Load the configuration and get the token secret
    config = load_config()
    token_secret = config["default"]["token_secret"]

    headers = {"token": token_secret}

    # Make a request to the remove data endpoint
    response = requests.delete(
        f"{CAUSADB_API_URL}/data/{name}",
        headers=headers
    )

    # Check the response status and print appropriate message
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "success":
            typer.echo("Successfully removed datasource.")
        else:
            typer.echo(f"Failed to remove datasource: {data['message']}")
    else:
        typer.echo(
            f"Failed to remove datasource. Server responded with status code {response.status_code}.")
