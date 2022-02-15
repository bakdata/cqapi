# cqapi -- ARCHIVED

[![Build Status](https://dev.azure.com/bakdata/public/_apis/build/status/bakdata.cqapi?branchName=master)](https://dev.azure.com/bakdata/public/_build/latest?definitionId=11&branchName=master)


## Installation

Some functionality of `cqapi` requires Python version `>= 3.7`.

To install the latest version of `cqapi` on the `master` branch run:

```
pip install git+ssh://git@github.com/bakdata/cqapi@master
```

Note that you can specify any branch or tag using the `@branch/tag-name` syntax, but the `master` branch is where we
attempt to keep a working version of this library.

### Usage

```python
from cqapi import ConqueryConnection

async with ConqueryConnection("http://conquery-base.url:9082") as cq:
    query = await cq.get_query("demo", "query.id")
    query_execution_id = await cq.execute_query("demo", query)
    query_result = await cq.get_query_result("demo", query_execution_id)
```

## Notes on Jupyter Notebooks

This package can be used just the same in a Jupyter Notebook given that the underlying kernel supports top-level
`async` calls.

The IPython shell and IPykernel have
[added support for top-level `async` since version 7.0](https://blog.jupyter.org/ipython-7-0-async-repl-a35ce050f7f7).
To make sure you're running the latest versions of both run `pip install ipython ipykernel --upgrade`.

## Documentation

Refer to [the docs](doc/doc.md) for usage examples.

## Running Tests

`python -m pytest tests/`
