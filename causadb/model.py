import requests
import time
import pandas as pd
import numpy as np
from typing import Union

from .utils import get_causadb_url


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
            f"{get_causadb_url()}/models/{self.model_name}",
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
                f"{get_causadb_url()}/models/{self.model_name}",
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
                f"{get_causadb_url()}/models/{self.model_name}", headers=headers
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
                f"{get_causadb_url()}/models/{self.model_name}", headers=headers
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
                f"{get_causadb_url()}/models/{self.model_name}", headers=headers
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
                f"{get_causadb_url()}/models/{self.model_name}", headers=headers
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
                f"{get_causadb_url()}/models/{self.model_name}", headers=headers
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
                f"{get_causadb_url()}/models/{self.model_name}", headers=headers
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
                f"{get_causadb_url()}/models/{self.model_name}/attach/{data_name}",
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
                f"{get_causadb_url()}/models/{self.model_name}/detach",
                headers=headers
            ).json()
        except:
            raise Exception("CausaDB server request failed")

    def train(self, wait: bool = True, poll_interval: float = 0.2, poll_limit: float = 30) -> None:
        """Train the model.

        Args:
            wait (bool): Whether to wait for the model to finish training.
            poll_interval (float): The interval at which to poll the server for the model status.
            poll_limit (float): The maximum time to wait for the model to finish training.

        Example:
            >>> model.train()
        """
        headers = {"token": self.client.token_secret}

        try:
            response = requests.post(
                f"{get_causadb_url()}/models/{self.model_name}/train",
                headers=headers
            )
        except:
            raise Exception("CausaDB server request failed")

        # If HTTPException status code is 400, raise an exception
        if response.status_code == 400:
            raise Exception(response.json()["detail"])
        response = response.json()

        if wait:
            time_elapsed = 0
            while self.status() != "trained":
                time.sleep(poll_interval)
                # If the model takes too long to train, raise an exception
                time_elapsed += poll_interval
                if time_elapsed > poll_limit:
                    raise Exception("Model training took too long")

    def status(self) -> str:
        """Get the status of the model.

        Returns:
            str: The status of the model.
        """
        headers = {"token": self.client.token_secret}

        try:
            response = requests.get(
                f"{get_causadb_url()}/models/{self.model_name}",
                headers=headers,
            ).json()
        except:
            raise Exception("CausaDB server request failed")

        model_status = response["details"]["status"]

        return model_status

    def simulate_actions(self, actions: dict, fixed: dict = {}, interval: float = 0.9, observation_noise: bool = False) -> dict:
        """Simulate an action on the model.

        Args:
            actions (dict): A dictionary representing the actions.
            fixed (dict): A dictionary representing the fixed nodes.
            interval (float): The interval at which to simulate the action.
            observation_noise (bool): Whether to include observation noise.

        Returns:
            dict: A dictionary representing the result of the action.

        Example:
            >>> model.simulate_actions(
            ...     {"x": [0, 1]}
            ... )
        """
        headers = {"token": self.client.token_secret}

        query = {
            "actions": actions,
            "fixed": fixed,
            "interval": interval,
            "observation_noise": observation_noise
        }

        try:
            response = requests.post(
                f"{get_causadb_url()}/models/{self.model_name}/simulate-actions",
                headers=headers,
                json=query,
            ).json()
        except:
            raise Exception("CausaDB server request failed")

        if "outcome" in response:
            outcome = response["outcome"]
            return {
                "median": pd.DataFrame.from_dict(outcome["median"]),
                "lower": pd.DataFrame.from_dict(outcome["lower"]),
                "upper": pd.DataFrame.from_dict(outcome["upper"])
            }

        raise Exception("CausaDB server request failed")

    def causal_effects(self, actions: Union[str, dict[str, tuple[np.ndarray, np.ndarray]]], fixed: dict[str, np.ndarray] = None, interval: float = 0.90, observation_noise=False) -> pd.DataFrame:
        """ Get the causal effects of actions on the model.

        Args:
            actions (Union[str, dict[str, tuple[np.ndarray, np.ndarray]]]): A dictionary representing the actions.
            fixed (dict): A dictionary representing the fixed nodes.
            interval (float): The interval at which to simulate the action.
            observation_noise (bool): Whether to include observation noise.

        Returns:
            pd.DataFrame: A dataframe representing the causal effects of the actions.

        Example:
            >>> model.causal_effects(
            ...     {"x": [0, 1]}
            ... )

        """
        headers = {"token": self.client.token_secret}

        query = {
            "actions": actions,
            "fixed": fixed,
            "interval": interval,
            "observation_noise": observation_noise
        }

        try:
            response = requests.post(
                f"{get_causadb_url()}/models/{self.model_name}/causal-effects",
                headers=headers,
                json=query,
            ).json()
        except:
            raise Exception("CausaDB server request failed")

        if "outcome" in response:
            return pd.DataFrame.from_dict(response["outcome"])

        raise Exception("CausaDB server request failed")

    def find_best_actions(self, targets: dict[str, float], actionable: list[str], fixed: dict[str, float] = {}) -> dict:
        """Get the optimal actions for a given set of target outcomes.

        Args:
            targets (dict[str, float]): A dictionary representing the target outcomes.
            actionable (list[str]): A list of actionable nodes.
            fixed (dict[str, float]): A dictionary representing the fixed nodes.

        Returns:
            dict: A dictionary representing the optimal actions.

        Example:
            >>> model.optimal_actions(
            ...     {"x": 0.5},
            ...     ["x"],
            ...     {"y": 0.5}
        """
        headers = {"token": self.client.token_secret}

        query = {
            "targets": targets,
            "actionable": actionable,
            "fixed": fixed
        }

        try:
            response = requests.post(
                f"{get_causadb_url()}/models/{self.model_name}/find-best-actions",
                headers=headers,
                json=query,
            ).json()
        except:
            raise Exception("CausaDB server request failed")

        if "best_actions" in response:
            return pd.DataFrame.from_dict(response["best_actions"])

        raise Exception("CausaDB server request failed")

    def _update(self) -> None:
        """Pushes the current state of the model to the CausaDB server."""
        headers = {"token": self.client.token_secret}

        try:
            requests.post(
                f"{get_causadb_url()}/models/{self.model_name}",
                headers=headers,
                json=self.config
            ).json()
        except:
            raise Exception("CausaDB server request failed")
