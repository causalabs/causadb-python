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
