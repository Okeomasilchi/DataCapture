from flask import Flask, Blueprint, g, render_template

app = Flask(__name__)

# Define two blueprints
bp1 = Blueprint('bp1', __name__)
bp2 = Blueprint('bp2', __name__)

# First blueprint
@bp1.route('/route1')
def route1():
    g.data_to_pass = "Hello from Route 1"
    return render_template('template1.html')

# Second blueprint
@bp2.route('/route2')
def route2():
    data_received = getattr(g, 'data_to_pass', 'Default Data')
    return f"Data received in Route 2: {data_received}"

# Register blueprints with the app
app.register_blueprint(bp1)
app.register_blueprint(bp2, url_prefix='/bp2')  # Optional: Define a prefix for the second blueprint

if __name__ == '__main__':
    app.run(debug=True)
