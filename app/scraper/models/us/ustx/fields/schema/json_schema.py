"""JSON Schema for hcdc_fields package."""

court_division_indicator_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "code",
            "definition"
        ],
        "properties": {
            "code": {
                "bsonType": ["int", "string"],
                "description": ""
            },
            "definition": {
                "bsonType": "string",
                "description": ""
            }
        }
    }
}

instrument_type_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "code",
            "definition"
        ],
        "properties": {
            "code": {
                "bsonType": "string",
                "description": ""
            },
            "definition": {
                "bsonType": "string",
                "description": ""
            }
        }
    }
}

case_disposition_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "code",
            "definition"
        ],
        "properties": {
            "code": {
                "bsonType": "string",
                "description": ""
            },
            "definition": {
                "bsonType": "string",
                "description": ""
            }
        }
    }
}

case_status_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "code",
            "definition"
        ],
        "properties": {
            "code": {
                "bsonType": "string",
                "description": ""
            },
            "definition": {
                "bsonType": "string",
                "description": ""
            }
        }
    }
}

defendant_status_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "code",
            "definition"
        ],
        "properties": {
            "code": {
                "bsonType": "string",
                "description": ""
            },
            "definition": {
                "bsonType": "string",
                "description": ""
            }
        }
    }
}

current_offense_level_degree_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "code",
            "definition"
        ],
        "properties": {
            "code": {
                "bsonType": "string",
                "description": ""
            },
            "definition": {
                "bsonType": "string",
                "description": ""
            }
        }
    }
}

docket_calendar_name_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "code",
            "definition"
        ],
        "properties": {
            "code": {
                "bsonType": "string",
                "description": ""
            },
            "definition": {
                "bsonType": "string",
                "description": ""
            }
        }
    }
}

calendar_reason_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "code",
            "definition"
        ],
        "properties": {
            "code": {
                "bsonType": "string",
                "description": ""
            },
            "definition": {
                "bsonType": "string",
                "description": ""
            }
        }
    }
}

defendant_race_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "code",
            "definition"
        ],
        "properties": {
            "code": {
                "bsonType": "string",
                "description": ""
            },
            "definition": {
                "bsonType": "string",
                "description": ""
            }
        }
    }
}

defendant_birthplace_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "code",
            "definition"
        ],
        "properties": {
            "code": {
                "bsonType": "string",
                "description": ""
            },
            "definition": {
                "bsonType": "string",
                "description": ""
            }
        }
    }
}

defendant_uscitizen_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "code",
            "definition"
        ],
        "properties": {
            "code": {
                "bsonType": "string",
                "description": ""
            },
            "definition": {
                "bsonType": "string",
                "description": ""
            }
        }
    }
}
