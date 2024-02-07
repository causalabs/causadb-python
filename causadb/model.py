import requests
from .utils import CAUSADB_URL


class Model:
    def __init__(self, model_name: str, client: "CausaDB") -> None:
        """Initializes the Model class.

        Args:
            model_name (str): The name of the model.
            client (CausaDB): A CausaDB client.
        """
        self.client = client
        self.model_name = model_name
        self.config = {}

        self._update()

    def __repr__(self) -> str:
        return f"<Model {self.model_name}>"

    def remove(self) -> None:
        """Remove the model from the CausaDB system."""
        headers = {"token": self.client.token_secret}
        try:
            requests.delete(
                f"{CAUSADB_URL}/models/{self.model_name}",
                headers=headers,
            )
        except:
            raise Exception("CausaDB server request failed")

    def set_nodes(self, nodes: list[str]) -> None:
        """Set the nodes of the model.

        Args:
            nodes (list[str]): A list of node names.

        Example:
            >>> model.set_nodes(["x", "y", "z"])
        """
        headers = {"token": self.client.token_secret}

        try:
            response = requests.get(
                f"{CAUSADB_URL}/models/{self.model_name}", headers=headers
            ).json()
        except:
            raise Exception("CausaDB server request failed")

        self.config = response["details"]["config"]
        self.config["nodes"] = nodes

        self._update()

    def get_nodes(self) -> list[str]:
        """Get the nodes of the model.

        Returns:
            list[str]: A list of node names.
        """
        headers = {"token": self.client.token_secret}

        try:
            response = requests.get(
                f"{CAUSADB_URL}/models/{self.model_name}", headers=headers
            ).json()
        except:
            raise Exception("CausaDB server request failed")

        return response["details"]["config"]["nodes"]

    def set_edges(self, edges: list[tuple[str, str]]) -> None:
        """Set the edges of the model.

        Args:
            edges (list[tuple[str, str]]): A list of tuples representing edges.

        Example:
            >>> model.set_edges([
            ...     ("SaturatedFatsInDiet", "Weight"),
            ...     ("Weight", "BMI"),
            ... ])
        """
        headers = {"token": self.client.token_secret}

        try:
            response = requests.get(
                f"{CAUSADB_URL}/models/{self.model_name}", headers=headers
            ).json()
        except:
            raise Exception("CausaDB server request failed")

        self.config = response["details"]["config"]
        self.config["edges"] = edges

        self._update()

    def get_edges(self) -> list[tuple[str, str]]:
        """Get the edges of the model.

        Returns:
            list[tuple[str, str]]: A list of tuples representing edges.
        """
        headers = {"token": self.client.token_secret}

        try:
            response = requests.get(
                f"{CAUSADB_URL}/models/{self.model_name}", headers=headers
            ).json()
        except:
            raise Exception("CausaDB server request failed")

        edges = response["details"]["config"]["edges"]
        # Convert the edges to a list of tuples
        return [(edge[0], edge[1]) for edge in edges]

    def set_node_types(self, node_types: dict) -> None:
        """Set the node types of the model.

        Args:
            node_types (dict): A dictionary of node types.

        Example:
            >>> model.set_node_types({
            ...     "x1": {"type": "seasonal", "min": 0, "max": 1}
            ... })
        """
        headers = {"token": self.client.token_secret}

        try:
            response = requests.get(
                f"{CAUSADB_URL}/models/{self.model_name}", headers=headers
            ).json()
        except:
            raise Exception("CausaDB server request failed")

        self.config = response["details"]["config"]
        self.config["node_types"] = node_types

        self._update()

    def get_node_types(self) -> dict:
        """Get the node types of the model.

        Returns:
            dict: A dictionary of node types.
        """
        headers = {"token": self.client.token_secret}

        try:
            response = requests.get(
                f"{CAUSADB_URL}/models/{self.model_name}", headers=headers
            ).json()
        except:
            raise Exception("CausaDB server request failed")

        return response["details"]["config"]["node_types"]

    def _update(self) -> None:
        """Update the model with the latest data. Pushes the current state of the model to the CausaDB server."""
        headers = {"token": self.client.token_secret}

        try:
            response = requests.post(
                f"{CAUSADB_URL}/models/{self.model_name}",
                headers=headers,
                json=self.config
            ).json()
        except:
            raise Exception("CausaDB server request failed")
