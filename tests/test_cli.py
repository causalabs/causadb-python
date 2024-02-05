from typer.testing import CliRunner
import time

from causadb.cli.main import app

runner = CliRunner()


def test_account_setup():
    result = runner.invoke(
        app, ["account", "setup"], input="test-token-id\ntest-token-secret\n")
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
        app, ["data", "add", "--data", "test", "--filepath", "tests/test-data.csv"])
    assert result.exit_code == 0
    assert "Successfully added data" in result.stdout


def test_models_add():
    result = runner.invoke(
        app, ["models", "add", "--model", "test", "--config", "tests/model-config.json"])

    assert result.exit_code == 0
    # assert "Successfully added model" in result.stdout


def test_models_attach():
    result = runner.invoke(
        app, ["models", "attach", "--model", "test", "--data", "test"])

    assert result.exit_code == 0
    # assert "Successfully attached data" in result.stdout


def test_models_info():
    result = runner.invoke(
        app, ["models", "info", "--model", "test"])
    assert result.exit_code == 0
    assert "id" in result.stdout


def test_models_train():
    result = runner.invoke(
        app, ["models", "train", "--model", "test"])

    assert result.exit_code == 0

    trained_status = False
    while not trained_status:
        result = runner.invoke(
            app, ["models", "status", "--model", "test"])
        if "trained" in result.stdout:
            trained_status = True
        time.sleep(1)

    assert result.exit_code == 0


def test_models_status():
    result = runner.invoke(
        app, ["models", "status", "--model", "test"])

    print(result.stdout)

    assert result.exit_code == 0


def test_models_simulate_action():
    result = runner.invoke(
        app, ["models", "simulate-action", "--model", "test", "--action", "tests/test-action.json"])

    print(result.stdout)

    assert result.exit_code == 0


def test_models_detach():
    result = runner.invoke(
        app, ["models", "detach", "--model", "test"])

    assert result.exit_code == 0
    # assert "Successfully detached data" in result.stdout


def test_data_remove():
    result = runner.invoke(app, ["data", "remove", "--data", "test"])
    assert result.exit_code == 0
    assert "Successfully removed data" in result.stdout


def test_models_remove():
    result = runner.invoke(app, ["models", "remove", "--model", "test"])
    assert result.exit_code == 0
    # assert "Successfully removed model" in result.stdout


def test_account_remove():
    result = runner.invoke(app, ["account", "remove"], input="y\n")
    assert result.exit_code == 0
    # assert "Successfully removed account" in result.stdout

    # Log back in
    result = runner.invoke(
        app, ["account", "setup"], input="test-token-id\ntest-token-secret\n")
