import pytest
import causadb
from causadb import CausaDB, Model, Data
# Arbitrary test to check if the package is working


@pytest.fixture
def client():
    client = CausaDB()
    client.set_token("test-token-id", "test-token-secret")
    return client


def test_package():
    # Check version exists and is in semver format
    assert causadb.__version__ is not None
    assert len(causadb.__version__.split(".")) == 3


def test_client_initialization(client):
    # Check that the client is initialized
    assert client is not None

    assert client.token_id == "test-token-id"
    assert client.token_secret == "test-token-secret"


def test_bad_tokens(client):
    # Check that bad tokens are rejected
    with pytest.raises(Exception):
        response = client.set_token("bad-token-id", "bad-token-secret")
    assert client.token_id == "test-token-id"
    assert client.token_secret == "test-token-secret"


def test_data_add(client):
    client \
        .add_data("test-data-2") \
        .from_csv("tests/test-data.csv")


def test_data_list(client):
    data_list = client.list_data()
    assert data_list is not None
    assert len(data_list) > 0


def test_model_create(client):
    # Check that models can be created
    model = client.create_model("test-model-12345")
    assert model is not None
    assert model.model_name == "test-model-12345"
    assert model.client == client


def test_set_nodes(client):
    model = client.get_model("test-model-12345")
    model.set_nodes(["x", "y", "z"])
    nodes = model.get_nodes()
    assert "x" in nodes
    assert len(nodes) == 3


def test_set_edges(client):
    model = client.get_model("test-model-12345")
    model.set_edges([
        ("SaturatedFatsInDiet", "Weight"),
        ("Weight", "BMI"),
    ])
    edges = model.get_edges()
    assert ("SaturatedFatsInDiet", "Weight") in edges
    assert len(edges) == 2


def test_set_node_types(client):
    model = client.get_model("test-model-12345")
    model.set_node_types({
        "x": "continuous",
        "y": "continuous",
        "z": "continuous",
    })
    node_types = model.get_node_types()
    assert node_types["x"] == "continuous"
    assert len(node_types) == 3


def test_model_list(client):
    model_list = client.list_models()
    assert model_list is not None
    assert len(model_list) > 0
    assert "test-model-12345" in [model.model_name for model in model_list]


def test_model_get(client):
    model = client.get_model("test-model-12345")
    assert model is not None
    assert model.model_name == "test-model-12345"
    assert model.client == client


def test_model_remove(client):
    model = client \
        .get_model("test-model-12345") \
        .remove()
    model_list = client.list_models()
    assert "test-model-12345" not in [model.model_name for model in model_list]
