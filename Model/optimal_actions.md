# Optimal Actions

```python
def optimal_actions(target_outcomes: dict[str, float],
                    actionable_nodes: list[str],
                    condition_nodes: dict[str, float] = \{\}) -> dict
```

Get the optimal actions for a given set of target outcomes.

**Arguments**:

- `target_outcomes` _dict[str, float]_ - A dictionary of target outcomes.
- `actionable_nodes` _list[str]_ - A list of actionable nodes.
- `condition_nodes` _dict[str, float]_ - A dictionary of condition nodes.
  

**Returns**:

- `dict` - A dictionary representing the optimal actions.
  

**Example**:

  >>> model.optimal_actions(
  ...     \{"x": 0.5\},
  ...     ["y"],
  ...     \{"z": 0.5\}
  ... )

<a id="causadb"></a>

# causadb

<a id="causadb.CausaDB"></a>

