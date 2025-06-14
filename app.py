from flask import Flask, render_template
from ai_routes import ai_routes

app = Flask(__name__)
app.register_blueprint(ai_routes) # Import the ai_routes blueprint from ai_routes.py

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
