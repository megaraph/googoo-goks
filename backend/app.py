from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

import routes

if __name__ == "__main__":
    app.run(debug=True)
