class Data:
    def __repr__(self) -> str:
        return f"<Data {self.data_name}>"

    def __init__(self, data_name: str) -> None:
        """Initializes the Data class.

        Args:
            data_name (str): The name of the data.
        """
        self.data_name = data_name
