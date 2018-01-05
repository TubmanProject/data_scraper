"""Pipeline for a denormalized dispositions view."""

dispositions_denormalized_pipeline = [
    {
        "$lookup": {
            "from": "court_division_indicator",
            "let": {"cdi": "$court_division_indicator_code"},
            "pipeline": [
                {
                    "$match": {
                        "$expr": {
                            "$eq": ["$code", "$$cdi"]
                        }
                    }
                },
                {
                    "$project": {
                        "_id": 0
                    }
                }
            ],
            "as": "court_division_indicator"
        }
    },
    {
        "$unwind": "$court_division_indicator"
    },
    {
        "$lookup": {
            "from": "instrument_type",
            "let": {"ins": "$instrument_type_code"},
            "pipeline": [
                {
                    "$match": {
                        "$expr": {
                            "$eq": ["$code", "$$ins"]
                        }
                    }
                },
                {
                    "$project": {
                        "_id": 0
                    }
                }
            ],
            "as": "instrument_type"
        }
    },
    {
        "$unwind": "$instrument_type"
    },
    {
        "$lookup": {
            "from": "case_disposition",
            "let": {"cad": "$case_disposition_code"},
            "pipeline": [
                {
                    "$match": {
                        "$expr": {
                            "$eq": ["$code", "$$cad"]
                        }
                    }
                },
                {
                    "$project": {
                        "_id": 0
                    }
                }
            ],
            "as": "case_disposition"
        }
    },
    {
        "$unwind": "$case_disposition"
    },
    {
        "$lookup": {
            "from": "case_status",
            "let": {"cst": "$case_status_code"},
            "pipeline": [
                {
                    "$match": {
                        "$expr": {
                            "$eq": ["$code", "$$cst"]
                        }
                    }
                },
                {
                    "$project": {
                        "_id": 0
                    }
                }
            ],
            "as": "case_status"
        }
    },
    {
        "$unwind": "$case_status"
    },
    {
        "$lookup": {
            "from": "defendant_status",
            "let": {"dst": "$defendant_status_code"},
            "pipeline": [
                {
                    "$match": {
                        "$expr": {
                            "$eq": ["$code", "$$dst"]
                        }
                    }
                },
                {
                    "$project": {
                        "_id": 0
                    }
                }
            ],
            "as": "defendant_status"
        }
    },
    {
        "$unwind": "$defendant_status"
    },
    {
        "$lookup": {
            "from": "current_offense_level_degree",
            "let": {"curr_l_d": "$current_offense_level_degree_code"},
            "pipeline": [
                {
                    "$match": {
                        "$expr": {
                            "$eq": ["$code", "$$curr_l_d"]
                        }
                    }
                },
                {
                    "$project": {
                        "_id": 0
                    }
                }
            ],
            "as": "current_offense_level_degree"
        }
    },
    {
        "$unwind": "$current_offense_level_degree"
    },
    {
        "$lookup": {
            "from": "docket_calendar_name",
            "let": {"cnc": "$docket_calendar_name_code"},
            "pipeline": [
                {
                    "$match": {
                        "$expr": {
                            "$eq": ["$code", "$$cnc"]
                        }
                    }
                },
                {
                    "$project": {
                        "_id": 0
                    }
                }
            ],
            "as": "docket_calendar_name"
        }
    },
    {
        "$unwind": "$docket_calendar_name"
    },
    {
        "$lookup": {
            "from": "calendar_reason",
            "let": {"rea": "$calendar_reason_code"},
            "pipeline": [
                {
                    "$match": {
                        "$expr": {
                            "$eq": ["$code", "$$rea"]
                        }
                    }
                },
                {
                    "$project": {
                        "_id": 0
                    }
                }
            ],
            "as": "calendar_reason"
        }
    },
    {
        "$unwind": "$calendar_reason"
    },
    {
        "$lookup": {
            "from": "defendant_race",
            "let": {"def_rac": "$defendant_race_code"},
            "pipeline": [
                {
                    "$match": {
                        "$expr": {
                            "$eq": ["$code", "$$def_rac"]
                        }
                    }
                },
                {
                    "$project": {
                        "_id": 0
                    }
                }
            ],
            "as": "defendant_race"
        }
    },
    {
        "$unwind": "$defendant_race"
    },
    {
        "$project": {
            "_id": 0,
            "rundate": 1,
            "court_division_indicator": 1,
            "case_number": 1,
            "filing_date": 1,
            "instrument_type": 1,
            "case_disposition": 1,
            "court": 1,
            "case_status": 1,
            "defendant_status": 1,
            "bond_amount": 1,
            "current_offense": {
                "code": "$current_offense_code",
                "definition": "$current_offense_definition",
                "level_degree": "$current_offense_level_degree"
            },
            "next_appearance_date": 1,
            "docket_calendar_name": 1,
            "calendar_reason": 1,
            "defendant": {
                "name": "$defendant_name",
                "spn": "$defendant_spn",
                "sex": "$defendant_sex",
                "race": "$defendant_race",
                "date_of_birth": "$defendant_date_of_birth",
                "address": {
                    "street_number": "$defendant_street_number",
                    "street_name": "$defendant_street_name",
                    "street_address": {"$concat": ["$defendant_street_number", " ", "$defendant_street_name"]},
                    "city": "$defendant_city",
                    "state": "$defendant_state",
                    "zip_code": "$defendant_zip_code"
                }
            },
            "attorney": {
                "name": "$attorney_name",
                "spn": "$attorney_spn",
                "connection": {
                    "code": "$attorney_connection_code",
                    "definition": "$attorney_connection_definition"
                }
            },
            "disposition_date": 1,
            "disposition": 1,
            "sentence": 1,
            "complainant": {
                "name": "$complainant_name",
                "agency": "$complainant_agency"
            },
            "offense_report_number": 1
        }
    }
]
