"""API route for fields."""

import base64
import json
import os
import pickle
import sys
import traceback

from app.scraper.models.us.ustx.fields import (CourtDivisionIndicator,
                                               InstrumentType,
                                               CaseDisposition,
                                               CaseStatus,
                                               DefendantStatus,
                                               CurrentOffenseLevelDegree,
                                               DocketCalendarName,
                                               CalendarReason,
                                               DefendantRace,
                                               DefendantBirthplace,
                                               DefendantUSCitizen)
from app.response import Response
from bson.json_util import dumps, RELAXED_JSON_OPTIONS
from flask import Blueprint, request, current_app
from json import JSONDecodeError
from .tasks import cache_mongodb_request_task
from pymongo.errors import OperationFailure, InvalidOperation

fields = Blueprint('case_status', __name__, url_prefix='/v1/fields')
models = {
    "court_division_indicator": CourtDivisionIndicator,
    "instrument_type": InstrumentType,
    "case_disposition": CaseDisposition,
    "case_status": CaseStatus,
    "defendant_status": DefendantStatus,
    "current_offense_level_degree": CurrentOffenseLevelDegree,
    "docket_calendar_name": DocketCalendarName,
    "calendar_reason": CalendarReason,
    "defendant_race": DefendantRace,
    "defendant_birthplace": DefendantBirthplace,
    "defendant_uscitizen": DefendantUSCitizen
}


@fields.route('/<field>', methods=['GET'])
def get_field_data(field):
    """Get fields data."""
    # b64 encode the full path
    encoded_full_path = base64.urlsafe_b64encode(request.full_path.encode()).decode()

    # check for cache
    try:
        redis = current_app.redis
        if 'query' in request.args:
            p_string = redis.get(request.args.get('query', None))
            if p_string is not None:
                data = pickle.loads(p_string)
                return Response.make_data_resp(data=data,
                                               msg='Query successful.')
            else:
                return Response.make_error_resp(msg='Error: The query id: {} has expired.'.format(request.args
                                                                                                         .get('query',
                                                                                                              None)),
                                                type='Not Found',
                                                code=404)
        else:
            redis = current_app.redis
            p_string = redis.get('{}_{}'.format(encoded_full_path, 1))
            if p_string is not None:
                data = pickle.loads(p_string)
                return Response.make_data_resp(data=data,
                                               msg='Query successful.')

    except Exception as err:
        # other error
        return Response.make_exception_resp(err,
                                            type=err.__class__.__name__,
                                            code=500)

    try:
        if not field:
            return Response.make_error_resp(msg='Error: A URL parameter is required.',
                                            type='Bad Request',
                                            code=400)
        else:
            # pass MultiDict of query params to the find method
            cursor, metadata = models[field].find(request.args)
    except ValueError as err:
        return Response.make_error_resp(msg=json.loads(str(err))['message'],
                                        type=err.__class__.__name__,
                                        code=400)
    except KeyError as err:
        return Response.make_error_resp(msg=json.loads(str(err))['message'],
                                        type=err.__class__.__name__,
                                        code=400)
    except Exception as err:
        # other error
        return Response.make_exception_resp(err,
                                            type=err.__class__.__name__,
                                            code=500)

    try:
        # total
        total_docs = cursor.count()

        # https://stackoverflow.com/questions/14822184/is-there-a-ceiling-equivalent-of-operator-in-python
        total_batches = -(-total_docs//metadata['batch_size'])  # upside-down floor divsion

        # determine the existence of another batch
        next_batch = 2 if 1 < total_batches else 1

        # convert cursor to json response
        data = {
            'metadata': {
                'total': total_docs,
                'batch_size': metadata['batch_size'],
                'query': '{}_{}'.format(encoded_full_path, 1),
                'next': '{}_{}'.format(encoded_full_path, next_batch),
                'links': {
                    'self': {
                        'href': '{}?query={}'.format(request.path, '{}_{}'.format(encoded_full_path, 1))
                    },
                    'next': {
                        'href': '{}?query={}'.format(request.path, '{}_{}'.format(encoded_full_path, next_batch))
                    }
                }
            },
            'results': [json.loads(dumps(doc, json_options=RELAXED_JSON_OPTIONS)) for doc in cursor.rewind()
                                                                                                   .limit(metadata['batch_size'])]
        }

    except OperationFailure as err:
        # database error on cursor.count()
        return Response.make_exception_resp(err,
                                            type=err.__class__.__name__,
                                            code=500)
    except InvalidOperation as err:
        # cursor has already been used
        return Response.make_exception_resp(err,
                                            type=err.__class__.__name__,
                                            code=500)
    except JSONDecodeError as err:
        # data being deserialized is not a valid JSON document
        return Response.make_exception_resp(err,
                                            type=err.__class__.__name__,
                                            code=500)
    except TypeError as err:
        # cursor.limit(int) or cusor.skip(int) is not an integer
        return Response.make_exception_resp(err,
                                            type=err.__class__.__name__,
                                            code=500)
    except ValueError as err:
        # cusor.skip(int) is less than 0
        return Response.make_exception_resp(err,
                                            type=err.__class__.__name__,
                                            code=500)
    except Exception as err:
        return Response.make_exception_resp(err,
                                            type=err.__class__.__name__,
                                            code=500)

    try:
        if total_docs > 0:
            cache_mongodb_request_task(models[field], request.args, encoded_full_path, data['metadata'], cache_expire=24000)
    except Exception as err:
        # log the caching exception
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # include the filename, line number, and stacktrace
        exception_msg = 'Exception: {}: {}: {} {}'.format(exc_type, fname, exc_tb.tb_lineno, traceback.format_exc())
        current_app.logger.critical('Exception caught: {}'.format(exception_msg))

    return Response.make_data_resp(data=data,
                                   msg='Query successful.')
