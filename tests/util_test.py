from cqapi.util import selects_per_concept


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

expected = {
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
    assert expected == selects_per_concept(concepts)
