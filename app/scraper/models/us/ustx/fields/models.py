"""HCDC fields models."""

import json
import os

from app.extensions import db
from app.scraper.models.us.ustx.fields.schema import (court_division_indicator_schema,
                                                      instrument_type_schema,
                                                      case_disposition_schema,
                                                      case_status_schema,
                                                      defendant_status_schema,
                                                      current_offense_level_degree_schema,
                                                      docket_calendar_name_schema,
                                                      calendar_reason_schema,
                                                      defendant_race_schema,
                                                      defendant_birthplace_schema,
                                                      defendant_uscitizen_schema)


class CourtDivisionIndicator(object):
    """CourtDivisionIndicator class."""

    # tablename
    collection = 'court_division_indicator'

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
        db.create_collection(cls.collection, validator=court_division_indicator_schema)

    @classmethod
    def seed_db(cls, data_path):
        """Seed the collection."""
        data_filename = 'hcdc_{}.json'.format(cls.collection)
        data_filepath = os.path.join(data_path, data_filename)

        # open data file
        try:
            with open(data_filepath, 'r') as f:
                data = json.load(f)
        except EnvironmentError:
            raise

        for d in data:
            # create a new record
            new_record = {}
            new_record['code'] = d['code']
            new_record['definition'] = d['definition']

            # add the new instance of the class to the db session
            try:
                db[cls.collection].insert_one(new_record)
            except Exception:
                raise

    @classmethod
    def find(cls, request_params):
        """Find the court division indicator from an http request.

        request_params is a MultiDict.
        """
        # initialize the query
        query = {}

        # build the query dict
        if not request_params:
            cursor = db.court_division_indicator.find(query,
                                                      projection={'_id': 0},
                                                      limit=1000000,
                                                      batch_size=10000)
            metadata = {'limit': 1000000, 'batch_size': 10000}
            return cursor, metadata

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

        cursor = db.court_division_indicator.find(query,
                                                  projection={'_id': 0},
                                                  limit=limit,
                                                  batch_size=batch_size)
        metadata = {'limit': limit, 'batch_size': batch_size}
        return cursor, metadata


class InstrumentType(object):
    """Instrument Type class."""

    # tablename
    collection = 'instrument_type'

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
        db.create_collection(cls.collection, validator=instrument_type_schema)

    @classmethod
    def seed_db(cls, data_path):
        """Seed the collection."""
        data_filename = 'hcdc_{}.json'.format(cls.collection)
        data_filepath = os.path.join(data_path, data_filename)

        # open data file
        try:
            with open(data_filepath, 'r') as f:
                data = json.load(f)
        except EnvironmentError:
            raise

        for d in data:
            # create a new record
            new_record = {}
            new_record['code'] = d['code']
            new_record['definition'] = d['definition']

            # add the new instance of the class to the db session
            try:
                db[cls.collection].insert_one(new_record)
            except Exception:
                raise

    @classmethod
    def find(cls, request_params):
        """Find the instrument_type from an http request.

        request_params is a MultiDict.
        """
        # initialize the query
        query = {}

        # build the query dict
        if not request_params:
            cursor = db.instrument_type.find(query,
                                             projection={'_id': 0},
                                             limit=1000000,
                                             batch_size=10000)
            metadata = {'limit': 1000000, 'batch_size': 10000}
            return cursor, metadata

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

        cursor = db.instrument_type.find(query,
                                         projection={'_id': 0},
                                         limit=limit,
                                         batch_size=batch_size)
        metadata = {'limit': limit, 'batch_size': batch_size}
        return cursor, metadata


