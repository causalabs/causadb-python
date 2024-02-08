# Set Edges

```python
def set_edges(edges: list[tuple[str, str]]) -> None
```

Set the edges of the model.

**Arguments**:

- `edges` _list[tuple[str, str]]_ - A list of tuples representing edges.
  

**Example**:

  >>> model.set_edges([
  ...     ("SaturatedFatsInDiet", "Weight"),
  ...     ("Weight", "BMI"),
  ... ])

<a id="model.Model.get_edges"></a>

