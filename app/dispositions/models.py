"""Dispositions Model."""

import datetime
import json

from app.dispositions.schema import dispositions_json_schema, dispositions_denormalized_pipeline
from app.extensions import db


class Dispositions(object):
    """Dispositions Class.

    Establish the schema for disposition objects.
    Define methods for downloading and parsing disposition data.
    """

    schema_validator = dispositions_json_schema

    def __init__(self):
        """__init__ method.

        Method undefined
        """
        pass

    def __repr__(self):
        """__repr__ method.

        Print a string representation of the Python object to be parsed by the
        Python interpreter.
        """
        pass

    @classmethod
    def setup_schema(cls):
        """Set up the MongoDB schema."""
        db.create_collection('dispositions', validator=cls.schema_validator)

    @classmethod
    def create_denormalized_view(cls):
        """Create a denormalized view of the model."""
        db.command('create', 'denormalized_dispositions_view',
                   viewOn='dispositions',
                   pipeline=dispositions_denormalized_pipeline)

    @classmethod
    def find(cls, request_params):
        """Find dispositions from an http request.

        request_params is a MultiDict.
        """
        # initialize the query
        query = {}

        # closure methods
        def date_range_min(path, value):
            """Create a query for date ranges."""
            nonlocal query

            # check data format YYYY-MM-DD
            try:
                # parse the provided value into a datetime object
                dt = datetime.datetime.strptime(value, '%Y-%m-%d')
            except ValueError as err:
                error = {
                    'message': ('Invalid Parameter: '
                                'The date parameter "{}" is not the correct format. '
                                'The date should be supplied in YYYY-MM-DD format.').format(value),
                    'sys_message': str(err)
                }
                error = json.dumps(error)
                raise ValueError(error) from err

            # check for an existing date range set on the path
            if path in query:
                # look for a $lt value
                if '$lte' in query[path]:
                    # save the $lt range limit
                    lte = query[path]['$lte']
                    query[path] = {
                        '$gte': dt,
                        '$lte': lte
                    }
                else:
                    query[path] = {'$gte': dt}
            else:
                query[path] = {'$gte': dt}

        def date_range_max(path, value):
            """Create a query for date ranges."""
            nonlocal query

            # check data format YYYY-MM-DD
            try:
                # parse the provided value into a datetime object
                dt = datetime.datetime.strptime(value, '%Y-%m-%d')
            except ValueError as err:
                error = {
                    'message': ('Invalid Parameter: '
                                'The date parameter "{}" is not the correct format. '
                                'The date should be supplied in YYYY-MM-DD format.').format(value),
                    'sys_message': str(err)
                }
                error = json.dumps(error)
                raise ValueError(error) from err

            # check for an existing date range set on the path
            if path in query:
                # look for a $gt value
                if '$gte' in query[path]:
                    # save the $gt range limit
                    gte = query[path]['$gte']
                    query[path] = {
                        '$gte': gte,
                        '$lte': dt
                    }
                else:
                    query[path] = {'$lte': dt}
            else:
                query[path] = {'$lte': dt}

        def string_search(path, value):
            """Search mongo path for string matches."""
            nonlocal query
            search_words = value.split(' ')
            # capturing group, positive lookahead, match any character, zero or more times, match search word
            pattern = ''.join(list(map(lambda x: '(?=.*{})'.format(str(x)), search_words)))
            query[path] = {
                '$regex': '^{}'.format(pattern),
                '$options': 'ims'
            }

        def number_range_min(path, value):
            """Create a query for number ranges."""
            nonlocal query

            # check data format as integer
            try:
                # parse the provided value into a float
                num = int(value)
            except ValueError as err:
                error = {
                    'message': ('Invalid Parameter: '
                                'The number parameter "{}" is not the correct format. '
                                'The number should be supplied as an integer or float.').format(value),
                    'sys_message': str(err)
                }
                error = json.dumps(error)
                raise ValueError(error) from err

            # check for an existing date range set on the path
            if path in query:
                # look for a $lte value
                if '$lte' in query[path]:
                    # save the $lte range limit
                    lte = query[path]['$lte']
                    query[path] = {
                        '$gte': num,
                        '$lte': lte
                    }
                else:
                    query[path] = {'$gte': num}
            else:
                query[path] = {'$gte': num}

        def number_range_max(path, value):
            """Create a query for number ranges."""
            nonlocal query

            # check data format as integer
            try:
                # parse the provided value into a float
                num = int(value)
            except ValueError as err:
                error = {
                    'message': ('Invalid Parameter: '
                                'The number parameter "{}" is not the correct format. '
                                'The number should be supplied as an integer or float.').format(value),
                    'sys_message': str(err)
                }
                error = json.dumps(error)
                raise ValueError(error) from err

            # check for an existing date range set on the path
            if path in query:
                # look for a $gte value
                if '$gte' in query[path]:
                    # save the $lte range limit
                    gte = query[path]['$gte']
                    query[path] = {
                        '$gte': gte,
                        '$lte': num
                    }
                else:
                    query[path] = {'$lte': num}
            else:
                query[path] = {'$lte': num}

        # map parameters to methods
        param_map = {
            'rundate': {'path': 'rundate'},
            'rundate_min': {
                'path': 'rundate',
                'method': date_range_min
            },
            'rundate_max': {
                'path': 'rundate',
                'method': date_range_max
            },
            'filing_date': {'path': 'filing_date'},
            'filing_date_min': {
                'path': 'filing_date',
                'method': date_range_min
            },
            'filing_date_max': {
                'path': 'filing_date',
                'method': date_range_max
            },
            'instrument_type': {
                'path': 'instrument_type.definition',
                'method': string_search
            },
            'case_disposition': {
                'path': 'case_disposition.definition',
                'method': string_search
            },
            'court_division_indicator': {
                'path': 'court_division_indicator.definition',
                'method': string_search
            },
            'case_status': {
                'path': 'case_status.definition',
                'method': string_search
            },
            'defendant_status': {
                'path': 'defendant_status.definition',
                'method': string_search
            },
            'bond_amount': {'path': 'bond_amount'},
            'bond_amount_min': {
                'path': 'bond_amount',
                'method': number_range_min
            },
            'bond_amount_max': {
                'path': 'bond_amount',
                'method': number_range_max
            },
            'current_offense': {
                'path': 'current_offense.definition',
                'method': string_search
            },
            'next_appearance_date': {'path': 'next_appearance_date'},
            'next_appearance_date_min': {
                'path': 'next_appearance_date',
                'method': date_range_min
            },
            'next_appearance_date_max': {
                'path': 'next_appearance_date',
                'method': date_range_max
            },
            'docket_calendar_name': {
                'path': 'docket_calendar_name.definition',
                'method': string_search
            },
            'calendar_reason': {
                'path': 'calendar_reason.definition',
                'method': string_search
            },
            'current_offense_level_degree': {
                'path': 'current_offense.level_degree.definition',
                'method': string_search
            },
            'defendant_spn': {
                'path': 'defendant.spn',
                'method': string_search
            },
            'defendant_sex': {
                'path': 'defendant.sex',
                'method': string_search
            },
            'defendant_race': {
                'path': 'defendant.race.definition',
                'method': string_search
            },
            'defendant_dob': {'path': 'defendant.date_of_birth'},
            'defendant_dob_min': {
                'path': 'defendant.date_of_birth',
                'method': date_range_min
            },
            'defendant_dob_max': {
                'path': 'defendant.date_of_birth',
                'method': date_range_max
            },
            'defendant_street_number': {
                'path': 'defendant.address.street_number',
                'method': string_search
            },
            'defendant_street_name': {
                'path': 'defendant.address.street_name',
                'method': string_search
            },
            'defendant_street_address': {
                'path': 'defendant.address.street_address',
                'method': string_search
            },
            'defendant_city': {
                'path': 'defendant.address.city',
                'method': string_search
            },
            'defendant_state': {
                'path': 'defendant.address.state',
                'method': string_search
            },
            'defendant_zip_code': {
                'path': 'defendant.address.zip_code',
                'method': string_search
            },
            'attorney_spn': {
                'path': 'attorney.spn',
                'method': string_search
            },
            'attorney_connection': {
                'path': 'attorney.connection.definition',
                'method': string_search
            },
            'disposition_date': {'path': 'disposition_date'},
            'disposition_date_min': {
                'path': 'disposition_date',
                'method': date_range_min
            },
            'disposition_date_max': {
                'path': 'disposition_date',
                'method': date_range_max
            },
            'disposition': {
                'path': 'disposition',
                'method': string_search
            },
            'sentence': {
                'path': 'sentence',
                'method': string_search
            },
            'complainant_name': {
                'path': 'complainant.name',
                'method': string_search
            },
            'complainant_agency': {
                'path': 'complainant.agency',
                'method': string_search
            },
            'offense_report_number': {
                'path': 'offense_report_number',
                'method': string_search
            }
        }

        # build the query dict
        if not request_params:
            cursor = db.denormalized_dispositions_view.find(query,
                                                            limit=1000000,
                                                            batch_size=10000)
            metadata = {'limit': 1000000, 'batch_size': 10000}
            return cursor, metadata

        for key, val in request_params.items():
            if key in param_map:
                if 'method' in param_map[key]:
                    method = param_map[key]['method']
                    path = param_map[key]['path']
                    try:
                        method(path, val)
                    except ValueError as err:
                        raise
                    except Exception as err:
                        raise
                else:
                    error = {
                        'message': ('Invalid Parameter: '
                                    'An unsupported query parameter was supplied.')
                    }
                    error = json.dumps(error)
                    raise ValueError(error)

        # fields
        if 'fields' in request_params:
            try:
                # map the fields into a projection
                fields = request_params.get('fields', None).split(',')
                projection = {}
                for field in fields:
                    projection[param_map[field]['path']] = 1
            except KeyError as err:
                error = {
                    'message': ('Invalid field provided: '
                                'Please reference the API documentation for valid values for the "fields" parameter.'),
                    'sys_message': str(err)
                }
                error = json.dumps(error)
                raise KeyError(error) from err

        else:
            projection = None

        # limit
        try:
            limit = int(request_params.get('limit', 1000000))
        except ValueError as err:
            error = {
                'message': ('Invalid Parameter: '
                            'The "limit" parameter "{}" is not the correct format. '
                            'An integer should be supplied.').format(request_params.get('limit', 10000)),
                'sys_message': str(err)
            }
            error = json.dumps(error)
            raise ValueError(error) from err

        # batch size
        try:
            batch_size = int(request_params.get('batch_size', 10000))
        except ValueError as err:
            error = {
                'message': ('Invalid Parameter: '
                            'The "batch_size" parameter "{}" is not the correct format. '
                            'An integer should be supplied.').format(request_params.get('batch_size', 10000)),
                'sys_message': str(err)
            }
            error = json.dumps(error)
            raise ValueError(error) from err

        cursor = db.denormalized_dispositions_view.find(query,
                                                        limit=limit,
                                                        projection=projection,
                                                        batch_size=batch_size)
        metadata = {'limit': limit, 'batch_size': batch_size}
        return cursor, metadata
