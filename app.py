
from flask import Flask, jsonify, render_template, request
from src.generator import generate_marketing_copy

app = Flask(__name__)

REQUIRED_FIELDS = [
    "title", "author", "genre", "description", "audience"
]

COPY_TYPES = ["all", "description", "headlines", "social", "keywords"]


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        details = {
            field: request.form.get(field, "").strip()
            for field in REQUIRED_FIELDS
        }

        if not all(details.values()):
            error = "Please fill in all fields."
        else:
            try:
                result = generate_marketing_copy(**details)
            except Exception:
                app.logger.exception("Marketing copy generation failed.")
                error = "Unable to generate marketing copy. Check API configuration."

    return render_template("index.html", result=result, error=error)


@app.route("/generate", methods=["POST"])
def generate():
    if not request.is_json:
        return jsonify({
            "success": False,
            "error": "Content-Type must be application/json."
        }), 415

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "error": "A valid JSON object is required."
        }), 400

    invalid_fields = [
        field for field in REQUIRED_FIELDS
        if not isinstance(data.get(field), str) or not data[field].strip()
    ]

    if invalid_fields:
        return jsonify({
            "success": False,
            "error": "Required fields are missing or invalid.",
            "fields": invalid_fields
        }), 400

    copy_type = data.get("copy_type", "all")

    if not isinstance(copy_type, str) or copy_type not in COPY_TYPES:
        return jsonify({
            "success": False,
            "error": "Invalid copy_type.",
            "allowed_types": COPY_TYPES
        }), 400

    details = {
        field: data[field].strip()
        for field in REQUIRED_FIELDS
    }

    try:
        result = generate_marketing_copy(
            **details,
            copy_type=copy_type
        )

        return jsonify({
            "success": True,
            "copy_type": copy_type,
            "marketing_copy": result
        }), 200

    except ValueError as exc:
        if "OPENAI_API_KEY is missing" in str(exc):
            return jsonify({
                "success": False,
                "error": str(exc)
            }), 503

        app.logger.exception("Configuration error.")
        return jsonify({
            "success": False,
            "error": "Marketing copy configuration is invalid."
        }), 500

    except Exception:
        app.logger.exception("Marketing copy generation failed.")
        return jsonify({
            "success": False,
            "error": "Marketing copy generation failed. Please try again."
        }), 502


if __name__ == "__main__":
    app.run(debug=True)
