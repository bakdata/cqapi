# cqapi

[![Build Status](https://dev.azure.com/bakdata/public/_apis/build/status/bakdata.cqapi?branchName=master)](https://dev.azure.com/bakdata/public/_build/latest?definitionId=11&branchName=master)

## Installation

Some functionality of `cqapi` requires Python version `>= 3.7`.

To install the latest version of `cqapi` on the `master` branch run:
```
pip install git+ssh://git@github.com/bakdata/cqapi@master
```

Note that you can specify any branch or tag using the `@branch/tag-name` syntax, but the `master` branch is where we
attempt to keep a working version of this library.

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

The IPython shell and IPykernel have
[added support for top-level `async` since version 7.0](https://blog.jupyter.org/ipython-7-0-async-repl-a35ce050f7f7).
To make sure you're running the latest versions of both run `pip install ipython ipykernel --upgrade`.



## Run Tests

`python -m pytest tests/`