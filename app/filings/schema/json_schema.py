"""JSON Schema for filings package."""

filings_json_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "rundate",
            "court_division_indicator_code",
            "case_number",
            "instrument_type_code",
            "case_disposition_code",
            "court",
            "case_status_code",
            "defendant_status_code",
            "current_offense_code",
            "current_offense_level_degree_code",
            "defendant_spn"
        ],
        "properties": {
            "rundate": {
                "bsonType": ["date", "timestamp"],
                "description": ""
            },
            "court_division_indicator_code": {
                "bsonType": ["int", "string"],
                "description": ""
            },
            "case_number": {
                "bsonType": ["long", "int", "string"],
                "description": ""
            },
            "filing_date": {
                "bsonType": ["date", "timestamp", "null"],
                "description": ""
            },
            "instrument_type_code": {
                "bsonType": "string",
                "description": ""
            },
            "case_disposition_code": {
                "bsonType": "string",
                "description": ""
            },
            "court": {
                "bsonType": ["int", "string"],
                "description": ""
            },
            "case_status_code": {
                "bsonType": "string",
                "description": ""
            },
            "defendant_status_code": {
                "bsonType": "string",
                "description": ""
            },
            "bond_amount": {
                "bsonType": ["int", "string", "null"],
                "description": ""
            },
            "current_offense_code": {
                "bsonType": ["int", "long", "string"],
                "description": ""
            },
            "current_offense_definition": {
                "bsonType": ["string", "null"],
                "description": ""
            },
            "current_offense_level_degree_code": {
                "bsonType": "string",
                "description": ""
            },
            "next_appearance_date": {
                "bsonType": ["date", "timestamp", "null"],
                "description": ""
            },
            "docket_calendar_name_code": {
                "bsonType": ["string", "null"],
                "description": ""
            },
            "calendar_reason_code": {
                "bsonType": ["string", "null"],
                "description": ""
            },
            "defendant_name": {
                "bsonType": ["string", "null"],
                "description": ""
            },
            "defendant_spn": {
                "bsonType": ["int", "long", "string"],
                "description": ""
            },
            "defendant_race_code": {
                "bsonType": ["string", "null"],
                "description": ""
            },
            "defendant_sex": {
                "bsonType": ["string", "null"],
                "description": ""
            },
            "defendant_date_of_birth": {
                "bsonType": ["date", "timestamp", "null"],
                "description": ""
            },
            "defendant_street_number": {
                "bsonType": ["string", "int", "long", "null"],
                "description": ""
            },
            "defendant_street_name": {
                "bsonType": ["string", "null"],
                "description": ""
            },
            "defendant_city": {
                "bsonType": ["string", "null"],
                "description": ""
            },
            "defendant_state": {
                "bsonType": ["string", "null"],
                "description": ""
            },
            "defendant_zip_code": {
                "bsonType": ["string", "int", "null"],
                "description": ""
            },
            "defendant_birthpace_code": {
                "bsonType": ["string", "null"],
                "description": ""
            },
            "defendant_uscitizen_code": {
                "bsonType": ["string", "null"],
                "description": ""
            },
            "attorney_name": {
                "bsonType": ["string", "null"],
                "description": ""
            },
            "attorney_spn": {
                "bsonType": ["int", "long", "string", "null"],
                "description": ""
            },
            "attorney_connection_code": {
                "bsonType": ["string", "null"],
                "description": ""
            },
            "attorney_connection_definition": {
                "bsonType": ["string", "null"],
                "description": ""
            }
        }
    }
}
