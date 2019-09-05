from cqapi.util import *
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
        "selects": [{
            "id": "select.id"
         }]
    },
    "multiple_selects": {
        "selects": [
            {"id": "select.id.1"},
            {"id": "selects.id.2"},
            {"id": "select.id.3"}
        ]
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
        "selects": [{
            "id": "select.id"
        }]
    },
    "multiple_selects_chatter": {
        "other": "attributes",
        "number": 1,
        "selects": [
            {"id": "select.id.1"},
            {"id": "selects.id.2"},
            {"id": "select.id.3"}
        ]
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
    enriched_query = add_selects_to_concept_query(query_without_concept, target_concept_id, [select_id])
    assert query_without_concept == enriched_query


def test_add_select_to_concept_with_match():
    enriched_query = add_selects_to_concept_query(query_with_concept, target_concept_id, [select_id])
    expected = copy.deepcopy(query_with_concept)
    expected['root']['children'][1]['selects'] = [select_id]
    assert expected == enriched_query


def test_add_selects_to_concept_with_match_with_preexisting():
    enriched_query = add_selects_to_concept_query(query_with_concept_and_preexisting_selects, target_concept_id, [select_id])
    assert select_id in enriched_query['root']['children'][1]['selects']


def test_add_selects_to_concept_with_date_restriction():
    enriched_query = add_selects_to_concept_query(query_with_daterange, target_concept_id, [select_id])
    assert select_id in enriched_query['root']['children'][1]['child']['selects']


def test_add_date_restriction_to_concept_bad_dateranges():
    with pytest.raises(ValueError) as e:
        add_date_restriction_to_concept_query(query_with_concept, target_concept_id, "1-02-1902", date.today())
    with pytest.raises(ValueError) as e:
        add_date_restriction_to_concept_query(query_with_concept, target_concept_id, date.today(), "199-02-01")
    with pytest.raises(ValueError) as e:
        add_date_restriction_to_concept_query(query_with_concept, target_concept_id, "2019-02-18", "1992-02-18")
    assert "Invalid DATE_RESTRICTION: Start-date after end-date" == str(e.value)


def test_add_date_restriction_to_concept():
    enriched_query = add_date_restriction_to_concept_query(query_with_concept, target_concept_id, "1992-02-18", "2019-08-23")
    assert query_with_daterange == enriched_query


def test_create_relative_query():
    # bad time unit
    with pytest.raises(ValueError) as e:
        create_relative_query({}, {}, {}, 1, 1, time_unit='NOT_A_TIME_UNIT')
    assert "Invalid time_unit. Must be one of ['QUARTERS', 'DAYS']" == str(e.value)

    # bad time values
    with pytest.raises(ValueError) as e:
        create_relative_query({}, {}, {}, 1, -1)
    assert "Invalid time_after. Must be positive" == str(e.value)
    with pytest.raises(ValueError) as e:
        create_relative_query({}, {}, {}, -1, 1)
    assert "Invalid time_before. Must be positive" == str(e.value)

    # bad index selector
    with pytest.raises(ValueError) as e:
        create_relative_query({}, {}, {}, 1, 1, index_selector='NOT_VALID')
    assert "Invalid index_selector. Must be one of ['FIRST', 'LAST', 'RANDOM']" == str(e.value)

    # bad index placement
    with pytest.raises(ValueError) as e:
        create_relative_query({}, {}, {}, 1, 1, index_placement='NOT_VALID')
    assert "Invalid index_placement. Must be one of ['BEFORE', 'NEUTRAL', 'AFTER']" == str(e.value)

    # valid input
    index_query = {
        'lets_pretend': 'this was a valid query'
    }
    before = [
        {
            'before': 'feature'
        },
        {
            'another': 'concept'
        }
    ]
    after = {
        'after': 'outcome concept'
    }

    query = create_relative_query(index_query, before, after, 2, 1, index_selector='LAST', index_placement='BEFORE',
                                  time_unit='DAYS')
    expected = {
        'type': 'RELATIVE_FORM_QUERY',
        'query': index_query,
        'features': before,
        'outcomes': after,
        'indexSelector': 'LAST',  # FIRST, LAST, RANDOM
        'indexPlacement': 'BEFORE',  # BEFORE, AFTER, NEUTRAL
        'timeCountBefore': 2,
        'timeCountAfter': 1,
        'timeUnit': 'DAYS'
    }
    assert expected == query

    query_with_defaults = create_relative_query(index_query, before, after, 4, 4)
    expected = {
        'type': 'RELATIVE_FORM_QUERY',
        'query': index_query,
        'features': before,
        'outcomes': after,
        'indexSelector': 'FIRST', # FIRST, LAST, RANDOM
        'indexPlacement': 'NEUTRAL', # BEFORE, AFTER, NEUTRAL
        'timeCountBefore': 4,
        'timeCountAfter': 4,
        'timeUnit': 'QUARTERS'
    }
    assert expected == query_with_defaults


valid_date_strings = [
    {
        'string': '2020-04-12',
        'expected': date(2020, 4, 12)
    },
    {
        'string': '2020-03-31',
        'expected': date(2020, 3, 31)
    },
    {
        'string': '1922-12-24',
        'expected': date(1922, 12, 24)
    }
]

@pytest.mark.parametrize("param", valid_date_strings)
def test_parse_iso_date(param):
    input = param.get('string')
    expected = param.get('expected')
    assert expected == _parse_iso_date(input)


invalid_date_strings = [
    {
        'string': '2020-13-31',
        'expected': ValueError
    },
    {
        'string': '1922-12-32',
        'expected': ValueError
    },
    {
        'string': '2012-02-30',
        'expected': ValueError
    },
    {
        'string': '1900-04-31',
        'expected': ValueError
    },
    {
        'string': '1900-04-31-12',
        'expected': ValueError
    }
]

@pytest.mark.parametrize("param", invalid_date_strings)
def test_parse_iso_date_failures(param):
    input = param.get('string')
    expected_error = param.get('expected')
    with pytest.raises(expected_error):
        _parse_iso_date(input)
