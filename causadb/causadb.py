import requests
import os
import toml
from .data import Data
from .model import Model
from .utils import get_causadb_url, set_causadb_url


class CausaDB:
    """CausaDB client class to interact with the CausaDB system.
    """

    def __repr__(self) -> str:
        return f"<CausaDB client>"

    def __str__(self) -> str:
        return "CausaDB client"

    def __init__(self, token: str = None, custom_url: str = None) -> None:
        """Initializes the CausaDB client.

        Args:
            custom_url (str, optional): The URL of the CausaDB server. For custom deployments or development purposes. Defaults to None.
        """
        # If the token is not provided, try to load it from the config file
        if token is None:
            token = self._load_token()

        # If we now have a token, set it. If not, the user will have to use set_token.
        if token is not None:
            self.set_token(token)

        # If a custom URL is provided, set it
        if custom_url is not None:
            set_causadb_url(custom_url)

    def _load_token(self) -> str:
        """Load the token from the config file.

        Returns:
            str: The token secret.
        """
        dir_name = os.path.expanduser("~/.causadb")
        config_filepath = os.path.join(dir_name, "config.toml")

        if not os.path.exists(config_filepath):
            raise Exception("No token found")

        with open(config_filepath, "r") as f:
            config = toml.load(f)

        token_secret = config \
            .get("default", {}) \
            .get("token_secret", None)

        return token_secret

    def set_token(self, token: str) -> None:
        """Set the token for the CausaDB client.

        Args:
            token (str): Token secret provided by CausaDB.

        Raises:
            Exception: If the token is invalid.
        """

        # Verify that the tokens are correct
        headers = {"token": token}
        response = requests.get(
            f"{get_causadb_url()}/account",
            headers=headers
        )

        # If the response is successful, set the tokens
        if response.status_code == 200:
            self.token = token
        else:
            raise Exception("Invalid token")

    def create_model(self, model_name: str) -> Model:
        """Create a model and add it to the CausaDB system.

        Args:
            model_name (str): The name of the model.

        Returns:
            Model: The model object.
        """
        return Model(model_name, self)

    def add_data(self, data_name: str) -> Data:
        """Add data to the CausaDB system.

        Args:
            data_name (str): The name of the data.

        Returns:
            Data: The data object.
        """
        return Data(data_name, self)

    def get_model(self, model_name: str) -> Model:
        """Get a model by name.

        Args:
            model_name (str): The name of the model.

        Returns:
            Model: The model object.
        """
        headers = {"token": self.token}

        try:
            response = requests.get(
                f"{get_causadb_url()}/models/{model_name}", headers=headers
            ).json()
        except:
            raise Exception("CausaDB server request failed")

        # If the model exists, return it
        model = Model(model_name, self)

        return model

    def list_models(self) -> list[Model]:
        """List all models.

        Returns:
            list[Model]: A list of model objects.
        """
        headers = {"token": self.token}

        try:
            response = requests.get(
                f"{get_causadb_url()}/models", headers=headers
            ).json()
        except:
            raise Exception("CausaDB server request failed")

        model_list = []
        for model_spec in response.get("models", []):
            model = Model(model_spec["name"], self)
            model_list.append(model)

        return model_list

    def get_data(self, data_name: str) -> Data:
        """Get a data by name.

        Args:
            data_name (str): The name of the data.

        Returns:
            Data: The data object.
        """
        headers = {"token": self.token}
        try:
            response = requests.get(
                f"{get_causadb_url()}/data/{data_name}", headers=headers
            ).json()
        except:
            raise Exception("CausaDB server request failed")

        data = Data(data_name, self)

        return data

    def list_data(self) -> list[Data]:
        """List all data.

        Returns:
            list[Data]: A list of data objects.
        """
        headers = {"token": self.token}

        try:
            response = requests.get(
                f"{get_causadb_url()}/data", headers=headers
            ).json()
        except:
            raise Exception("CausaDB client failed to connect to server")

        data_list = []
        for data_spec in response.get("data", []):
            data = Data(data_spec["name"], self)
            data_list.append(data)

        return data_list
