# Train

```python
def train(data_name: str = None,
          wait: bool = True,
          poll_interval: float = 0.2,
          poll_limit: float = 30.0,
          verbose: bool = False,
          progress_interval: float = 1.0) -> None
```

Train the model.

**Arguments**:

- `wait` _bool_ - Whether to wait for the model to finish training.
- `poll_interval` _float_ - The interval at which to poll the server for the model status.
- `poll_limit` _float_ - The maximum time to wait for the model to finish training.
- `verbose` _bool_ - Whether to display model progress.
- `progress_interval` _float_ - The interval at which to display the model progress.
  

**Example**:

  >>> model.train()

<a id="model.Model.status"></a>

