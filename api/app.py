from flask import Flask, request, jsonify
from flask_cors import CORS
from engine.analyzer import analyze
from ai.explain import generate_explanation


app = Flask(__name__)
CORS(app)


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "API running"}), 200


@app.route("/analyze", methods=["POST"])
def analyze_medicine():

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    try:
        # 1️⃣ Deterministic Safety Engine
        result = analyze(data)

        # If engine returns validation error → do NOT call AI
        if "error" in result:
            return jsonify(result), 400

        # 2️⃣ AI Explanation Layer
        explanation = generate_explanation(result)

        result["ai_explanation"] = explanation

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
