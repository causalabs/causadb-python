import typer
from typing import Optional
import requests
import causadb.cli.account as account
import causadb.cli.data as data
import causadb.cli.models as models
from causadb.cli.utils import CAUSADB_URL
from causadb import __version__

app = typer.Typer()


def version_callback(value: bool):
    if value:
        typer.echo(f"CausaDB CLI v{__version__}")
        server_version = requests.get(
            f"{CAUSADB_URL}/version"
        ).json()["version"]
        typer.echo(f"CausaDB Server v{server_version}")

        raise typer.Exit()


@app.callback()
def cli(
        _: Optional[bool] = typer.Option(
            None, "-v", "--version", callback=version_callback, is_eager=True, help="Print the version of the CausaDB CLI"
        )
):
    ...


app.add_typer(account.app, name="account", help="Manage account")
app.add_typer(data.app, name="data", help="Manage linked datasources")
app.add_typer(models.app, name="models", help="Manage models")
