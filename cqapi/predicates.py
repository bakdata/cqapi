from abc import ABC, abstractmethod
from typing import List
import json


def parse_predicate(dictionary: dict):
    type = dictionary.get('type', None)
    if type == 'AND':
        return dict_to_and(dictionary)
    elif type == 'OR':
        return dict_to_or(dictionary)
    elif type == 'NEGATION':
        return dict_to_negation(dictionary)
    elif type == 'DATE_RESTRICTION':
        return dict_to_date_restriction(dictionary)
    elif type == 'CONCEPT':
        return dict_to_concept(dictionary)
    else:
        raise AttributeError('Missing attribute "type" or "type" is not a predicate ("AND", "OR", "NEGATION", "CONCEPT").')


def dict_to_and(dictionary: dict):
    return AndPredicate([parse_predicate(predicate) for predicate in dictionary.get("children", [])])


def dict_to_or(dictionary: dict):
    return OrPredicate([parse_predicate(predicate) for predicate in dictionary.get("children", [])])


def dict_to_negation(dictionary: dict):
    return NegationPredicate(parse_predicate(dictionary.get("child", None)))


def dict_to_date_restriction(dictionary: dict):
    return DateRestrictionPredicate(dictionary.get("dateRange", None), parse_predicate(dictionary.get("child", None)))


def dict_to_concept(dictionary: dict):
    return Concept(
        dictionary.get("label", None),
        dictionary.get("ids"),
        dictionary.get("tables", []),
        dictionary.get("selects", []),
        dictionary.get("exclude_from_time_aggregation", False)
    )


class Predicate(ABC):
    @abstractmethod
    def _to_execution_format(self):
        pass


class AndPredicate(Predicate):
    def __init__(self, children: List[Predicate]):
        self.children = children

    def __str__(self):
        return f"AND({[str(child) for child in self.children]})"

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def _to_execution_format(self):
        return {"type": "AND", "children": [child._to_execution_format() for child in self.children]}


class OrPredicate(Predicate):
    def __init__(self, children: List[Predicate]):
        self.children = children

    def __str__(self):
        return f"AND({[str(child) for child in self.children]})"

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def _to_execution_format(self):
        return {"type": "OR", "children": [child._to_execution_format() for child in self.children]}


class NegationPredicate(Predicate):
    def __init__(self, child: Predicate):
        self.child = child

    def __str__(self):
        return f"NEGATION({str(self.child)})"

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def _to_execution_format(self):
        return {"type": "NEGATION", "child": self.child._to_execution_format()}


class DateRestrictionPredicate(Predicate):
    def __init__(self, date_range: dict, child: Predicate):
        self.date_range = date_range
        self.child = child

    def __str__(self):
        return f"DATE_RESTRICTION(range: {str(self.date_range)}, {str(self.child)})"

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def _to_execution_format(self):
        return {"type": "DATE_RANGE", "dateRange": json.dumps(self.date_range), "child": self.child._to_execution_format()}


class Concept(Predicate):
    def __init__(self, label, ids, tables, selects, exclude_from_time_aggregation):
        self.label = label
        self.ids = ids
        self.tables = tables
        self.selects = selects
        self.exclude_from_time_aggregation = exclude_from_time_aggregation

    def __str__(self):
        return self.label

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def _to_execution_format(self):
        new_dict = dict(self.__dict__)
        new_dict.pop("exclude_from_time_aggregation")
        return dict(new_dict, type="CONCEPT")
