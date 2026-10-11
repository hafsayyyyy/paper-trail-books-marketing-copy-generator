
import os

from flask import Flask, jsonify, render_template, request
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

            except ValueError as exc:
                if "OPENAI_API_KEY is missing" in str(exc):
                    error = (
                        "OpenAI API key is missing. "
                        "Please configure your API key."
                    )
                else:
                    app.logger.exception(
                        "Marketing copy generation failed."
                    )
                    error = (
                        "Unable to generate marketing copy. "
                        "Check your API configuration and available credits."
                    )

            except Exception:
                app.logger.exception(
                    "Marketing copy generation failed."
                )
                error = (
                    "Unable to generate marketing copy. "
                    "Check your API configuration and available credits."
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
            "marketing_copy": result,
        }), 200

    except ValueError as exc:
        if "OPENAI_API_KEY is missing" in str(exc):
            return jsonify({
                "success": False,
                "error": str(exc),
            }), 503

        app.logger.exception(
            "Marketing copy configuration error."
        )

        return jsonify({
            "success": False,
            "error": "Marketing copy configuration is invalid.",
        }), 500

    except Exception:
        app.logger.exception(
            "Marketing copy generation failed."
        )

        return jsonify({
            "success": False,
            "error": (
                "Marketing copy generation failed. Please try again."
            ),
        }), 502


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
    )