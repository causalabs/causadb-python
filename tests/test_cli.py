from typer.testing import CliRunner

from causadb.cli.main import app

runner = CliRunner()


def test_account_setup():
    result = runner.invoke(
        app, ["account", "setup"], input="ct-LZj5EvCgMAxYuo07vxR4LbGcfo4Ydo3u\ncs-WGVTHQTFQ8HTHLogYrX31dyy9FK8ijFt\n")
    assert result.exit_code == 0
    assert "Setup successful" in result.stdout


def test_data_list():
    result = runner.invoke(app, ["data", "list"])
    assert result.exit_code == 0
    assert "id" in result.stdout


def test_models_list():
    result = runner.invoke(app, ["models", "list"])
    assert result.exit_code == 0
    assert "id" in result.stdout


def test_data_add():
    result = runner.invoke(
        app, ["data", "add", "--name", "test", "--filepath", "tests/test-data.csv"])
    assert result.exit_code == 0
    assert "Successfully added data" in result.stdout


def test_models_add():
    result = runner.invoke(
        app, ["models", "add", "--name", "test", "--config", "tests/model-config.json"])
    assert result.exit_code == 0
    # assert "Successfully added model" in result.stdout


def test_data_remove():
    result = runner.invoke(app, ["data", "remove", "--name", "test"])
    assert result.exit_code == 0
    assert "Successfully removed data" in result.stdout


def test_models_remove():
    result = runner.invoke(app, ["models", "remove", "--name", "test"])
    assert result.exit_code == 0
    # assert "Successfully removed model" in result.stdout


def test_account_remove():
    result = runner.invoke(app, ["account", "remove"], input="y\n")
    assert result.exit_code == 0
    # assert "Successfully removed account" in result.stdout

    # Log back in
    result = runner.invoke(
        app, ["account", "setup"], input="ct-LZj5EvCgMAxYuo07vxR4LbGcfo4Ydo3u\ncs-WGVTHQTFQ8HTHLogYrX31dyy9FK8ijFt\n")
