from cqapi import Concept, AndPredicate, ConceptQuery
from cqapi.util import object_to_dict, dict_to_object
import json


concept = Concept("TestConcept",
                  ["test.id1", "test.id2"],
                  ["test.table1", "test.table2"],
                  ["test.select1", "test.select2"],
                  False)

and_pred = AndPredicate([concept])

concept_query = ConceptQuery(and_pred)

expected_serialization = """{
    "__class__": "ConceptQuery",
    "__module__": "cqapi.concept_query",
    "root": {
        "__class__": "AndPredicate",
        "__module__": "cqapi.predicates",
        "children": [
            {
                "__class__": "Concept",
                "__module__": "cqapi.predicates",
                "label": "TestConcept",
                "ids": [
                    "test.id1",
                    "test.id2"
                ],
                "tables": [
                    "test.table1",
                    "test.table2"
                ],
                "selects": [
                    "test.select1",
                    "test.select2"
                ],
                "exclude_from_time_aggregation": false
            }
        ]
    }
}"""

def test_concept_query_init():
    assert(isinstance(concept_query, ConceptQuery))


def test_concept_query_equality():
    equal_concept_query = ConceptQuery(and_pred)
    unequal_concept_query = ConceptQuery(concept)
    assert concept_query == equal_concept_query
    assert concept_query != unequal_concept_query


def test_concept_query_serialization():
    serialized = json.dumps(concept_query, default=object_to_dict, indent=4)
    assert serialized == expected_serialization


def test_concept_query_deserialization():
    deserialized = json.loads(expected_serialization, object_hook=dict_to_object)
    assert deserialized == concept_query

