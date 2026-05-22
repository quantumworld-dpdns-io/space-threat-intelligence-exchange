---
name: data-analysis
description: Analyze threat intelligence data using DuckDB, Apache Arrow, and DataFusion
---

# Data Analysis Skill

Analyze space threat intelligence data using local analytical engines.

## Tools Available

### DuckDB (Local Analytics)
```python
from stie.storage.duckdb_client import duckdb_analytics

duckdb_analytics.connect()
results = duckdb_analytics.query("""
    SELECT threat_type, severity, COUNT(*) as count
    FROM analytics.threat_summary
    GROUP BY threat_type, severity
""")
```

### Apache Arrow (Data Interchange)
```python
from stie.storage.arrow_client import arrow_client

table = arrow_client.query_parquet("data/threats.parquet")
print(table.schema)
```

### Apache DataFusion (Query Engine)
```python
from stie.storage.datafusion_client import datafusion_analytics

datafusion_analytics.connect()
datafusion_analytics.register_parquet("threats", "data/threats.parquet")
result = datafusion_analytics.sql("SELECT * FROM threats LIMIT 10")
```

### Qdrant (Vector Similarity)
```python
from stie.storage.qdrant_client import get_qdrant

client = await get_qdrant()
results = await client.search(
    collection_name="threat_reports",
    query_vector=embedding,
    limit=10,
)
```

## Reference Files
- `src/stie/storage/duckdb_client.py`
- `src/stie/storage/arrow_client.py`
- `src/stie/storage/datafusion_client.py`
