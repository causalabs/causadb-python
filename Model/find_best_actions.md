# Find Best Actions

```python
def find_best_actions(targets: dict[str, float],
                      actionable: list[str],
                      fixed: dict[str, float] = \{\}) -> dict
```

Get the optimal actions for a given set of target outcomes.

**Arguments**:

- `targets` _dict[str, float]_ - A dictionary representing the target outcomes.
- `actionable` _list[str]_ - A list of actionable nodes.
- `fixed` _dict[str, float]_ - A dictionary representing the fixed nodes.
  

**Returns**:

- `dict` - A dictionary representing the optimal actions.
  

**Example**:

  >>> model.optimal_actions(
  ...     \{"x": 0.5\},
  ...     ["x"],
  ...     \{"y": 0.5\}

<a id="model.Model.causal_attributions"></a>

