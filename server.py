from flask import Flask
import os

# Create a Flask app
app = Flask(__name__)

# Define a route for the root URL '/'
@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    # Get the port number from the PORT environment variable, or use 5000 as a default
    port = int(os.environ.get('PORT', 5000))

    # Run the Flask app on the provided port
    app.run(host='0.0.0.0', port=port)