class CaseDisposition(object):
    """Case disposition class."""

    # tablename
    collection = 'case_disposition'

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
        db.create_collection(cls.collection, validator=case_disposition_schema)

    @classmethod
    def seed_db(cls, data_path):
        """Seed the collection."""
        data_filename = 'hcdc_{}.json'.format(cls.collection)
        data_filepath = os.path.join(data_path, data_filename)

        # open data file
        try:
            with open(data_filepath, 'r') as f:
                data = json.load(f)
        except EnvironmentError:
            raise

        for d in data:
            # create a new record
            new_record = {}
            new_record['code'] = d['code']
            new_record['definition'] = d['definition']

            # add the new instance of the class to the db session
            try:
                db[cls.collection].insert_one(new_record)
            except Exception:
                raise

    @classmethod
    def find(cls, request_params):
        """Find the case_disposition from an http request.

        request_params is a MultiDict.
        """
        # initialize the query
        query = {}

        # build the query dict
        if not request_params:
            cursor = db.case_disposition.find(query,
                                              projection={'_id': 0},
                                              limit=1000000,
                                              batch_size=10000)
            metadata = {'limit': 1000000, 'batch_size': 10000}
            return cursor, metadata

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

        cursor = db.case_disposition.find(query,
                                          projection={'_id': 0},
                                          limit=limit,
                                          batch_size=batch_size)
        metadata = {'limit': limit, 'batch_size': batch_size}
        return cursor, metadata


class CaseStatus(object):
    """Case status class."""

    # tablename
    collection = 'case_status'

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
        db.create_collection(cls.collection, validator=case_status_schema)

    @classmethod
    def seed_db(cls, data_path):
        """Seed the collection."""
        data_filename = 'hcdc_{}.json'.format(cls.collection)
        data_filepath = os.path.join(data_path, data_filename)

        # open data file
        try:
            with open(data_filepath, 'r') as f:
                data = json.load(f)
        except EnvironmentError:
            raise

        for d in data:
            # create a new record
            new_record = {}
            new_record['code'] = d['code']
            new_record['definition'] = d['definition']

            # add the new instance of the class to the db session
            try:
                db[cls.collection].insert_one(new_record)
            except Exception:
                raise

    @classmethod
    def find(cls, request_params):
        """Find the case_status from an http request.

        request_params is a MultiDict.
        """
        # initialize the query
        query = {}

        # build the query dict
        if not request_params:
            cursor = db.case_status.find(query,
                                         projection={'_id': 0},
                                         limit=1000000,
                                         batch_size=10000)
            metadata = {'limit': 1000000, 'batch_size': 10000}
            return cursor, metadata

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

        cursor = db.case_status.find(query,
                                     projection={'_id': 0},
                                     limit=limit,
                                     batch_size=batch_size)
        metadata = {'limit': limit, 'batch_size': batch_size}
        return cursor, metadata


class DefendantStatus(object):
    """Defendant status class."""

    # tablename
    collection = 'defendant_status'

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
        db.create_collection(cls.collection, validator=defendant_status_schema)

    @classmethod
    def seed_db(cls, data_path):
        """Seed the collection."""
        data_filename = 'hcdc_{}.json'.format(cls.collection)
        data_filepath = os.path.join(data_path, data_filename)

        # open data file
        try:
            with open(data_filepath, 'r') as f:
                data = json.load(f)
        except EnvironmentError:
            raise

        for d in data:
            # create a new record
            new_record = {}
            new_record['code'] = d['code']
            new_record['definition'] = d['definition']

            # add the new instance of the class to the db session
            try:
                db[cls.collection].insert_one(new_record)
            except Exception:
                raise

    @classmethod
    def find(cls, request_params):
        """Find the defendant_status from an http request.

        request_params is a MultiDict.
        """
        # initialize the query
        query = {}

        # build the query dict
        if not request_params:
            cursor = db.defendant_status.find(query,
                                              projection={'_id': 0},
                                              limit=1000000,
                                              batch_size=10000)
            metadata = {'limit': 1000000, 'batch_size': 10000}
            return cursor, metadata

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

        cursor = db.defendant_status.find(query,
                                          projection={'_id': 0},
                                          limit=limit,
                                          batch_size=batch_size)
        metadata = {'limit': limit, 'batch_size': batch_size}
        return cursor, metadata


