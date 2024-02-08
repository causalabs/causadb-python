# Train

```python
def train(wait=True, poll_interval=0.2) -> None
```

Train the model.

**Arguments**:

- `wait` _bool_ - Whether to wait for the model to finish training.
- `poll_interval` _float_ - The interval at which to poll the server for the model status.
  

**Example**:

  >>> model.train()

<a id="model.Model.status"></a>

