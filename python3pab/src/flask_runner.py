from flask import Flask, jsonify
from flask_cors import CORS

import main

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (e.g. from GitHub Pages)

@app.route('/api/data')
def get_data():
    # Replace this with your actual Python logic
    result = main.fetch_data()
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)