class CurrentOffenseLevelDegree(object):
    """CurrentOffenseLevelDegree class."""

    # tablename
    collection = 'current_offense_level_degree'

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
        db.create_collection(cls.collection, validator=current_offense_level_degree_schema)

    @classmethod
    def seed_db(cls, data_path):
        """Seed the collection."""
        data_filename = 'hcdc_{}.json'.format(cls.collection)
        data_filepath = os.path.join(data_path, data_filename)

        # open data file
        try:
            with open(data_filepath, 'r') as f:
                data = json.load(f)
        except EnvironmentError:
            raise

        for d in data:
            # create a new record
            new_record = {}
            new_record['code'] = d['code']
            new_record['definition'] = d['definition']

            # add the new instance of the class to the db session
            try:
                db[cls.collection].insert_one(new_record)
            except Exception:
                raise

    @classmethod
    def find(cls, request_params):
        """Find the current_offense_level_degree from an http request.

        request_params is a MultiDict.
        """
        # initialize the query
        query = {}

        # build the query dict
        if not request_params:
            cursor = db.current_offense_level_degree.find(query,
                                                          projection={'_id': 0},
                                                          limit=1000000,
                                                          batch_size=10000)
            metadata = {'limit': 1000000, 'batch_size': 10000}
            return cursor, metadata

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

        cursor = db.current_offense_level_degree.find(query,
                                                      projection={'_id': 0},
                                                      limit=limit,
                                                      batch_size=batch_size)
        metadata = {'limit': limit, 'batch_size': batch_size}
        return cursor, metadata


class DocketCalendarName(object):
    """DocketCalendarName class."""

    # tablename
    collection = 'docket_calendar_name'

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
        db.create_collection(cls.collection, validator=docket_calendar_name_schema)

    @classmethod
    def seed_db(cls, data_path):
        """Seed the collection."""
        data_filename = 'hcdc_{}.json'.format(cls.collection)
        data_filepath = os.path.join(data_path, data_filename)

        # open data file
        try:
            with open(data_filepath, 'r') as f:
                data = json.load(f)
        except EnvironmentError:
            raise

        for d in data:
            # create a new record
            new_record = {}
            new_record['code'] = d['code']
            new_record['definition'] = d['definition']

            # add the new instance of the class to the db session
            try:
                db[cls.collection].insert_one(new_record)
            except Exception:
                raise

    @classmethod
    def find(cls, request_params):
        """Find the docket_calendar_name from an http request.

        request_params is a MultiDict.
        """
        # initialize the query
        query = {}

        # build the query dict
        if not request_params:
            cursor = db.docket_calendar_name.find(query,
                                                  projection={'_id': 0},
                                                  limit=1000000,
                                                  batch_size=10000)
            metadata = {'limit': 1000000, 'batch_size': 10000}
            return cursor, metadata

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

        cursor = db.docket_calendar_name.find(query,
                                              projection={'_id': 0},
                                              limit=limit,
                                              batch_size=batch_size)
        metadata = {'limit': limit, 'batch_size': batch_size}
        return cursor, metadata


class CalendarReason(object):
    """Calendar reason class."""

    # tablename
    collection = 'calendar_reason'

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
        db.create_collection(cls.collection, validator=calendar_reason_schema)

    @classmethod
    def seed_db(cls, data_path):
        """Seed the collection."""
        data_filename = 'hcdc_{}.json'.format(cls.collection)
        data_filepath = os.path.join(data_path, data_filename)

        # open data file
        try:
            with open(data_filepath, 'r') as f:
                data = json.load(f)
        except EnvironmentError:
            raise

        for d in data:
            # create a new record
            new_record = {}
            new_record['code'] = d['code']
            new_record['definition'] = d['definition']

            # add the new instance of the class to the db session
            try:
                db[cls.collection].insert_one(new_record)
            except Exception:
                raise

    @classmethod
    def find(cls, request_params):
        """Find the calendar_reason from an http request.

        request_params is a MultiDict.
        """
        # initialize the query
        query = {}

        # build the query dict
        if not request_params:
            cursor = db.calendar_reason.find(query,
                                             projection={'_id': 0},
                                             limit=1000000,
                                             batch_size=10000)
            metadata = {'limit': 1000000, 'batch_size': 10000}
            return cursor, metadata

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

        cursor = db.calendar_reason.find(query,
                                         projection={'_id': 0},
                                         limit=limit,
                                         batch_size=batch_size)
        metadata = {'limit': limit, 'batch_size': batch_size}
        return cursor, metadata


