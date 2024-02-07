import requests
from .utils import CAUSADB_URL


class Model:
    def __init__(self, model_name: str, client: "CausaDB") -> None:
        """Initializes the Model class.

        Args:
            model_name (str): The name of the model.
            client (CausaDB): A CausaDB client.
        """
        self.model_name = model_name
        self.client = client
        self.config = {}

    def __repr__(self) -> str:
        return f"<Model {self.model_name}>"

    @staticmethod
    def from_json(model_spec: dict, client: "CausaDB") -> "Model":
        """Load a model from a JSON specification from the server.

        Args:
            model_spec (dict): The model specification.
            client (CausaDB): A CausaDB client.

        Returns:
            Model: The model object.
        """
        model = Model(model_spec["name"], client)
        model.config = model_spec["config"]

        return model

    def _update_config(self, config: dict) -> None:
        """Update the model with a new config.

        Args:
            config (dict): The new model configuration.
        """
        headers = {"token": self.client.token_secret}
        data = requests.post(
            f"{CAUSADB_URL}/models/{self.model_name}",
            headers=headers,
            json=config,
        ).json()
