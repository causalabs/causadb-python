# Simulate Actions

```python
def simulate_actions(actions: dict,
                     fixed: dict = \{\},
                     interval: float = 0.9,
                     observation_noise: bool = False) -> dict
```

Simulate an action on the model.

**Arguments**:

- `actions` _dict_ - A dictionary representing the actions.
- `fixed` _dict_ - A dictionary representing the fixed nodes.
- `interval` _float_ - The interval at which to simulate the action.
- `observation_noise` _bool_ - Whether to include observation noise.
  

**Returns**:

- `dict` - A dictionary representing the result of the action.
  

**Example**:

  >>> model.simulate_actions(
  ...     \{"x": [0, 1]\}
  ... )

<a id="model.Model.causal_effects"></a>

