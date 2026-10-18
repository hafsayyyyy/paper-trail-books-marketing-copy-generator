
# Project Handover

## Project
Paper Trail Books Marketing Copy Generator

## GitHub Repository
https://github.com/hafsayyyyy/paper-trail-books-marketing-copy-generator

## Live Website
https://paper-trail-books-marketing-copy-generator.onrender.com/

## Technologies
- Python
- Flask
- Bootstrap
- SQLite
- Pytest
- Render

## Main Routes
- `/` - Home page and marketing copy generator
- `/generate` - Generate marketing copy
- `/save` - Save reviewed copy
- `/history` - View saved copy history

## Run Locally
1. Activate the virtual environment.
2. Install dependencies using `pip install -r requirements.txt`.
3. Run `python app.py`.
4. Open `http://127.0.0.1:5000`.

## Run Tests
`python -m pytest -q`

## Render Settings
Build Command: `pip install -r requirements.txt`

Start Command: `gunicorn app:app`

## Credentials
Configure API keys and secrets privately through environment variables. Never add real passwords or API keys to this file.

## Next Steps
1. Verify the Render deployment after pushing changes.
2. Test copy generation, saving, and the history page.
3. Consider persistent storage because SQLite data may not survive restarts on an ephemeral hosting filesystem.
