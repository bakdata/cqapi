# cqapi

## Installation



## Usage

#### ConqueryConnection

Always use `ConqueryConnection` as an asynchronous context manager:
```python
from cqapi import ConqueryConnection

async with ConqueryConnection("http://conquery-base.url:9082") as cq:
    query_result = await cq.get_query("demo", "query.id")
    query = query_result['query']
    query_execution_id = await cq.execute_query("demo", query)
    
```

## Usage in a Jupyter Notebook

This package can be used just the same in a Jupyter Notebook given that the underlying kernel supports top-level
`async` calls.

The IPython shell and IPykernel have [added support for top-level `async` since version 7.0](https://blog.jupyter.org/ipython-7-0-async-repl-a35ce050f7f7).
To make sure you're running the latest versions of both run `pip install ipython ipykernel --upgrade`.



## Run Tests

`python -m pytest tests/`