from cqapi.predicates import Predicate, parse_predicate


def dict_to_concept_query(dictionary: dict):
    return ConceptQuery(
        parse_predicate(dictionary.get("root", None))
    )


class ConceptQuery:
    def __init__(self, root: Predicate):
        self.root: Predicate = root

    def __str__(self):
        return f"ConceptQuery({str(self.root)})"

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def _to_execution_format(self):
        return {"type": "CONCEPT_QUERY", "root": self.root._to_execution_format()}
