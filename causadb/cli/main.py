import typer

app = typer.Typer()


@app.callback()
def callback():
    """
    Build, manage, and use causal models on CausaDB
    """


@app.command()
def shoot():
    """
    Shoot the portal gun
    """
    typer.echo("Shooting portal gun")


@app.command()
def load():
    """
    Load the portal gun
    """
    typer.echo("Loading portal gun")
