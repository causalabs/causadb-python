import typer

app = typer.Typer()


@app.command()
def list():
    """
    List linked datasources.
    """
    typer.echo("Listing linked datasources")


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
