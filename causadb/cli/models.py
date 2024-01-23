import typer

app = typer.Typer()


@app.command()
def list():
    """
    List models.
    """

    typer.echo("Listing models")


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
