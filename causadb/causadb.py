import requests
import os
from .data import Data
from .model import Model
from .utils import CAUSADB_URL


class CausaDB:
    """CausaDB client class to interact with the CausaDB system.
    """

    def __repr__(self) -> str:
        return f"<CausaDB client>"

    def __str__(self) -> str:
        return f"{self.token_id}"

    def __init__(self) -> None:
        """Initializes the CausaDB client.

        Args:
            token_id (str): Token ID provided by CausaDB.
            token_secret (str): Token secret provided by CausaDB.
        """
        self.token_id = None
        self.token_secret = None

    def set_token(self, token_id: str, token_secret: str) -> bool:
        """Set the token for the CausaDB client.

        Args:
            token_id (str): Token ID provided by CausaDB.
            token_secret (str): Token secret provided by CausaDB.

        Returns:
            bool: True if the token is valid, False otherwise.
        """

        # Verify that the tokens are correct
        headers = {"token": token_secret}
        response = requests.get(
            f"{CAUSADB_URL}/account",
            headers=headers
        )

        # If the response is successful, set the tokens
        if response.status_code == 200:
            self.token_id = token_id
            self.token_secret = token_secret
            return True

        return False

    def create_model(self, model_name: str) -> Model:
        """Create a model and add it to the CausaDB system.

        Args:
            model_name (str): The name of the model.

        Returns:
            Model: The model object.
        """
        return Model(model_name, self)

    def get_model(self, model_name: str) -> Model:
        """Get a model by name.

        Args:
            model_name (str): The name of the model.

        Returns:
            Model: The model object.
        """
        return Model(model_name)

    def list_models(self) -> list[Model]:
        """List all models.

        Returns:
            list[Model]: A list of model objects.
        """
        headers = {"token": self.token_secret}

        response = requests.get(
            f"{CAUSADB_URL}/models", headers=headers
        ).json()

        print(response)

        return [Model("model1"), Model("model2")]

    def get_data(self, data_name: str) -> Data:
        """Get a data by name.

        Args:
            data_name (str): The name of the data.

        Returns:
            Data: The data object.
        """
        return Data(data_name)
