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
    response = client.set_token("bad-token-id", "bad-token-secret")
    assert response is False
    assert client.token_id == "test-token-id"
    assert client.token_secret == "test-token-secret"


def test_data_add(client):
    client \
        .add_data("test-data-2") \
        .from_csv("tests/test-data.csv")


def test_data_list(client):
    data_list = client.list_data()
    assert data_list is not None


def test_model_create(client):
    # Check that models can be created
    model = client.create_model("test-model")
    assert model is not None
    assert model.model_name == "test-model"
    assert model.client == client

    config = {
        "edges": [
            ["x", "y"],
            ["x", "z"],
            ["y", "z"]
        ],
        "nodes": ["x", "y", "z"],
        "node_types": {"x1": {"type": "seasonal", "min": 0, "max": 1}}
    }

    model._update_config(config)

    # data = client.create_data("test-data")
    # assert data is not None

    # data.from_csv("tests/test-data.csv")
    # assert type(data.columns) == list

    # model.set_edges([
    #     ("SaturatedFatsInDiet", "Weight"),
    #     ("Weight", "BMI"),
    # ])


def test_model_list(client):
    model_list = client.list_models()
    assert model_list is not None
    assert len(model_list) > 0
    assert "test-model" in [model.model_name for model in model_list]


def test_model_get(client):
    model = client.get_model("test-model")
    assert model is not None
    assert model.model_name == "test-model"
    assert model.client == client
