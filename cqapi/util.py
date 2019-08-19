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
    """

    :param concepts:
    :return:
    """
    return {concept_id: concept.get('selects', []) for (concept_id, concept) in concepts.items()}
