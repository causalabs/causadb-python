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
