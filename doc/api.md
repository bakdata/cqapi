# Conquery API

`cqapi` provides functionality to interact with a running Conquery instance's REST interface via the `ConqueryConnection`
context manager.

## `ConqueryConnection`

Always use `ConqueryConnection` as the asynchronous context manager it is.
A connection is opened by providing the address (including the port) of a running Conquery instance:

```python
from cqapi import ConqueryConnection

async with ConqueryConnection("http://conquery-base.url:9082") as cq:
    query = await cq.get_query("demo", "query.id")
    query_execution_id = await cq.execute_query("demo", query)
    query_result = await cq.get_query_result("demo", query_execution_id)
```

A `ConqueryClientConnectionError` will be raised if `cqapi` cannot communicate with Conquery via the given address.

The context manager provides various methods that allow to interact with the Conquery instance that was connected to.
Note that all of the methods provided by a `ConqueryConnection` are `async` and their results need to be `await`ed.

### `cq.get_datasets()`

Will return a `list` of dataset ids.
The dataset ids can then be used with many of the following methods to interact with a specific dataset available on the
Conquery instance you are talking to.

```python
datasets = await cq.get_datasets()
# ['dataset', 'another_dataset_id']
```

### `cq.get_concepts(dataset)`

Will return a `dict` containing top-level concept ids as keys that map to the corresponding concept definition.
Concept ids and definitions can i.a. be used to create new concept queries.

```python
concepts = await cq.get_concepts('dataset')
# {
#   "concept1": {
#     ...
#   },
#   "concept2": {
#     ...
#   }
# }
```

### `cq.get_concept(dataset, concept_id)`

Will return a `list` containing all concept definitions of the concept identified by the given `concept_id` as well as
all child concepts.

```python
concept = await cq.get_concept('dataset', 'concept1')
# [
#   {
#     "ids": [ 'concept1' ],
#     ...
#   },
#   {
#     "ids": [ 'concept1.child' ],
#     ...
#   }
# ]
```

### `cq.get_stored_queries(dataset)`

Will return a `list` of stored queries for the dataset. The stored query objects contain the query itself, as well as
information on when and by whom the query was initially defined.

```python
stored_queries = await cq.get_stored_queries('dataset')
# [
#   {
#     "label": ...,
#     "createdAt": ...,
#     "query": {
#       ...
#     }
#   },
#   ...
# ]
```

### `cq.get_stored_query(dataset, query_id)`

Will return *just the query itself* for a given query id. Note that the query is not wrapped in another JSON object like
is the case with `get_stored_queries`.

```python
query = await cq.get_stored_query('dataset', 'some_query_id')
# {
#   "type": "CONCEPT_QUERY",
#   ...
# }
```

### `cq.get_query(dataset, query_id)`

Will return the query description, including the query itself and its current status, for a given query id.

```python
query_definition = await cq.get_query('dataset', 'some_query_id')
# {
#   "createdAt": ...,
#   "status": 'RUNNING',
#   "query": {
#     ...
#   },
#   ...
# }
```

### `cq.execute_query(dataset, query)`

Starts the execution of a given query on the given dataset. Will return the query id for the newly started query.

```python
query = {
    'type': 'CONCEPT_QUERY',
    'root': {
#       ...    
    }
}
query_id = await cq.execute_query('dataset', query)
# 'qid_1234'
```

### `cq.get_query_result(dataset, query_id)`

Blocks until the given query execution is finished. Once the query execution is finished, `get_query_results` will
return the results table in a `list` of `list`s.

```python
results = await cq.get_query_result('dataset', query_id)
# [['colA', 'colB'],
#  [1,      'A'   ],
#  [42,     'C'   ]]
```

### Corresponding Conquery REST Endpoints 

Each of the provided methods wraps one (sometimes multiple) call to the REST API of Conquery. This association is
summarized in the following table. A comprehensive list of the available endpoints and their documentation can be found
[here](https://github.com/bakdata/conquery/blob/develop/docs/REST%20API%20JSONs.md).

| `ConqueryConnection` method | CQ REST endpoint | HTTP method |
| --------------------------- | ---------------- | ----------- |
| `get_datasets` | `/datasets` | GET |
| `get_concepts` | `/datasets/{dataset}/concepts` | GET |
| `get_concept` | `/datasets/{dataset}/concepts/{concept}` | GET |
| `get_stored_queries` | `/datasets/{dataset}/stored_query` | GET |
| `get_stored_query` | `/datasets/{dataset}/stored_query/{query_id}` | GET |
| `get_query` | `/datasets/{dataset}/queries/{query_id}` | GET |
| `execute_query` | `/datasets/{dataset}/queries` | POST |
| `get_query_result` | `/datasets/{dataset}/queries/{query_id}` and `/datasets/{dataset}/result` | GET & GET|
