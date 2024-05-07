# Find Best Actions

```python
def find_best_actions(
        targets: dict[str, float],
        actionable: list[str],
        fixed: dict[str, list[float]] = \{\},
        constraints: dict[str, tuple] = \{\},
        data: pd.DataFrame = None,
        target_importance: dict[str, float] = \{\}) -> pd.DataFrame
```

Get the optimal actions for a given set of target outcomes.

**Arguments**:

- `targets` _dict[str, float]_ - A dictionary representing the target outcomes.
- `actionable` _list[str]_ - A list of actionable nodes.
- `fixed` _dict[str, float]_ - A dictionary representing the fixed nodes.
- `constraints` _dict[str, tuple]_ - A dictionary representing the constraints.
- `data` _pd.DataFrame_ - A dataframe representing the data.
- `target_importance` _dict[str, float]_ - A dictionary representing the target importance.
  

**Returns**:

- `dict` - A dictionary representing the optimal actions.
  

**Example**:

  >>> model.optimal_actions(
  ...     \{"x": 0.5\},
  ...     ["x"],
  ...     \{"y": 0.5\}

<a id="model.Model.causal_attributions"></a>

