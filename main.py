
from flask import Flask, render_template, request, jsonify
import requests

from model import analyze_job_offer, AVAILABLE_MODELS
from tools import validate_job_text, get_safety_tips

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}

    job_text = data.get("text", "")
    selected_model = data.get("model", "Gemma")

    valid, message = validate_job_text(job_text)

    if not valid:
        return jsonify({"error": message}), 400

    if selected_model not in AVAILABLE_MODELS and selected_model != "Both":
        return jsonify({"error": "Please select a valid model."}), 400

    try:
        if selected_model == "Both":
            results = {}

            for name in AVAILABLE_MODELS:
                try:
                    results[name] = analyze_job_offer(job_text, name)
                except requests.RequestException:
                    results[name] = "Model unavailable. Check Ollama."

            return jsonify({
                "results": results,
                "safety_tips": get_safety_tips()
            })

        result = analyze_job_offer(job_text, selected_model)

        return jsonify({
            "result": result,
            "model": selected_model,
            "safety_tips": get_safety_tips()
        })

    except requests.RequestException:
        return jsonify({
            "error": "Cannot connect to Ollama. Make sure Ollama is running."
        }), 503


if __name__ == "__main__":
    app.run(debug=True)
