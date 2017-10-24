from flask import make_response, jsonify, abort, current_app
from werkzeug.http import HTTP_STATUS_CODES
import sys
import os
import traceback

class Response():
    
    @classmethod
    def _make_json_response(cls, response, code=200):
        """
        This method sets up the json response for all other response types
        jsonifies the data and sets the content type
        """
        #if response type is not defined, use default HTTP status name
        if code is not 200 and not response['errors']['type']:
           response['errors']['type'] = HTTP_STATUS_CODES[code]
        
        return make_response(jsonify(response), code)
    
    @classmethod
    def make_success_resp(cls, msg=None):
       response = {
          'success': True,
          'message': msg or ''
       }
       return cls._make_json_response(response)
    
    @classmethod
    def make_data_resp(cls, data, msg=None):
        response = {
           'success': True,
           'data'   : data,
           'message': msg or ''
        }
        return cls._make_json_response(response)
    
    @classmethod   
    def make_error_resp(cls, msg, type=None, code=400):
        response = {
           'errors': {
              'code' : code,
              'message' : msg or "Something is wrong!",
              'type'     : type
           }
        }
        return cls._make_json_response(response, code)
    
    @classmethod   
    def make_form_error_resp(cls, form, msg=None):
        type = 'Form validation error'
        if not msg:
           msg = form.errors
        return cls.make_error_resp(msg=msg, type=type, code=422)
    
    @classmethod   
    def make_exception_resp(cls, exception, type=None, code=500):
        #NOTE: Will probably not want to display excpetion to users in production
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #include file name, line number and stacktrace
        msg = "Exception: %s: %s: %s %s" % (exc_type, fname, exc_tb.tb_lineno, traceback.format_exc())
        if(current_app.config['DEBUG']):
           return cls.make_error_resp(msg=msg, type=type, code=422)
        else:
           current_app.logger.critical('Exception caught:  %s' % msg)
           return cls.make_error_resp(msg="Internal Server Error. Report this problem!", type=type, code=422)