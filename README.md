### A python client for Mesh Queries

#### Installation

`pip install mesh-python`

#### Usage

```python
from mesh import MeshClient

key = "{username}:{password}"
client = MeshClient(key)
query = "$UNIV2.DPI_WETH.DPI_PRICE"

df = client.engine(query)
```