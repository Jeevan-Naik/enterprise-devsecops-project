from app.config.settings import APP_VERSION, APP_PORT
from flask import Flask, jsonify
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route("/")
def home():
    app.logger.info("Home endpoint called")
    return jsonify({
        "application": "Employee Management API",
        "version": APP_VERSION
    })

@app.route("/health")
def health():
    app.logger.info("Health endpoint called")
    return jsonify({
        "status": "UP"
    })

@app.route("/version")
def version():
    app.logger.info("Version endpoint called")
    return jsonify({
        "version": APP_VERSION
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=APP_PORT)