import typer
import requests
from causadb.cli.utils import load_config, show_table, CAUSADB_API_URL
from typing import Annotated
import json

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

    show_table(data["models"], columns=[
               "id", "name", "data", "created_at"])


@app.command()
def add(
    model_name_raw: Annotated[str, typer.Option(
        "--model",
        help="The name of your model, used for accessing it later.")] = None,
    model_config_filepath: Annotated[str, typer.Option(
        "--config",
        help="Path to a model config file (e.g. /path/to/config.json). See the docs for more information.")] = None
):
    """
    Create a model.
    """

    # If name is None, prompt the user for a name.
    if model_name_raw is None:
        model_name_raw = typer.prompt(
            "Enter the name of your model (e.g. my-model)")

    model_name = model_name_raw.replace(" ", "-")

    # Replace spaces with dashes.
    if " " in model_name_raw:
        typer.echo(
            f"Note: Spaces in model name replaced with dashes. Now model name: {model_name}.")

    # If model_config_filepath is None, prompt the user for a model_config_filepath file.
    if model_config_filepath is None:
        model_config_filepath = typer.prompt(
            "Enter the path to your model config file (e.g. /path/to/config.json)")

    # Read the config file into a dict.
    try:
        with open(model_config_filepath, "r") as f:
            try:
                model_config = json.load(f)
            except:
                typer.echo(
                    "Failed to read config file. Please check the file is valid JSON.")
                return 1
    except:
        typer.echo("Failed to read config file. Please check the path.")
        return 1

    config = load_config()
    token_secret = config["default"]["token_secret"]

    headers = {"token": token_secret}

    data = requests.post(
        f"{CAUSADB_API_URL}/models/{model_name}",
        headers=headers,
        json=model_config,
    ).json()

    typer.echo(data["message"])


@app.command()
def remove(
    model_name: Annotated[str, typer.Option(
        "--model",
        help="The name of the model you wish to remove.")] = None,
):
    """
    Delete a model.
    """
    # If name is None, prompt the user for a name.
    if model_name is None:
        model_name = typer.prompt(
            "Enter the name of the model you wish to remove (e.g. my-model)")

    # Make sure model_name can be used in an API URL.
    if " " in model_name:
        typer.echo(
            "Model name cannot contain spaces. Please try again.")
        return 1

    # Load the configuration and get the token secret
    config = load_config()
    token_secret = config["default"]["token_secret"]

    headers = {"token": token_secret}

    # Make a request to the remove data endpoint
    response = requests.delete(
        f"{CAUSADB_API_URL}/models/{model_name}",
        headers=headers
    ).json()

    typer.echo(response["message"])


@app.command()
def info(
    model_name: Annotated[str, typer.Option(
        "--model",
        help="The name of the model you wish to retrieve information about.")] = None
):
    """
    Show info about a model.
    """

    if model_name is None:
        model_name = typer.prompt(
            "Enter the name of the model you wish to attach data to (e.g. my-model)")

    config = load_config()
    token_secret = config["default"]["token_secret"]

    headers = {"token": token_secret}

    data = requests.get(
        f"{CAUSADB_API_URL}/models/{model_name}",
        headers=headers,
    ).json()

    # Pretty print the response
    typer.echo(json.dumps(data, indent=4))


@app.command()
def attach(
    model_name: Annotated[str, typer.Option(
        "--model",
        help="The name of the model you wish to attach data to.")] = None,
    data_name: Annotated[str, typer.Option(
        "--data",
        help="The name of the data you wish to attach.")] = None,
):
    """
    Attach data to a model.
    """

    if model_name is None:
        model_name = typer.prompt(
            "Enter the name of the model you wish to attach data to (e.g. my-model)")

    if data_name is None:
        data_name = typer.prompt(
            "Enter the name of the data you wish to attach (e.g. my-data)")

    config = load_config()
    token_secret = config["default"]["token_secret"]

    headers = {"token": token_secret}

    data = requests.post(
        f"{CAUSADB_API_URL}/models/{model_name}/attach/{data_name}",
        headers=headers,
    ).json()

    typer.echo(f"{data_name} successfully attached to {model_name}.")


@app.command()
def detach(
    model_name: Annotated[str, typer.Option(
        "--model",
        help="The name of the model you wish to attach data to.")] = None
):
    """
    Detach a datasource from a model.
    """

    if model_name is None:
        model_name = typer.prompt(
            "Enter the name of the model you wish to attach data to (e.g. my-model)")

    config = load_config()
    token_secret = config["default"]["token_secret"]

    headers = {"token": token_secret}

    data = requests.delete(
        f"{CAUSADB_API_URL}/models/{model_name}/detach",
        headers=headers,
    ).json()

    typer.echo("Data successfully detached from model.")


@app.command()
def train(
    model_name: Annotated[str, typer.Option(
        "--model",
        help="The name of the model you wish to train.")] = None
):
    """
    Train a model.
    """

    if model_name is None:
        model_name = typer.prompt(
            "Enter the name of the model you wish to train (e.g. my-model)")

    config = load_config()
    token_secret = config["default"]["token_secret"]

    headers = {"token": token_secret}

    data = requests.post(
        f"{CAUSADB_API_URL}/models/{model_name}/train",
        headers=headers,
    ).json()

    if data["status"] == "success":
        typer.echo(
            f"Model training started. Check the status with `causadb models info --model {model_name}`.")
    else:
        typer.echo("Model training failed. Check the logs for more information.")


@app.command()
def status(
    model_name: Annotated[str, typer.Option(
        "--model",
        help="The name of the model you wish to retrieve status for.")] = None
):
    """
    Show status of a model.
    """

    if model_name is None:
        model_name = typer.prompt(
            "Enter the name of the model you wish to attach data to (e.g. my-model)")

    config = load_config()
    token_secret = config["default"]["token_secret"]

    headers = {"token": token_secret}

    data = requests.get(
        f"{CAUSADB_API_URL}/models/{model_name}",
        headers=headers,
    ).json()

    model_status = data["details"]["status"]

    typer.echo(f"Model status: {model_status}")
