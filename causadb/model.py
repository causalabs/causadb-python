import requests
import time
import pandas as pd

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

        # Pull config from the server
        headers = {"token": self.client.token_secret}
        response = requests.get(
            f"{CAUSADB_URL}/models/{self.model_name}",
            headers=headers,
        ).json()

        if "details" in response:
            self.config = response["details"]["config"]

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

    def attach(self, data_name: str) -> None:
        """Attach data to the model.

        Args:
            data_name (str): The name of the data to attach.
        """
        headers = {"token": self.client.token_secret}

        try:
            response = requests.post(
                f"{CAUSADB_URL}/models/{self.model_name}/attach/{data_name}",
                headers=headers
            ).json()
        except:
            raise Exception("CausaDB server request failed")

    def detach(self, data_name: str) -> None:
        """Detach data from the model.

        Args:
            data_name (str): The name of the data to detach.
        """
        headers = {"token": self.client.token_secret}

        try:
            response = requests.delete(
                f"{CAUSADB_URL}/models/{self.model_name}/detach",
                headers=headers
            ).json()
        except:
            raise Exception("CausaDB server request failed")

    def train(self, wait=True, poll_interval=0.2) -> None:
        """Train the model.

        Args:
            wait (bool): Whether to wait for the model to finish training.
            poll_interval (float): The interval at which to poll the server for the model status.

        Example:
            >>> model.train()
        """
        headers = {"token": self.client.token_secret}

        try:
            response = requests.post(
                f"{CAUSADB_URL}/models/{self.model_name}/train",
                headers=headers
            )
        except:
            raise Exception("CausaDB server request failed")

        # If HTTPException status code is 400, raise an exception
        if response.status_code == 400:
            raise Exception(response.json()["detail"])
        response = response.json()

        if wait:
            while self.status() != "trained":
                # Try again in 200ms
                time.sleep(poll_interval)

    def status(self) -> str:
        """Get the status of the model.

        Returns:
            str: The status of the model.
        """
        headers = {"token": self.client.token_secret}

        try:
            response = requests.get(
                f"{CAUSADB_URL}/models/{self.model_name}",
                headers=headers,
            ).json()
        except:
            raise Exception("CausaDB server request failed")

        model_status = response["details"]["status"]

        return model_status

    def simulate_action(self, action: dict) -> dict:
        """Simulate an action on the model.

        Args:
            action (dict): A dictionary representing the action.

        Returns:
            dict: A dictionary representing the result of the action.
        """
        headers = {"token": self.client.token_secret}

        try:
            response = requests.post(
                f"{CAUSADB_URL}/models/{self.model_name}/simulate-action",
                headers=headers,
                json=action,
            ).json()
        except:
            raise Exception("CausaDB server request failed")

        if "outcome" in response:
            return response["outcome"]

        raise Exception("CausaDB server request failed")

    def _update(self) -> None:
        """Pushes the current state of the model to the CausaDB server."""
        headers = {"token": self.client.token_secret}

        try:
            response = requests.post(
                f"{CAUSADB_URL}/models/{self.model_name}",
                headers=headers,
                json=self.config
            ).json()
        except:
            raise Exception("CausaDB server request failed")
