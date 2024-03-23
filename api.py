#!/usr/bin/python3

import os
from api.v1 import app


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    app.run(host=host, port=5000, debug=True, threaded=True)
