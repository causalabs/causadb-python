import pytest
from dotenv import load_dotenv
import os
import causadb
import pandas as pd
from causadb import CausaDB, Model, Data

load_dotenv()

CAUSADB_TOKEN = os.getenv("CAUSADB_TOKEN")


@pytest.fixture
def client():
    client = CausaDB()
    client.set_token(CAUSADB_TOKEN)
    return client


@pytest.fixture
def model_trained(client):
    model = client.create_model("test-model-12345")

    model.set_nodes(["x", "y", "z"])
    model.set_edges([
        ("x", "y"),
        ("y", "z"),
    ])

    data = {
        "x": [1.01, 2.03, 2.98, 4.01, 5.0001],
        "y": [2.1, 3.9, 6.2, 7.6, 9.6],
        "z": [1.1, 2.1, 2.9, 4.3, 4.7],
    }

    df = pd.DataFrame(data)

    client.add_data("test-data-12345").from_pandas(df)

    model.attach("test-data-12345")

    model.train("test-data-12345")

    return model


@pytest.fixture
def model_untrained(client):
    # Create a new model
    model = client.create_model("test-model-untrained")

    # Define nodes and edges
    model.set_nodes(["x", "y", "z"])
    model.set_edges([
        ("x", "y"),
        ("y", "z"),
    ])

    return model


def test_model_train_missing_data(client):
    # Create a new model
    model = client.create_model("test-model-missing-data")

    # Define nodes and edges
    model.set_nodes(["x", "y", "z"])
    model.set_edges([
        ("x", "y"),
        ("y", "z"),
    ])

    # Generate data with missing values
    data = {
        "x": [1, 2, 3, None, 5],
        "y": [1, None, 3, 4, 5],
        "z": [None, 2, 3, 4, 5],
    }
    df = pd.DataFrame(data)

    # Add data to CausaDB
    with pytest.raises(Exception):
        client.add_data("test-data-missing").from_pandas(df)


def test_model_train_non_numeric_data(client):
    # Create a new model
    model = client.create_model("test-model-non-numeric-data")

    # Define nodes and edges
    model.set_nodes(["x", "y", "z"])
    model.set_edges([
        ("x", "y"),
        ("y", "z"),
    ])

    # Generate data with non-numeric values
    data = {
        "x": [1, 2, 3, "a", 5],
        "y": [1, "b", 3, 4, 5],
        "z": ["c", 2, 3, 4, 5],
    }
    df = pd.DataFrame(data)

    # Add data to CausaDB
    with pytest.raises(Exception):
        client.add_data("test-data-non-numeric").from_pandas(df)


def test_model_train_wrong_node_types(client):
    # Create a new model
    model = client.create_model("test-model-wrong-node-types")

    # Define nodes and edges
    model.set_nodes(["x", "y", "z"])
    model.set_edges([
        ("x", "y"),
        ("y", "z"),
    ])
    model.set_node_types({
        "x": "continuous",
        "y": "binary",
        "z": "continuous",
    })

    # Generate data with wrong node types
    data = {
        "x": [1, 2, 3, 4, 5],
        "y": [0, 1, 3, 1, 0],
        "z": [1.1, 2.2, 3.3, 4.4, 5.5],
    }

    df = pd.DataFrame(data)

    # Add data to CausaDB
    client.add_data("test-data-wrong-node-types").from_pandas(df)

    # Train the model
    with pytest.raises(Exception):
        model.train("test-data-wrong-node-types")


def test_model_simulate_actions_wrong_types(model_trained):
    with pytest.raises(Exception):
        model_trained.simulate_actions(1)


def test_model_structure_invalid(client):
    # Create a new model
    model = client.create_model("test-model-invalid-structure")

    # Define nodes and edges
    model.set_nodes(["x", "y", "z"])
    model.set_edges([
        ("x", "y"),
        ("y", "z"),
        ("z", "x"),  # This creates a cycle, which is not valid
    ])

    # Add data to the model
    data = {
        "x": [1, 2, 3, 4, 5],
        "y": [2, 3, 4, 5, 6],
        "z": [3, 4, 5, 6, 7],
    }
    df = pd.DataFrame(data)

    client.add_data("test-data-invalid-structure").from_pandas(df)

    # Try to train the model, check it raises an exception mentioning the cycle

    with pytest.raises(Exception) as excinfo:
        model.train("test-data-invalid-structure")

    assert "cycles" in str(excinfo.value)


def test_invalid_token():
    # Try to create a client with an invalid token
    with pytest.raises(Exception) as excinfo:
        client = CausaDB()
        client.set_token("invalid-token")
    assert "token" in str(excinfo.value)


def test_find_best_actions_target_upstream(client, model_trained):
    # Try to find the best actions with a target that is upstream from the action
    with pytest.raises(Exception) as excinfo:
        model_trained.find_best_actions(targets={"x": 0}, actionable=["y"])
    assert "causal pathway" in str(excinfo.value)


def test_simulate_actions_untrained_model(model_untrained):
    # Try to simulate actions without training the model
    with pytest.raises(Exception) as excinfo:
        model_untrained.simulate_actions({"x": 0})
    assert "not trained" in str(excinfo.value)


def test_causal_effects_untrained_model(model_untrained):
    # Try to get causal effects without training the model
    with pytest.raises(Exception) as excinfo:
        model_untrained.causal_effects({"x": [0, 1]})
    assert "not trained" in str(excinfo.value)


def test_causal_attributions_untrained_model(model_untrained):
    # Try to get causal attributions without training the model
    with pytest.raises(Exception) as excinfo:
        model_untrained.causal_attributions("z")
    assert "not trained" in str(excinfo.value)


def test_find_best_actions_untrained_model(model_untrained):
    # Try to find best actions without training the model
    with pytest.raises(Exception) as excinfo:
        model_untrained.find_best_actions({"y": 0.5}, ["x"], {"z": 0.5})
    assert "not trained" in str(excinfo.value)
