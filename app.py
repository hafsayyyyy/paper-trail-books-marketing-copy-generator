
import os
import json
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import HTTPException

from src.generator import generate_marketing_copy

app = Flask(__name__)

SAVE_FILE = Path(__file__).resolve().parent / "saved_copies.json"

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
    if not isinstance(data, dict):
        return ["A valid JSON object is required."]

    return [
        field
        for field in REQUIRED_FIELDS
        if not isinstance(data.get(field), str)
        or not data[field].strip()
    ]


@app.route("/", methods=["GET", "POST"])
def index():
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
                error = "Unable to generate marketing copy. Please check your configuration."

    return render_template("index.html", result=result, error=error)


@app.route("/generate", methods=["POST"])
def generate():
    if not request.is_json:
        return jsonify({
            "success": False,
            "error": "Content-Type must be application/json.",
        }), 415

    data = request.get_json(silent=True)
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
        app.logger.exception("Invalid input or configuration.")
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


@app.route("/save", methods=["POST"])
def save_copy():
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

    copy = data.get("copy")
    checklist = data.get("checklist")
    book = data.get("book")

    if not isinstance(copy, str) or not copy.strip():
        return jsonify({
            "success": False,
            "error": "Marketing copy is required.",
        }), 400

    if not isinstance(checklist, dict):
        return jsonify({
            "success": False,
            "error": "A review checklist is required.",
        }), 400

    required_checks = [
        "tone_matches_brand_voice",
        "appropriate_length",
        "brand_keywords_included",
    ]

    if not all(checklist.get(key) is True for key in required_checks):
        return jsonify({
            "success": False,
            "error": "Complete all review checks before saving.",
        }), 400

    if not isinstance(book, dict):
        return jsonify({
            "success": False,
            "error": "Book details are required.",
        }), 400

    record = {
        "saved_at": datetime.now(timezone.utc).isoformat(),
        "book": book,
        "format": data.get("format", "all"),
        "copy": copy.strip(),
        "checklist": checklist,
    }

    try:
        if SAVE_FILE.exists():
            with SAVE_FILE.open("r", encoding="utf-8") as file:
                records = json.load(file)
            if not isinstance(records, list):
                raise ValueError("Saved data must be a JSON list.")
        else:
            records = []

        records.append(record)

        with SAVE_FILE.open("w", encoding="utf-8") as file:
            json.dump(records, file, indent=2, ensure_ascii=False)

        return jsonify({
            "success": True,
            "message": "Marketing copy and review checklist saved.",
        }), 200

    except (OSError, json.JSONDecodeError, ValueError):
        app.logger.exception("Unable to save marketing copy.")
        return jsonify({
            "success": False,
            "error": "Unable to save the copy on the server.",
        }), 500


@app.errorhandler(HTTPException)
def handle_http_error(error):
    if request.path in ("/generate", "/save"):
        return jsonify({
            "success": False,
            "error": error.description,
        }), error.code
    return error


@app.errorhandler(Exception)
def handle_unexpected_error(error):
    app.logger.exception("Unexpected application error.")

    if request.path in ("/generate", "/save"):
        return jsonify({
            "success": False,
            "error": "An unexpected server error occurred.",
        }), 500

    return "An unexpected server error occurred.", 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="127.0.0.1", port=port, debug=True)