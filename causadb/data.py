import requests
import pandas as pd
from .utils import get_causadb_url


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

    def remove(self) -> None:
        """Remove the data from the CausaDB system."""
        headers = {"token": self.client.token}
        try:
            requests.delete(
                f"{get_causadb_url()}/data/{self.data_name}",
                headers=headers,
            )
        except Exception as e:
            raise Exception(f"CausaDB server request failed: {e}")

    def from_csv(self, filepath: str) -> None:
        """Add data from a CSV file.

        Args:
            filepath (str): The path to the CSV file.
        """
        dataset = pd.read_csv(filepath).to_dict()

        self._update(dataset)

    def from_pandas(self, dataframe: pd.DataFrame) -> None:
        """Add data from a pandas DataFrame.

        Args:
            dataframe (pd.DataFrame): The pandas DataFrame.
        """
        dataset = dataframe.to_dict()

        self._update(dataset)

    def from_dict(self, data: dict) -> None:
        """Add data from a dictionary.

        Args:
            data (dict): The data dictionary.
        """
        self._update(data)

    def _update(self, data: dict) -> None:
        """Pushes the data to the CausaDB server.

        Args:
            data (dict): The new data.
        """

        # Check if the data are valid (no missing values, all numeric or string values)
        df = pd.DataFrame(data)
        if df.isnull().values.any():
            raise Exception("Data contains missing values")
        if not all(df.map(lambda x: isinstance(x, (int, float, str))).all()):
            raise Exception("Data contains non-numeric or non-string values")

        # Check that data types are consistent within each column
        inconsistent_columns = []
        for k, v in df.to_dict(orient='list').items():
            if not all(isinstance(value, type(v[0])) for value in v):
                inconsistent_columns.append(k)

        if len(inconsistent_columns) > 0:
            raise Exception(
                f"Data contains inconsistent data types in columns: {inconsistent_columns}"
            )

        # Send a POST request to the CausaDB server to update the data
        try:
            headers = {"token": self.client.token}
            response = requests.post(
                f"{get_causadb_url()}/data/{self.data_name}",
                headers=headers,
                json=data,
            ).json()
        except Exception as e:
            raise Exception(f"CausaDB server request failed: {e}")

        if response["status"] != "success":
            # If the response is not successful, raise an exception and include the error message
            raise Exception(f"Failed to update data: {response['message']}")
