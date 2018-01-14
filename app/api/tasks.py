"""Celery tasks for api endpoints."""

import base64
import json
import pickle

from app.extensions import celery
from bson.json_util import dumps, RELAXED_JSON_OPTIONS
from celery import chain
from flask import current_app
from json import JSONDecodeError
from pymongo.errors import OperationFailure, InvalidOperation


class APIEndpointTaskBaseClass(celery.Task):
    """Scrape Task Base Class."""

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Error Handler."""
        # log the failure
        # use print(), as anything written to standard out/-err will be redirected to the logging system
        print('Task ID: {0} Error Type: {1} Error Message: {2} Error Traceback: {3}'.format(task_id,
                                                                                            exc.__class__.__name__,
                                                                                            str(exc),
                                                                                            einfo.traceback))


@celery.task(base=APIEndpointTaskBaseClass, serializer='pickle')
def cache_mongodb_request(model, request_args, encoded_full_path=None, batch_size=None, batch=None, cache_expire=24):
    """Celery task to cache the results of a mongodb query."""
    try:
        cursor, metadata = model.find(request_args)

        # total
        total_docs = cursor.count()

        # determine docs to skip
        skipped = batch_size * (batch - 1)
        skipped = 0 if skipped < 0 else skipped

        # https://stackoverflow.com/questions/14822184/is-there-a-ceiling-equivalent-of-operator-in-python
        total_batches = -(-total_docs//batch_size)  # upside-down floor divsion

        # determine the path of the request
        full_path = base64.urlsafe_b64decode(encoded_full_path).decode()
        path = full_path.split('?')[0]

        # determine the existence of another batch
        next_batch = batch + 1 if batch < total_batches else batch

        # convert cursor to json response
        data = {
            'metadata': {
                'total': total_docs,
                'offset': skipped,
                'batch_size': batch_size,
                'query': '{}_{}'.format(encoded_full_path, batch),
                'next': '{}_{}'.format(encoded_full_path, next_batch),
                'links': {
                    'self': {
                        'href': '{}?query={}'.format(path, '{}_{}'.format(encoded_full_path, batch))
                    },
                    'next': {
                        'href': '{}?query={}'.format(path, '{}_{}'.format(encoded_full_path, next_batch))
                    }
                }
            },
            'results': [json.loads(dumps(doc, json_options=RELAXED_JSON_OPTIONS)) for doc in cursor.rewind()
                                                                                                   .skip(skipped)
                                                                                                   .limit(batch_size)]
        }

        # cache the hash in redis
        redis = current_app.redis  # current_app requires the application context
        p_data = pickle.dumps(data)
        redis.set(data['metadata']['query'], p_data)

        # set the query to expire in 24 hours
        redis.expire(data['metadata']['query'], int(cache_expire) * 60 * 60)

        return cursor

    except OperationFailure as err:
        # database error on cursor.count()
        raise
    except InvalidOperation as err:
        # cursor has already been used
        raise
    except JSONDecodeError as err:
        # data being deserialized is not a valid JSON document
        raise
    except TypeError as err:
        # cursor.limit(int) or cusor.skip(int) is not an integer
        raise
    except ValueError as err:
        # cusor.skip(int) is less than 0
        raise
    except Exception as err:
        raise


def cache_mongodb_request_task(model, request_args, encoded_full_path, metadata, cache_expire=24):
    """Cache the MongoDB request."""
    # determine the size of the cursor
    total_docs = metadata['total']
    # determine batch size
    batch_size = metadata['batch_size']
    # determine number of batches to process
    # https://stackoverflow.com/questions/14822184/is-there-a-ceiling-equivalent-of-operator-in-python
    total_batches = -(-total_docs//batch_size)  # upside-down floor divsion

    task = chain(cache_mongodb_request.si(model,
                                          request_args,
                                          encoded_full_path=encoded_full_path,
                                          batch_size=batch_size,
                                          batch=i,
                                          cache_expire=cache_expire) for i in range(total_batches))

    task.apply_async(serializer='pickle')

    data = {
        "task_id": task.id,
        "msg": "Asynchronous task started to process the following MongoDB query: {}.".format(encoded_full_path)
    }

    return data
