"""MongoDB to JSON Schema Validator."""

# primitives: array, boolean, integer, number, null, object, string
bson_types = {
    "double": {
        "format": False,
        "primitive": "number"
    },
    "string": {
        "format": False,
        "primitive": "string"
    },
    "object": {
        "format": False,
        "primitive": "object"
    },
    "array": {
        "format": False,
        "primitive": "array"
    },
    "bool": {
        "format": False,
        "primitive": "boolean"
    },
    "date": {
        "format": "date-time",
        "primitive": "string"
    },
    "null": {
        "format": False,
        "primitive": "null"
    },
    "regex": {
        "format": "regex",
        "primitive": "string"
    },
    "int": {
        "format": False,
        "primitive": "integer"
    },
    "timestamp": {
        "format": "date-time",
        "primitive": "string"
    },
    "long": {
        "format": False,
        "primitive": "integer"
    },
    "decimal": {
        "format": False,
        "primitive": "number"
    }
}


def mongo_schema_to_json(mongo_schema):
    """Convert bson to json."""
    schema_primitive = mongo_schema['$jsonSchema']['bsonType']
    required = mongo_schema['$jsonSchema']['required']
    properties = mongo_schema['$jsonSchema']['properties']

    json_schema = {}
    # schema declaration
    json_schema['$schema'] = 'http://json-schema.org/draft-04/schema#'
    # root schema instance type declaration
    json_schema['type'] = schema_primitive
    # required must be an array with unique strings as elements
    json_schema['required'] = required
    # initialize the root schema properties
    json_schema['properties'] = {}
    # properties must be a valid JSON schema object
    for key, val in properties.items():
        prop_schema = {}
        if isinstance(val['bsonType'], list):
            tmp_arr = []
            for x in val['bsonType']:
                tmp_arr.append(bson_types[x]['primitive'])
                if bson_types[x]['format']:
                    prop_schema['format'] = bson_types[x]['format']

            unique_arr = list(set(tmp_arr))
            if len(unique_arr) is 1:
                prop_schema['type'] = unique_arr[0]
            else:
                prop_schema['type'] = unique_arr

        elif isinstance(val['bsonType'], str):
            prop_schema['type'] = bson_types[val['bsonType']]['primitive']
            if bson_types[val['bsonType']]['format']:
                prop_schema['format'] = bson_types[val['bsonType']]['format']

        for k, v in val.items():
            if k not in ['bsonType']:
                prop_schema[k] = v

        json_schema['properties'][key] = prop_schema

    return json_schema
