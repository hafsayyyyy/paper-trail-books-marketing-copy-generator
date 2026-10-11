# Paper Trail Books Marketing Copy Generator

A Flask-based application that generates book marketing copy using the OpenAI API. It follows the brand voice and guidelines defined in `brand_voice.json`.

## Features

* Generate engaging book descriptions.
* Create three promotional headlines.
* Generate five social media captions.
* Suggest seven relevant keywords.
* Generate all content types together.
* Validate required input fields.
* Provide a JSON API for marketing copy generation.

## Requirements

* Python 3.11 or compatible version
* OpenAI API key with available API access and credits

## Local Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/hafsayyyyy/paper-trail-books-marketing-copy-generator.git
   cd paper-trail-books-marketing-copy-generator
   ```

2. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add:

   ```text
   OPENAI_API_KEY=your_api_key_here
   OPENAI_MODEL=gpt-4o-mini
   ```

   Replace the placeholder with your own valid API key. Never commit the `.env` file or share your API key.

5. Start the application:

   ```bash
   python app.py
   ```

6. Open `http://127.0.0.1:5000` in your browser.

## JSON API

**Endpoint:** `POST /generate`

**Content-Type:** `application/json`

Example request:

```json
{
  "title": "The Lost World",
  "author": "John Smith",
  "genre": "Adventure",
  "description": "A journey into a mysterious world.",
  "audience": "Young adults",
  "copy_type": "all"
}
```

Supported `copy_type` values:

* `all`
* `description`
* `headlines`
* `social`
* `keywords`

The API returns generated copy as JSON. Invalid input produces an appropriate error response.

## Run Tests

```powershell
python -m pytest -q
```

The tests cover missing API-key handling and API input validation. They do not require a successful live OpenAI API call.

## Limitations

* A valid OpenAI API key and available API credits are required for live generation.
* Generated marketing copy should be reviewed before publication.
* The application does not independently verify book facts.
* No production deployment or authentication is configured by default.
