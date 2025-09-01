from flask import Flask, jsonify
from flask_cors import CORS

import main

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://harperct.github.io"}})

@app.route('/')
def home_data():
    print("wow you found my home dir! Nice!!")

@app.route('/api/data')
def get_data():
    print("API was hit!")
    try:
        result = main.fetch_data()
        print(f"Got result: {result}")
        return jsonify(result)
    except Exception as e:
        print("Failed fetching:", e)
        return jsonify({
            "status": "error",
            "message": "Failed to fetch data",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)