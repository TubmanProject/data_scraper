"""Controllers module for the frontend package."""
from flask import Blueprint, render_template

frontend = Blueprint('frontend', __name__)


@frontend.route('/', methods=['GET'])
def api_index():
    """Index page for the API documentation."""
    return render_template('api_docs.html')
