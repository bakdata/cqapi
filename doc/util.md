# Utilities

`cqapi` bundles a set of utility functions that have proved useful when working with Conquery query definitions.

These functions can be found in the `util` namespace but are also available as top-level imports:
```python
# makes utility functions available on the global namespace
import cqapi

# allows qualified usage of utility functions; e.g. util.selects_per_concept(concepts)
from cqapi import util
```

### `selects_per_concept(concepts)`

Aggregates a dict of concepts to a dict of available selects per concept.

Can be used to declutter the concepts dict returned from a `cq.get_concepts('dataset')` call.

```python
# selects_of_concept is applicable also to concepts returned by cq.get_concept('dataset', 'specific_concept')
concepts = await cq.get_concepts('dataset')
selects_by_concept = util.selects_per_concept(concepts)
type(selects_by_concept)  # dict of concept ids to available select ids for said concept 
```

### `add_selects_to_concept_query(query, target_concept_id, selects)`

Add select ids to CONCEPT nodes in a given concept query.

```python
# get selects for a given concept
concepts = await cq.get_concepts('dataset')
selects = util.selects_per_concept(concepts).get('concept_id')

# get preexisting query to add selects to
query = await cq.get_stored_query('dataset', 'query_id')

# add all available selects to query
query_with_selects = util.add_selects_to_concept_query(query, 'concept_id', selects)
```

### `add_date_restriction_to_concept_query(query, target_concept_id, date_start, date_end)`

Adds the date restriction directly above all occurrences of the target_concept_id in the query object.

The `date_start` and `date_end` parameters support `datetime.date` objects as well as ISO-formatted date strings.

### `concept_query_from_concept(concept_id, concept_definition)`

Creates a concept query from a given concept id and definition with no additional selects or restrictions.

### `add_subquery_to_concept_query(query, subquery)`

Joins two concept queries in a conjunction. Either query's predicates will be joined in a top-level `AND` predicate.

### `create_relative_query(index_query, before_query, after_query, time_before, time_after)`

Creates a relative time query from an index query, a before_query, an after_query, and the requested time frame.

Parameters:
* `index_query`: Concept query describing the event that is to be used as the index date.
* `before_query`: Concept query to select which information will be requested for the time frame before the index
   date.
* `after_query`: Concept query to select which information will be requested for time frame after the index date.
* `time_before`: Number of time units (see `time_unit`) before the index date to consider using the `before_query`.
* `time_after`: Number of time units (see `time_unit`) after the index date to consider using the `after_query`.
* Optional `index_selector`: One of `'FIRST'` (default), `'LAST'`, and `'RANDOM'`. Selects which index date to use in
  case `index_query` matches multiple event occurrences.
* Optional `index_placement`: One of `'BEFORE'`, `'NEUTRAL'` (default), and `'AFTER'`. Selects if the index event
  should be considered for either of the before or after time frames' results.
* Optional `time_unit`: One of `'QUARTERS'` (default) and `'DAYS'`. Time unit of `time_before` and `time_after`
  respectively.
