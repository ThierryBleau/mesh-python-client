### A python client for Mesh Queries

#### Installation

`pip install mesh-python`

#### Usage

```python
from mesh import MeshClient
import pandas as pd

key = "{your api key}"
client = MeshClient(key)
query = "$UNIV2.DPI_WETH.DPI_PRICE"

df = client.engine(query)
```