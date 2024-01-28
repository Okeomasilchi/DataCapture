#!/bin/env bash

# Create folder 'api' at the root of the project
mkdir -p test_api

# Create an empty file '__init__.py' in the 'api' folder
touch test_api/__init__.py

# Create folder 'v1' inside 'api'
mkdir -p test_api/test_v1

# Create an empty file '__init__.py' in the 'v1' folder
touch test_api/test_v1/__init__.py

# Create a file 'app.py' in the 'v1' folder
echo -e "from flask import Flask\nfrom models import storage\nfrom api.v1.views import app_views\nimport os\n\napp = Flask(__name__)\napp.register_blueprint(app_views)\n\n@app.teardown_appcontext\ndef close():\n    storage.close()\n\nif __name__ == \"__main__\":\n    host = os.environ.get(\"HBNB_API_HOST\", \"0.0.0.0\")\n    port = int(os.environ.get(\"HBNB_API_PORT\", 5000))\n    app.run(host=host, port=port, threaded=True)" > api/v1/app.py

# Create folder 'views' inside 'v1'
mkdir -p api/v1/views

# Create a file '__init__.py' in the 'views' folder
echo -e "from flask import Blueprint\n\napp_views = Blueprint('app_views', __name__, url_prefix='/api/v1')\n\n# Import all views in the package (wildcard import)\nfrom . import *" > api/v1/views/__init__.py

# Create a file 'index.py' in the 'views' folder
echo -e "from api.v1.views import app_views\n\n@app_views.route('/status', methods=['GET'])\ndef get_status():\n    return {\"status\": \"OK\"}" > api/v1/views/index.py
