import numpy as np
import pandas as pd

np.random.seed(42)

if __name__ == "__main__":
    x = np.random.normal(0, 1, 100)
    y = 2 * x + np.random.normal(0, 0.1, 100)
    z = -1 * y + np.random.normal(0, 0.1, 100)

    data = pd.DataFrame({
        "x": x,
        "y": y,
        "z": z,
    })

    data.to_csv("tests/test-data.csv", index=False)
