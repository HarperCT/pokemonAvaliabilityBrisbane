from flask import Flask, jsonify
from flask_cors import CORS

import main


class DataAPI:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app, resources={
            r"/": {"origins": "https://harperct.github.io"},
            r"/api/*": {"origins": "https://harperct.github.io"}
        })

        self.cached_data = None
        self.setup_routes()

        # Fetch the data once at startup
        self.fetch_and_cache_data()

    def fetch_and_cache_data(self):
        try:
            print("Fetching data for the first time...")
            self.cached_data = main.fetch_data()
            print("Data cached successfully!")
        except Exception as e:
            print("Error fetching initial data:", e)
            self.cached_data = {
                "status": "error",
                "message": "Failed to fetch initial data",
                "details": str(e)
            }

    def setup_routes(self):
        @self.app.route('/')
        def home_data():
            print("Home route accessed.")
            return {"message": "Welcome to the API!"}

        @self.app.route('/api/data')
        def get_data():
            print("API /api/data was hit.")
            return jsonify(self.cached_data)

    def run(self, host='0.0.0.0', port=5000):
        self.app.run(host=host, port=port)

if __name__ == '__main__':
    api = DataAPI()
    api.run()