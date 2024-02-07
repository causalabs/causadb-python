import requests
import pandas as pd
from .utils import CAUSADB_URL


class Data:
    def __repr__(self) -> str:
        return f"<Data {self.data_name}>"

    def __init__(self, data_name: str, client: "CausaDB") -> None:
        """Initializes the Data class.

        Args:
            data_name (str): The name of the data.
            client (CausaDB): A CausaDB client.
        """
        self.data_name = data_name
        self.client = client

    def _update_data(self, data: dict) -> None:
        """Update the database with new data.

        Args:
            data (dict): The new data.
        """

        # Send a POST request to the CausaDB server to update the data
        try:
            headers = {"token": self.client.token_secret}
            response = requests.post(
                f"{CAUSADB_URL}/data/{self.data_name}",
                headers=headers,
                json=data,
            ).json()
        except:
            raise Exception("CausaDB client failed to connect to server")

        if response["status"] != "success":
            # If the response is not successful, raise an exception and include the error message
            raise Exception(f"Failed to update data: {response['message']}")

    def from_csv(self, filepath: str) -> None:
        """Add data from a CSV file.

        Args:
            filepath (str): The path to the CSV file.
        """
        dataset = pd.read_csv(filepath).to_dict()

        self._update_data(dataset)
