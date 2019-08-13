from cqapi import Concept, AndPredicate, OrPredicate, Predicate
from cqapi.util import object_to_dict, dict_to_object
import json


concept1 = Concept("TestConcept",
                   ["test.id1", "test.id2"],
                   ["test.table1", "test.table2"],
                   ["test.select1", "test.select2"],
                   False)

concept2 = Concept("TestConcept",
                   ["test.id3", "test.id4"],
                   ["test.table3", "test.table4"],
                   ["test.select3", "test.select4"],
                   True)

and_pred = AndPredicate([concept1, concept2])
or_pred = OrPredicate([concept1, concept2])

expected_serialization_concept = """{
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
}"""

expected_serialization_and = """{
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
        },
        {
            "__class__": "Concept",
            "__module__": "cqapi.predicates",
            "label": "TestConcept",
            "ids": [
                "test.id3",
                "test.id4"
            ],
            "tables": [
                "test.table3",
                "test.table4"
            ],
            "selects": [
                "test.select3",
                "test.select4"
            ],
            "exclude_from_time_aggregation": true
        }
    ]
}"""

expected_serialization_or = """{
    "__class__": "OrPredicate",
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
        },
        {
            "__class__": "Concept",
            "__module__": "cqapi.predicates",
            "label": "TestConcept",
            "ids": [
                "test.id3",
                "test.id4"
            ],
            "tables": [
                "test.table3",
                "test.table4"
            ],
            "selects": [
                "test.select3",
                "test.select4"
            ],
            "exclude_from_time_aggregation": true
        }
    ]
}"""


def test_and_pred_init():
    assert isinstance(and_pred, Predicate)
    assert isinstance(and_pred, AndPredicate)


def test_and_pred_equality():
    and_pred2 = AndPredicate([concept1, concept2])
    and_pred3 = AndPredicate([concept1])

    assert and_pred == and_pred2
    assert and_pred != and_pred3


def test_and_pred_serialization():
    serialized = json.dumps(and_pred, default=object_to_dict, indent=4)
    print(serialized)
    assert serialized == expected_serialization_and


def test_and_deserialization():
    deserialized = json.loads(expected_serialization_and, object_hook=dict_to_object)
    assert deserialized == and_pred


def test_or_pred_init():
    assert isinstance(or_pred, Predicate)
    assert isinstance(or_pred, OrPredicate)


def test_or_pred_equality():
    or_pred2 = OrPredicate([concept1, concept2])
    or_pred3 = OrPredicate([concept1])

    assert or_pred == or_pred2
    assert or_pred != or_pred3


def test_or_pred_serialization():
    serialized = json.dumps(or_pred, default=object_to_dict, indent=4)
    assert serialized == expected_serialization_or


def test_or_deserialization():
    deserialized = json.loads(expected_serialization_or, object_hook=dict_to_object)
    assert deserialized == or_pred


def test_concept_class_init():
    assert isinstance(concept1, Concept)


def test_concept_equality():
    concept3 = Concept("TestConcept",
                       ["test.id3", "test.id4"],
                       ["test.table3", "test.table4"],
                       ["test.select3", "test.select4"],
                       True)

    assert concept1 != concept2
    assert concept2 == concept3


def test_concept_serialization():
    serialized = json.dumps(concept1, default=object_to_dict, indent=4)
    assert serialized == expected_serialization_concept


def test_concept_deserialization():
    deserialized = json.loads(expected_serialization_concept, object_hook=dict_to_object)
    assert deserialized == concept1


