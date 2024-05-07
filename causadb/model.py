import requests
import time
import pandas as pd
import numpy as np
from typing import Union
from pydantic import validate_call

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
        headers = {"token": self.client.token}
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
        headers = {"token": self.client.token}
        try:
            requests.delete(
                f"{get_causadb_url()}/models/{self.model_name}",
                headers=headers,
            )
        except Exception as e:
            raise Exception(f"CausaDB server request failed: {e}")

    @validate_call
    def set_nodes(self, nodes: list[str]) -> None:
        """Set the nodes of the model.

        Args:
            nodes (list[str]): A list of node names.

        Example:
            >>> model.set_nodes(["x", "y", "z"])
        """
        headers = {"token": self.client.token}

        try:
            response = requests.get(
                f"{get_causadb_url()}/models/{self.model_name}", headers=headers
            ).json()
        except Exception as e:
            raise Exception(f"CausaDB server request failed: {e}")

        self.config = response["details"]["config"]
        self.config["nodes"] = nodes

        self._update()

    def get_nodes(self) -> list[str]:
        """Get the nodes of the model.

        Returns:
            list[str]: A list of node names.
        """
        headers = {"token": self.client.token}

        try:
            response = requests.get(
                f"{get_causadb_url()}/models/{self.model_name}", headers=headers
            ).json()
        except Exception as e:
            raise Exception(f"CausaDB server request failed: {e}")

        return response["details"]["config"]["nodes"]

    @validate_call
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
        headers = {"token": self.client.token}

        try:
            response = requests.get(
                f"{get_causadb_url()}/models/{self.model_name}", headers=headers
            ).json()
        except Exception as e:
            raise Exception(f"CausaDB server request failed: {e}")

        self.config = response["details"]["config"]
        self.config["edges"] = edges

        self._update()

    def get_edges(self) -> list[tuple[str, str]]:
        """Get the edges of the model.

        Returns:
            list[tuple[str, str]]: A list of tuples representing edges.
        """
        headers = {"token": self.client.token}

        try:
            response = requests.get(
                f"{get_causadb_url()}/models/{self.model_name}", headers=headers
            ).json()
        except Exception as e:
            raise Exception(f"CausaDB server request failed: {e}")

        edges = response["details"]["config"]["edges"]
        # Convert the edges to a list of tuples
        return [(edge[0], edge[1]) for edge in edges]

    @validate_call
    def set_node_types(self, node_types: dict) -> None:
        """Set the node types of the model.

        Args:
            node_types (dict): A dictionary of node types.

        Example:
            >>> model.set_node_types({
            ...     "x1": {"type": "seasonal", "min": 0, "max": 1}
            ... })
        """
        headers = {"token": self.client.token}

        try:
            response = requests.get(
                f"{get_causadb_url()}/models/{self.model_name}", headers=headers
            ).json()
        except Exception as e:
            raise Exception(f"CausaDB server request failed: {e}")

        self.config = response["details"]["config"]
        self.config["node_types"] = node_types

        self._update()

    @validate_call
    def get_node_types(self) -> dict:
        """Get the node types of the model.

        Returns:
            dict: A dictionary of node types.
        """
        headers = {"token": self.client.token}

        try:
            response = requests.get(
                f"{get_causadb_url()}/models/{self.model_name}", headers=headers
            ).json()
        except Exception as e:
            raise Exception(f"CausaDB server request failed: {e}")

        return response["details"]["config"]["node_types"]

    @validate_call
    def attach(self, data_name: str) -> None:
        """Attach data to the model.

        Args:
            data_name (str): The name of the data to attach.
        """
        headers = {"token": self.client.token}

        try:
            response = requests.post(
                f"{get_causadb_url()}/models/{self.model_name}/attach/{data_name}",
                headers=headers
            ).json()
        except Exception as e:
            raise Exception(f"CausaDB server request failed: {e}")

    @validate_call
    def detach(self, data_name: str) -> None:
        """Detach data from the model.

        Args:
            data_name (str): The name of the data to detach.
        """
        headers = {"token": self.client.token}

        try:
            response = requests.delete(
                f"{get_causadb_url()}/models/{self.model_name}/detach",
                headers=headers
            ).json()
        except Exception as e:
            raise Exception(f"CausaDB server request failed: {e}")

    @validate_call
    def train(self, data_name: str = None, wait: bool = True, poll_interval: float = 0.2, poll_limit: float = 30.0, verbose: bool = False, progress_interval: float = 1.0) -> None:
        """Train the model.

        Args:
            wait (bool): Whether to wait for the model to finish training.
            poll_interval (float): The interval at which to poll the server for the model status.
            poll_limit (float): The maximum time to wait for the model to finish training.
            verbose (bool): Whether to display model progress.
            progress_interval (float): The interval at which to display the model progress.

        Example:
            >>> model.train()
        """

        # If data_name is provided, attach the data to the model
        if data_name:
            self.attach(data_name)

        headers = {"token": self.client.token}

        try:
            response = requests.post(
                f"{get_causadb_url()}/models/{self.model_name}/train",
                headers=headers
            )
        except Exception as e:
            raise Exception(f"CausaDB server request failed: {e}")

        # If HTTPException status code is 400, raise an exception
        if response.status_code == 400:
            raise Exception(response.json()["detail"])
        response = response.json()

        if wait:
            time_elapsed = 0
            last_progress = 0
            if verbose:
                print(f"Training model...")
            while self.status() != "trained":
                time.sleep(poll_interval)
                time_elapsed += poll_interval

                if verbose and time_elapsed - last_progress >= progress_interval:
                    # Display model training time elapsed time_elapsed
                    print(f"Training model... ({round(time_elapsed)}s)")
                    last_progress = time_elapsed

                if time_elapsed > poll_limit:
                    raise Exception(
                        "Model training took too long. Waiting time exceeded but the model is still training.")
            if verbose:
                print(f"Model training progress: {self.status()}")

    def status(self) -> str:
        """Get the status of the model.

        Returns:
            str: The status of the model.
        """
        headers = {"token": self.client.token}

        try:
            response = requests.get(
                f"{get_causadb_url()}/models/{self.model_name}",
                headers=headers,
            ).json()
        except Exception as e:
            raise Exception(f"CausaDB server request failed: {e}")

        model_status = response["details"]["status"]

        return model_status

    @validate_call
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
        headers = {"token": self.client.token}

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
            )
        except Exception as e:
            raise Exception(f"CausaDB server request failed: {e}")

        if response.status_code != 200:
            raise Exception(response.json()["detail"])

        response = response.json()

        if "outcome" in response:
            outcome = response["outcome"]
            return {
                "median": pd.DataFrame.from_dict(outcome["median"]),
                "lower": pd.DataFrame.from_dict(outcome["lower"]),
                "upper": pd.DataFrame.from_dict(outcome["upper"])
            }

        raise Exception("CausaDB server request failed - unexpected response.")

    @validate_call
    def causal_effects(self, actions: Union[str, dict[str, tuple[float, float]]], fixed: dict[str, float] = None, interval: float = 0.90, observation_noise=False) -> pd.DataFrame:
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
        headers = {"token": self.client.token}

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
            )
        except Exception as e:
            raise Exception(f"CausaDB server request failed: {e}")

        if response.status_code != 200:
            raise Exception(response.json()["detail"])

        response = response.json()

        if "outcome" in response:
            return pd.DataFrame.from_dict(response["outcome"])

        raise Exception("CausaDB server request failed - unexpected response.")

    # @validate_call
    def find_best_actions(self, targets: dict[str, float], actionable: list[str], fixed: dict[str, list[float]] = {},
                          constraints: dict[str, tuple] = {}, data: pd.DataFrame = None, target_importance: dict[str, float] = {}) -> pd.DataFrame:
        """Get the optimal actions for a given set of target outcomes.

        Args:
            targets (dict[str, float]): A dictionary representing the target outcomes.
            actionable (list[str]): A list of actionable nodes.
            fixed (dict[str, float]): A dictionary representing the fixed nodes.
            constraints (dict[str, tuple]): A dictionary representing the constraints.
            data (pd.DataFrame): A dataframe representing the data.
            target_importance (dict[str, float]): A dictionary representing the target importance.

        Returns:
            dict: A dictionary representing the optimal actions.

        Example:
            >>> model.optimal_actions(
            ...     {"x": 0.5},
            ...     ["x"],
            ...     {"y": 0.5}
        """
        headers = {"token": self.client.token}

        query = {
            "targets": targets,
            "actionable": actionable,
        }

        if fixed:
            query["fixed"] = fixed

        if constraints:
            query["constraints"] = constraints

        if data is not None:
            query["data"] = data.to_dict(orient="list")

        if target_importance:
            query["target_importance"] = target_importance

        try:
            response = requests.post(
                f"{get_causadb_url()}/models/{self.model_name}/find-best-actions",
                headers=headers,
                json=query,
            )
        except Exception as e:
            raise Exception(f"CausaDB server request failed: {e}")

        if response.status_code != 200:
            raise Exception(response.json()["detail"])

        response = response.json()

        if "best_actions" in response:
            return pd.DataFrame.from_dict(response["best_actions"])

        raise Exception("CausaDB server request failed - unexpected response.")

    @validate_call
    def causal_attributions(self, outcome: str, normalise: bool = False) -> pd.DataFrame:
        """Get the causal attributions for an outcome.

        Args:
            outcome (str): The outcome node.
            normalise (bool): Whether to normalise the causal attributions.

        Returns:
            pd.DataFrame: A dataframe representing the causal attributions of the outcome.

        Example:
            >>> model.causal_attributions("y")
        """
        headers = {"token": self.client.token}

        query = {
            "outcome": outcome,
            "normalise": normalise
        }

        try:
            response = requests.post(
                f"{get_causadb_url()}/models/{self.model_name}/causal-attributions",
                headers=headers,
                json=query,
            )
        except Exception as e:
            raise Exception(f"CausaDB server request failed: {e}")

        if response.status_code != 200:
            raise Exception(response.json()["detail"])

        response = response.json()

        if "outcome" in response:
            return pd.DataFrame.from_dict(response["outcome"])

        raise Exception("CausaDB server request failed")

    def _update(self) -> None:
        """Pushes the current state of the model to the CausaDB server."""
        headers = {"token": self.client.token}

        try:
            response = requests.post(
                f"{get_causadb_url()}/models/{self.model_name}",
                headers=headers,
                json=self.config
            )
        except Exception as e:
            raise Exception(f"CausaDB server request failed: {e}")

        if response.status_code != 200:
            raise Exception(response.json()["detail"])
