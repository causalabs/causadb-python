# Set Node Types

```python
@validate_call
def set_node_types(node_types: dict) -> None
```

Set the node types of the model.

**Arguments**:

- `node_types` _dict_ - A dictionary of node types.
  

**Example**:

  >>> model.set_node_types(\{
  ...     "x1": \{"type": "seasonal", "min": 0, "max": 1\}
  ... \})

<a id="model.Model.get_node_types"></a>

