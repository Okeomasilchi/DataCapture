#!/usr/bin/python3

import os
from flask_web import app


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT" + "1", 5001))
    app.run(host=host, port=port, debug=True, threaded=True)
