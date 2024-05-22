# Causal Attributions

```python
@validate_call
def causal_attributions(outcome: str, normalise: bool = False) -> pd.DataFrame
```

Get the causal attributions for an outcome.

**Arguments**:

- `outcome` _str_ - The outcome node.
- `normalise` _bool_ - Whether to normalise the causal attributions.
  

**Returns**:

- `pd.DataFrame` - A dataframe representing the causal attributions of the outcome.
  

**Example**:

  >>> model.causal_attributions("y")

<a id="data"></a>

# data

<a id="data.Data"></a>

