import typer
import causadb.cli.account as account
import causadb.cli.data as data
import causadb.cli.models as models

app = typer.Typer()
app.add_typer(account.app, name="account", help="Manage account")
app.add_typer(data.app, name="data", help="Manage linked datasources")
app.add_typer(models.app, name="models", help="Manage models")
