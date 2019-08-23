from cqapi.util import selects_per_concept, add_selects_to_concept, add_date_restriction_to_concept
import copy
from datetime import date
import pytest

concepts = {
    "no_selects": {
    },
    "empty_selects": {
        "selects": []
    },
    "single_selects": {
        "selects": ["select.id"]
    },
    "multiple_selects": {
        "selects": ["select.id.1", "selects.id.2", "select.id.3"]
    },
    "no_selects_chatter": {
        "other": "attributes",
        "number": 1
    },
    "empty_selects_chatter": {
        "other": "attributes",
        "number": 1,
        "selects": []
    },
    "single_selects_chatter": {
        "other": "attributes",
        "number": 1,
        "selects": ["select.id"]
    },
    "multiple_selects_chatter": {
        "other": "attributes",
        "number": 1,
        "selects": ["select.id.1", "selects.id.2", "select.id.3"]
    },
}

expected_selects = {
    "no_selects": [],
    "empty_selects": [],
    "single_selects": ["select.id"],
    "multiple_selects": ["select.id.1", "selects.id.2", "select.id.3"],
    "no_selects_chatter": [],
    "empty_selects_chatter": [],
    "single_selects_chatter": ["select.id"],
    "multiple_selects_chatter": ["select.id.1", "selects.id.2", "select.id.3"]
}


def test_selects_from_concepts():
    assert expected_selects == selects_per_concept(concepts)


target_concept_id = "target_concept.id"
select_id = "target_concept.select.id"

query_with_concept = {
    "type": "CONCEPT_QUERY",
    "root": {
        "type": 'AND',
        "children": [
            {
                "type": "OR",
                "children": [
                    {
                        "excludeFromTimeAggregation": False,
                        "ids": [ "other.id"],
                        "label": "3771",
                        "tables": [{"id": "demo.table"}],
                        "type": "CONCEPT"
                    },
                    {
                        "excludeFromTimeAggregation": False,
                        "ids": [ "yet_another.id"],
                        "label": "1617",
                        "tables": [{"id": "demo.table"}],
                        "type": "CONCEPT"
                    }
                ]
            },
            {
                "type": "CONCEPT",
                "ids": ["target_concept.id"],
                "label": "target concept",
                "tables": [{"id": "some.table"}],
                "excludeFromTimeAggregation": False
            }
        ]
    }
}

query_with_concept_and_preexisting_selects = {
    "type": "CONCEPT_QUERY",
    "root": {
        "type": 'AND',
        "children": [
            {
                "type": "OR",
                "children": [
                    {
                        "excludeFromTimeAggregation": False,
                        "ids": [ "other.id"],
                        "label": "3771",
                        "tables": [{"id": "demo.table"}],
                        "type": "CONCEPT"
                    },
                    {
                        "excludeFromTimeAggregation": False,
                        "ids": [ "yet_another.id"],
                        "label": "1617",
                        "tables": [{"id": "demo.table"}],
                        "type": "CONCEPT"
                    }
                ]
            },
            {
                "type": "CONCEPT",
                "ids": ["target_concept.id"],
                "label": "target concept",
                "selects": ["some_other_select"],
                "tables": [{"id": "some.table"}],
                "excludeFromTimeAggregation": False
            }
        ]
    }
}

query_without_concept = {
    "type": "CONCEPT_QUERY",
    "root": {
        "type": 'AND',
        "children": [
            {
                "type": "OR",
                "children": [
                    {
                        "excludeFromTimeAggregation": False,
                        "ids": ["other.id"],
                        "label": "3771",
                        "tables": [{"id": "demo.table"}],
                        "type": "CONCEPT"
                    },
                    {
                        "excludeFromTimeAggregation": False,
                        "ids": ["yet_another.id"],
                        "label": "1617",
                        "tables": [{"id": "demo.table"}],
                        "type": "CONCEPT"
                    }
                ]
            },
            {
                "type": "CONCEPT",
                "ids": ["not_the_target_concept.id"],
                "label": "not target concept",
                "tables": [{"id": "some.table"}],
                "excludeFromTimeAggregation": False
            }
        ]
    }
}

query_with_daterange = {
    "type": "CONCEPT_QUERY",
    "root": {
        "type": 'AND',
        "children": [
            {
                "type": "OR",
                "children": [
                    {
                        "excludeFromTimeAggregation": False,
                        "ids": ["other.id"],
                        "label": "3771",
                        "tables": [{"id": "demo.table"}],
                        "type": "CONCEPT"
                    },
                    {
                        "excludeFromTimeAggregation": False,
                        "ids": ["yet_another.id"],
                        "label": "1617",
                        "tables": [{"id": "demo.table"}],
                        "type": "CONCEPT"
                    }
                ]
            },
            {
                "type": "DATE_RESTRICTION",
                "dateRange": {
                    "min": "1992-02-18",
                    "max": "2019-08-23"
                },
                "child": {
                    "type": "CONCEPT",
                    "ids": ["target_concept.id"],
                    "label": "target concept",
                    "tables": [{"id": "some.table"}],
                    "excludeFromTimeAggregation": False
                }
            }
        ]
    }
}


def test_add_select_to_concept_without_match():
    enriched_query = add_selects_to_concept(query_without_concept, target_concept_id, [select_id])
    assert query_without_concept == enriched_query


def test_add_select_to_concept_with_match():
    enriched_query = add_selects_to_concept(query_with_concept, target_concept_id, [select_id])
    expected = copy.deepcopy(query_with_concept)
    expected['root']['children'][1]['selects'] = [select_id]
    assert expected == enriched_query


def test_add_selects_to_concept_with_match_with_preexisting():
    enriched_query = add_selects_to_concept(query_with_concept_and_preexisting_selects, target_concept_id, [select_id])
    assert select_id in enriched_query['root']['children'][1]['selects']


def test_add_selects_to_concept_with_date_restriction():
    enriched_query = add_selects_to_concept(query_with_daterange, target_concept_id, [select_id])
    assert select_id in enriched_query['root']['children'][1]['child']['selects']


def test_add_date_restriction_to_concept_bad_dateranges():
    with pytest.raises(ValueError) as e:
        add_date_restriction_to_concept(query_with_concept, target_concept_id, "199-02-01", date.today())
    assert "Invalid isoformat string: 199-02-01" == str(e.value)
    with pytest.raises(ValueError) as e:
        add_date_restriction_to_concept(query_with_concept, target_concept_id,  date.today(), "199-02-01")
    assert "Invalid isoformat string: 199-02-01" == str(e.value)
    with pytest.raises(ValueError) as e:
        add_date_restriction_to_concept(query_with_concept, target_concept_id,  "2019-02-18", "1992-02-18")
    assert "Invalid DATE_RESTRICTION: Start-date after end-date" == str(e.value)


def test_add_date_restriction_to_concept():
    enriched_query = add_date_restriction_to_concept(query_with_concept, target_concept_id, "1992-02-18", "2019-08-23")
    assert query_with_daterange == enriched_query
