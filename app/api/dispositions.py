"""API route for dispositions."""

import base64
import json
import os
import pickle
import sys
import traceback

from app.dispositions import Dispositions
from app.response import Response
from bson.json_util import dumps, RELAXED_JSON_OPTIONS
from flask import Blueprint, request, current_app
from json import JSONDecodeError
from .tasks import cache_mongodb_request_task
from pymongo.errors import OperationFailure, InvalidOperation

dispositions = Blueprint('dispositions', __name__, url_prefix='/v1/dispositions')


@dispositions.route('/', methods=['GET'])
def get_disposition_data():
    """Get disposition data."""
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
        if not request.args:
            request_args = {}
        else:
            request_args = request.args

        # pass MultiDict of query params to the find method
        cursor, metadata = Dispositions.find(request_args)
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
            cache_mongodb_request_task(Dispositions, request_args, encoded_full_path, data['metadata'])
    except Exception as err:
        # log the caching exception
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # include the filename, line number, and stacktrace
        exception_msg = 'Exception: {}: {}: {} {}'.format(exc_type, fname, exc_tb.tb_lineno, traceback.format_exc())
        current_app.logger.critical('Exception caught: {}'.format(exception_msg))

    return Response.make_data_resp(data=data,
                                   msg='Query successful.')
