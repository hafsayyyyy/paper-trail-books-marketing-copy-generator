
import os

from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import HTTPException

from models import init_db, insert_copy, fetch_history
from src.generator import generate_marketing_copy

app = Flask(__name__)

init_db()

REQUIRED_FIELDS = [
    "title",
    "author",
    "genre",
    "description",
    "audience",
]

FORMAT_TO_TYPE = {
    "tweet": "social",
    "email": "description",
    "flyer": "all",
}

CHECKLIST_KEYS = [
    "tone_matches_brand_voice",
    "appropriate_length",
    "brand_keywords_included",
]


def validate_book_details(data):
    """Return the required fields that are missing or invalid."""
    if not isinstance(data, dict):
        return REQUIRED_FIELDS[:]

    return [
        field
        for field in REQUIRED_FIELDS
        if not isinstance(data.get(field), str)
        or not data[field].strip()
    ]


def format_copy(copy_text, selected_format, book):
    """Format generated content for the selected marketing format."""

    if selected_format == "email":
        return (
            f"Subject: Discover {book['title']} by {book['author']}\n\n"
            "Hello, book lover!\n\n"
            f"{copy_text}\n\n"
            "Explore your next read with Paper Trail Books.\n\n"
            "Happy reading,\n"
            "Paper Trail Books"
        )

    if selected_format == "flyer":
        return (
            "PAPER TRAIL BOOKS PRESENTS\n\n"
            f"{book['title'].upper()}\n"
            f"By {book['author']}\n\n"
            f"{book['genre']} | For {book['audience']}\n\n"
            f"{copy_text}\n\n"
            "FIND YOUR NEXT GREAT READ\n"
            "Paper Trail Books"
        )

    # Return one post rather than the entire social-copy response.
    parts = copy_text.split("\n\n")
    first_post = parts[1] if len(parts) > 1 else copy_text
    first_post = first_post.strip()

    if first_post.startswith("1. "):
        first_post = first_post[3:]

    return first_post


@app.route("/", methods=["GET"])
def index():
    """Display the main application page."""
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    """Generate marketing copy for a book."""

    if not request.is_json:
        return jsonify(
            success=False,
            error="Content-Type must be application/json.",
        ), 415

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(
            success=False,
            error="A valid JSON object is required.",
        ), 400

    invalid_fields = validate_book_details(data)

    if invalid_fields:
        return jsonify(
            success=False,
            error="Please complete all required fields.",
            fields=invalid_fields,
        ), 400

    selected_format = data.get(
        "copy_format",
        data.get("format", "tweet"),
    )

    if selected_format not in FORMAT_TO_TYPE:
        return jsonify(
            success=False,
            error="Choose tweet, email, or flyer.",
        ), 400

    book = {
        key: data[key].strip()
        for key in REQUIRED_FIELDS
    }

    try:
        base_copy = generate_marketing_copy(
            **book,
            copy_type=FORMAT_TO_TYPE[selected_format],
        )

        final_copy = format_copy(
            base_copy,
            selected_format,
            book,
        )

        return jsonify(
            success=True,
            format=selected_format,
            copy=final_copy,
        ), 200

    except ValueError:
        app.logger.exception("Copy generation configuration/input error.")

        return jsonify(
            success=False,
            error=(
                "Could not generate copy. "
                "Check brand_voice.json and book details."
            ),
        ), 400

    except Exception:
        app.logger.exception("Copy generation failed.")

        return jsonify(
            success=False,
            error="Copy generation failed. Please try again.",
        ), 500


@app.route("/save", methods=["POST"])
def save_copy():
    """Validate and save generated copy and checklist to SQLite."""

    if not request.is_json:
        return jsonify(
            success=False,
            error="Content-Type must be application/json.",
        ), 415

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(
            success=False,
            error="A valid JSON object is required.",
        ), 400

    copy_text = data.get("copy")
    checklist = data.get("checklist")
    book = data.get("book")
    selected_format = data.get("format", "tweet")

    if not isinstance(copy_text, str) or not copy_text.strip():
        return jsonify(
            success=False,
            error="Marketing copy is required.",
        ), 400

    if not isinstance(book, dict) or validate_book_details(book):
        return jsonify(
            success=False,
            error="Valid book details are required.",
        ), 400

    if selected_format not in FORMAT_TO_TYPE:
        return jsonify(
            success=False,
            error="Choose tweet, email, or flyer.",
        ), 400

    if not isinstance(checklist, dict):
        return jsonify(
            success=False,
            error="A review checklist is required.",
        ), 400

    if not all(
        checklist.get(key) is True
        for key in CHECKLIST_KEYS
    ):
        return jsonify(
            success=False,
            error="Tick all three review checks before saving.",
        ), 400

    record = {
        "book": {
            key: book[key].strip()
            for key in REQUIRED_FIELDS
        },
        "format": selected_format,
        "copy": copy_text.strip(),
        "checklist": {
            key: checklist[key] is True
            for key in CHECKLIST_KEYS
        },
    }

    try:
        insert_copy(record)

        return jsonify(
            success=True,
            message="Copy and checklist saved successfully.",
        ), 200

    except Exception:
        app.logger.exception("Could not save copy to SQLite.")

        return jsonify(
            success=False,
            error="Unable to save copy on the server.",
        ), 500


@app.route("/history", methods=["GET"])
def history():
    """Display previously saved marketing copies."""
    try:
        records = fetch_history()
        return render_template("history.html", records=records)
    except Exception:
        app.logger.exception("Could not load saved history.")
        return "Unable to load saved history.", 500


@app.errorhandler(HTTPException)
def handle_http_error(error):
    """Return JSON errors for API endpoints."""

    if request.path in ("/generate", "/save"):
        return jsonify(
            success=False,
            error=error.description,
        ), error.code

    return error


@app.errorhandler(Exception)
def handle_unexpected_error(error):
    """Handle unexpected errors without exposing internal details."""

    app.logger.exception("Unexpected application error.")

    if request.path in ("/generate", "/save"):
        return jsonify(
            success=False,
            error="An unexpected server error occurred.",
        ), 500

    return "An unexpected server error occurred.", 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=os.environ.get("FLASK_DEBUG") == "1",
    )
