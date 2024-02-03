from flask import Flask, url_for, Blueprint, jsonify, redirect

app = Flask(__name__)

# Define two blueprints
bp1 = Blueprint('bp1', __name__)
bp2 = Blueprint('bp2', __name__)

# First blueprint
@bp1.route('/route1')
def route1():
    data_to_pass = {"message": "Hello from Route 1", "status": "success"}
    return redirect(url_for('bp2.route2', data=data_to_pass))

# Second blueprint
@bp2.route('/route2')
def route2():
    data_received = request.args.get('data')
    return f"Data received in Route 2: {data_received}"

# Register blueprints with the app
app.register_blueprint(bp1)
app.register_blueprint(bp2, url_prefix='/bp2')  # Optional: Define a prefix for the second blueprint

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
