def object_to_dict(obj):
    """ Convert object to dict with __class__ and __module__ members.

    Can be used with json.dumps to serialize an object to json in a format
    from which it can be deserialized into the original object again.

    :param obj: Object to be serialized
    :return: (JSON-serializable) dictionary with __class__ and __module__ members
    :rtype: dict

    :example:
    >>> json.dumps(object, default=object_to_dict)
    """
    obj_dict = {
        "__class__": obj.__class__.__name__,
        "__module__": obj.__module__
    }

    obj_dict.update(obj.__dict__)

    return obj_dict


def dict_to_object(dictionary):
    """ Convert dictionary to Python object if dictionary has __class__ and __module__ members.

    Can be used with json.loads to deserialize a JSON-encoded object.
    :param dictionary: Dictionary to deserialize
    :return: Deserialized object if __class__ and __module__ are present, otherwise the input dictionary.

    :example:
    >>> json.loads('{"__class__":"someClass","__module__":"someModule", ... }', object_hook=dict_to_object)
    """
    if "__class__" in dictionary and "__module__" in dictionary:
        class_name = dictionary.pop("__class__")
        module_name = dictionary.pop("__module__")

        module = __import__(module_name)

        class_ = getattr(module, class_name)

        object = class_(**dictionary)
    else:
        object = dictionary
    return object


def selects_per_concept(concepts: dict):
    """ Aggregates a dict of concepts to a dict of available selects per concept.

    Used to declutter the concepts dict returned from a ConqueryConnection.get_concepts('dataset') call.

    Usage example:
        # lets say you're interested in all available selects (specifically their ids) for a specific concept
        concepts = await cq.get_concepts('dataset')
        selects_of_concept_x = selects_per_concept(concepts).get('concept_x')
        type(selects_of_concept)  # = list, because of the above .get() call on the dictionary

        # selects_of_concept is applicable also to concepts returned by cq.get_concept('dataset', 'specific_concept')
        concepts = await cq.get_concept('dataset', 'specific_concept')
        selects_by_concept = selects_per_concept(concepts)
        type(selects_by_concept)  # = dict

    :param concepts: dict of concepts as returned by ConqueryConnection.get_concept and .get_concepts calls.
    :return: dict of list of available selects, i.e. a mapping from concept to its available selects.
    """
    return {concept_id: concept.get('selects', []) for (concept_id, concept) in concepts.items()}


def add_selects_to_concept(query, target_concept_id: str, selects: list):
    """ Add select-ids to CONCEPT nodes in CONCEPT_QUERYs.

    :param query: query to add selects to.
    :param target_concept_id: CONCEPT's id to which the selects should be added.
    :param selects: list or select ids to be added.
    :return: the enriched query object - will be the same as the input query iff it does not contain any CONCEPT nodes
        with the target_concept_id.
    """
    query_node_type = query.get('type')
    if query_node_type == 'CONCEPT_QUERY':
        query['root'] = add_selects_to_concept(query.get('root'), target_concept_id, selects)
        return query
    elif query_node_type == 'AND':
        query['children'] = [add_selects_to_concept(child, target_concept_id, selects) for child in query.get('children')]
        return query
    elif query_node_type == 'OR':
        query['children'] = [add_selects_to_concept(child, target_concept_id, selects) for child in query.get('children')]
        return query
    elif query_node_type == 'NEGATION':
        query['child'] = add_selects_to_concept(query.get('child'), target_concept_id, selects)
        return query
    elif query_node_type == 'DATE_RESTRICTION':
        query['child'] = add_selects_to_concept(query.get('child'), target_concept_id, selects)
        return query
    elif query_node_type == 'CONCEPT':
        if query.get('selects') is not None:
            query.get('selects').extend(selects)
            return query
        else:
            query['selects'] = selects
            return query
    else:
        raise Exception(f"Unknown type in query: {query.get('type')}")