class DefendantRace(object):
    """DefendantRace class."""

    # tablename
    collection = 'defendant_race'

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
        db.create_collection(cls.collection, validator=defendant_race_schema)

    @classmethod
    def seed_db(cls, data_path):
        """Seed the collection."""
        data_filename = 'hcdc_{}.json'.format(cls.collection)
        data_filepath = os.path.join(data_path, data_filename)

        # open data file
        try:
            with open(data_filepath, 'r') as f:
                data = json.load(f)
        except EnvironmentError:
            raise

        for d in data:
            # create a new record
            new_record = {}
            new_record['code'] = d['code']
            new_record['definition'] = d['definition']

            # add the new instance of the class to the db session
            try:
                db[cls.collection].insert_one(new_record)
            except Exception:
                raise

    @classmethod
    def find(cls, request_params):
        """Find the defendant_race from an http request.

        request_params is a MultiDict.
        """
        # initialize the query
        query = {}

        # build the query dict
        if not request_params:
            cursor = db.defendant_race.find(query,
                                            projection={'_id': 0},
                                            limit=1000000,
                                            batch_size=10000)
            metadata = {'limit': 1000000, 'batch_size': 10000}
            return cursor, metadata

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

        cursor = db.defendant_race.find(query,
                                        projection={'_id': 0},
                                        limit=limit,
                                        batch_size=batch_size)
        metadata = {'limit': limit, 'batch_size': batch_size}
        return cursor, metadata


class DefendantBirthplace(object):
    """DefendantBirthplace class."""

    # tablename
    collection = 'defendant_birthplace'

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
        db.create_collection(cls.collection, validator=defendant_birthplace_schema)

    @classmethod
    def seed_db(cls, data_path):
        """Seed the collection."""
        data_filename = 'hcdc_{}.json'.format(cls.collection)
        data_filepath = os.path.join(data_path, data_filename)

        # open data file
        try:
            with open(data_filepath, 'r') as f:
                data = json.load(f)
        except EnvironmentError:
            raise

        for d in data:
            # create a new record
            new_record = {}
            new_record['code'] = d['code']
            new_record['definition'] = d['definition']

            # add the new instance of the class to the db session
            try:
                db[cls.collection].insert_one(new_record)
            except Exception:
                raise

    @classmethod
    def find(cls, request_params):
        """Find the defendant_birthplace from an http request.

        request_params is a MultiDict.
        """
        # initialize the query
        query = {}

        # build the query dict
        if not request_params:
            cursor = db.defendant_birthplace.find(query,
                                                  projection={'_id': 0},
                                                  limit=1000000,
                                                  batch_size=10000)
            metadata = {'limit': 1000000, 'batch_size': 10000}
            return cursor, metadata

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

        cursor = db.defendant_birthplace.find(query,
                                              projection={'_id': 0},
                                              limit=limit,
                                              batch_size=batch_size)
        metadata = {'limit': limit, 'batch_size': batch_size}
        return cursor, metadata


class DefendantUSCitizen(object):
    """DefendantUSCitizen class."""

    # tablename
    collection = 'defendant_uscitizen'

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
        db.create_collection(cls.collection, validator=defendant_uscitizen_schema)

    @classmethod
    def seed_db(cls, data_path):
        """Seed the collection."""
        data_filename = 'hcdc_{}.json'.format(cls.collection)
        data_filepath = os.path.join(data_path, data_filename)

        # open data file
        try:
            with open(data_filepath, 'r') as f:
                data = json.load(f)
        except EnvironmentError:
            raise

        for d in data:
            # create a new record
            new_record = {}
            new_record['code'] = d['code']
            new_record['definition'] = d['definition']

            # add the new instance of the class to the db session
            try:
                db[cls.collection].insert_one(new_record)
            except Exception:
                raise

    @classmethod
    def find(cls, request_params):
        """Find the defendant_uscitizen from an http request.

        request_params is a MultiDict.
        """
        # initialize the query
        query = {}

        # build the query dict
        if not request_params:
            cursor = db.defendant_uscitizen.find(query,
                                                 projection={'_id': 0},
                                                 limit=1000000,
                                                 batch_size=10000)
            metadata = {'limit': 1000000, 'batch_size': 10000}
            return cursor, metadata

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

        cursor = db.defendant_uscitizen.find(query,
                                             projection={'_id': 0},
                                             limit=limit,
                                             batch_size=batch_size)
        metadata = {'limit': limit, 'batch_size': batch_size}
        return cursor, metadata
