# Causal Effects

```python
@validate_call
def causal_effects(actions: Union[str, dict[str, tuple[float, float]]],
                   fixed: dict[str, float] = None,
                   interval: float = 0.90,
                   observation_noise=False) -> pd.DataFrame
```

Get the causal effects of actions on the model.

**Arguments**:

- `actions` _Union[str, dict[str, tuple[np.ndarray, np.ndarray]]]_ - A dictionary representing the actions.
- `fixed` _dict_ - A dictionary representing the fixed nodes.
- `interval` _float_ - The interval at which to simulate the action.
- `observation_noise` _bool_ - Whether to include observation noise.
  

**Returns**:

- `pd.DataFrame` - A dataframe representing the causal effects of the actions.
  

**Example**:

  >>> model.causal_effects(
  ...     \{"x": [0, 1]\}
  ... )

<a id="model.Model.find_best_actions"></a>

