# run.py is used to launch the web server locally
import os
from app import create_app
from app.config import get_config

application_mode = os.getenv('APPLICATION_MODE', 'DEVELOPMENT')
Config = get_config(MODE=application_mode)

app = create_app(config=Config)

# __name__ == '__main__' applies when the module (run.py) is read from STDIN or prompt (python run.py)
if __name__ == '__main__':
    port = int(os.environ.get('PYTHON_PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)