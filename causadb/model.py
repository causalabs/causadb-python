import requests
from .utils import CAUSADB_URL


class Model:
    def __repr__(self) -> str:
        return f"<Model {self.model_name}>"

    def __init__(self, model_name: str, client: "CausaDB") -> None:
        """Initializes the Model class.

        Args:
            model_name (str): The name of the model.
            client (CausaDB): A CausaDB client.
        """
        self.model_name = model_name
        self.client = client

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
