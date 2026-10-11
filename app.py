
import os

from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import HTTPException

from src.generator import generate_marketing_copy

app = Flask(__name__)

REQUIRED_FIELDS = [
    "title",
    "author",
    "genre",
    "description",
    "audience",
]

COPY_TYPES = [
    "all",
    "description",
    "headlines",
    "social",
    "keywords",
]


def validate_book_details(data):
    """Validate the required book information."""

    if not isinstance(data, dict):
        return ["A valid JSON object is required."]

    invalid_fields = []

    for field in REQUIRED_FIELDS:
        value = data.get(field)

        if not isinstance(value, str) or not value.strip():
            invalid_fields.append(field)

    return invalid_fields


@app.route("/", methods=["GET", "POST"])
def index():
    """Display the web form and generate marketing copy."""

    result = None
    error = None

    if request.method == "POST":
        details = {
            field: request.form.get(field, "").strip()
            for field in REQUIRED_FIELDS
        }
        copy_type = request.form.get("copy_type", "all")
        invalid_fields = validate_book_details(details)

        if invalid_fields:
            error = "Please fill in all required fields."
        elif copy_type not in COPY_TYPES:
            error = "Please select a valid marketing content type."
        else:
            try:
                result = generate_marketing_copy(
                    **details,
                    copy_type=copy_type,
                )
            except Exception:
                app.logger.exception("Marketing copy generation failed.")
                error = (
                    "Unable to generate marketing copy. "
                    "Please check the brand voice configuration."
                )

    return render_template(
        "index.html",
        result=result,
        error=error,
    )


@app.route("/generate", methods=["POST"])
def generate():
    """Generate marketing copy through the JSON API."""

    if not request.is_json:
        return jsonify({
            "success": False,
            "error": "Content-Type must be application/json.",
        }), 415

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "error": "A valid JSON object is required.",
        }), 400

    invalid_fields = validate_book_details(data)

    if invalid_fields:
        return jsonify({
            "success": False,
            "error": "Required fields are missing or invalid.",
            "fields": invalid_fields,
        }), 400

    copy_type = data.get("copy_type", "all")

    if not isinstance(copy_type, str) or copy_type not in COPY_TYPES:
        return jsonify({
            "success": False,
            "error": "Invalid copy_type.",
            "allowed_types": COPY_TYPES,
        }), 400

    details = {
        field: data[field].strip()
        for field in REQUIRED_FIELDS
    }

    try:
        result = generate_marketing_copy(
            **details,
            copy_type=copy_type,
        )

        return jsonify({
            "success": True,
            "copy_type": copy_type,
            "copy": result,
            "marketing_copy": result,
        }), 200

    except ValueError:
        app.logger.exception("Marketing copy validation or configuration error.")
        return jsonify({
            "success": False,
            "error": "Unable to generate copy due to invalid input or configuration.",
        }), 400

    except Exception:
        app.logger.exception("Marketing copy generation failed.")
        return jsonify({
            "success": False,
            "error": "Marketing copy generation failed. Please try again.",
        }), 500


@app.errorhandler(HTTPException)
def handle_http_error(error):
    """Return JSON errors for API requests."""

    if request.path == "/generate":
        return jsonify({
            "success": False,
            "error": error.description,
        }), error.code

    return error


@app.errorhandler(Exception)
def handle_unexpected_error(error):
    """Return a JSON response for unexpected API failures."""

    app.logger.exception("Unexpected application error.")

    if request.path == "/generate":
        return jsonify({
            "success": False,
            "error": "An unexpected server error occurred.",
        }), 500

    return "An unexpected server error occurred.", 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
