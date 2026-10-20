# Paper Trail Books Marketing Copy Generator

## Project Overview

Paper Trail Books Marketing Copy Generator is a Flask-based web application that helps users create, review, and save marketing content for books. It provides a simple Bootstrap interface and stores approved marketing copies in an SQLite database so users can access their previous work through the History page.

## Features

- Generate book marketing copy using book details and brand voice.
- Support multiple marketing formats, including tweets, emails, and flyers.
- Collect book title, author, genre, target audience, and book description.
- Validate required form fields before generating content.
- Generate content without reloading the webpage.
- Display generated copy in an editable text area.
- Review generated copy using a checklist.
- Check tone, appropriate length, and inclusion of brand keywords.
- Save reviewed marketing copies to an SQLite database.
- Store book details, marketing format, generated copy, and checklist status.
- View previously saved entries on the `/history` page.
- Use a responsive Bootstrap interface.
- Provide JSON responses through the Flask API.
- Run automated tests using pytest.
- Deploy the application to Render.

## Technologies Used

- Python 3.11 or compatible version
- Flask
- SQLite
- HTML5 and CSS3
- Bootstrap
- JavaScript Fetch API
- python-dotenv
- OpenAI Python package, if configured for the selected generation method
- pytest
- Gunicorn
- Git and GitHub
- Render

## Project Requirements

Install Python and Git before running the project locally.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/hafsayyyyy/paper-trail-books-marketing-copy-generator.git
cd paper-trail-books-marketing-copy-generator
```

### 2. Create a Virtual Environment

On Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

If the application uses an API key, create a `.env` file in the project root and add the required environment variable using the name expected by `app.py`.

Example:

```text
OPENAI_API_KEY=your_api_key_here
```

Replace the placeholder with your own valid key. Never commit real API keys or other secrets to GitHub.

If the application is configured to generate copy without an external API, follow the configuration used by the current application.

## Run the Application Locally

Start the Flask application:

```bash
python app.py
```

Open the local address displayed by Flask in your browser. The default development address is usually:

```text
http://127.0.0.1:5000
```

Keep the terminal running while using the application.

## How to Use the Application

1. Open the application homepage.
2. Enter the book title and author.
3. Select the book genre.
4. Enter the target audience and book description.
5. Select the required marketing format.
6. Click the Generate button.
7. Review the generated marketing copy.
8. Complete the review checklist.
9. Click Save to store the reviewed copy.
10. Open the History page to view saved entries.

The review checklist covers brand voice, appropriate content length, and brand keyword inclusion.

## Application Routes

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Displays the main application page |
| `/generate` | POST | Generates marketing copy |
| `/save` | POST | Saves reviewed marketing copy |
| `/history` | GET | Displays previously saved entries |

The `/generate` and `/save` endpoints accept JSON requests where required and return JSON responses.

## SQLite Database

The application uses SQLite to store saved marketing copies.

Each saved record should include the available fields required by the application, including:

- Book title
- Author
- Marketing format
- Generated marketing copy
- Review checklist status

The database is used to retrieve previously saved records on the History page.

The database file may be created automatically by the application. Do not assume that a local database file is automatically included in the deployed environment.

For Render deployment, confirm that the database is stored on persistent storage if saved records must survive service restarts or redeployments. A database stored only on an ephemeral filesystem may be lost when the service restarts or is redeployed.

## Run Automated Tests

Run the project's tests with:

```bash
python -m pytest -q
```

The project has previously passed its four available automated tests. Run the command again after making changes to verify the current code.

## GitHub Repository

Repository:

https://github.com/hafsayyyyy/paper-trail-books-marketing-copy-generator

The source code, project documentation, and deployment configuration are maintained in this repository.

## Deployment on Render

The application is deployed on Render.

Live application:

https://paper-trail-books-marketing-copy.onrender.com

### Deployment Configuration

1. Push the latest project changes to GitHub.
2. Open the Render Dashboard.
3. Select the web service connected to the repository.
4. Confirm the required environment variables.
5. Set the build command to:

   ```bash
   pip install -r requirements.txt
   ```

6. Set the start command to:

   ```bash
   gunicorn app:app
   ```

7. Deploy the latest commit.
8. Review the deployment logs for build and startup errors.
9. Open the live URL and test the homepage, generation, saving, and History page.

Render provides the port through the `PORT` environment variable. The production server must listen on the port configured by the hosting platform.

### Deployment Verification

The latest deployment logs showed a successful build and Gunicorn startup. The homepage returned HTTP 200, and the service reported that it was live.

The generation, save, and history workflows should also be tested on the live service after deployment.

## Troubleshooting

### Application Does Not Start

- Confirm that the virtual environment is activated.
- Install dependencies using `pip install -r requirements.txt`.
- Check the terminal for Python errors.
- Confirm that the configured start command matches the Flask application module.

### Marketing Copy Is Not Generated

- Check that all required form fields are filled in.
- Review the application logs.
- If an external API is configured, confirm that the API key is valid and available to the application.

### Save Request Fails

- Confirm that marketing copy has been generated.
- Complete all required review checklist items.
- Check the response from the `/save` endpoint and the application logs.

### History Page Is Empty

- Generate and save a new marketing copy.
- Refresh the History page.
- Check that the save request succeeded and that the application is reading from the expected database.

### Saved Records Disappear After Deployment

Check whether the deployed SQLite database is stored on persistent storage. Configure a persistent disk or another suitable persistent database solution if required by the hosting environment.

## Client Handover Note

The Paper Trail Books Marketing Copy Generator provides a web interface for creating, reviewing, and saving book marketing content. Users can generate copy in supported formats, review it using the checklist, and view saved entries through the History page. The application is hosted on Render, and its source code is maintained on GitHub.

The client should maintain access to the GitHub repository and Render service, configure any required API credentials securely, and monitor deployment logs when troubleshooting. SQLite persistence should be verified against the hosting configuration to ensure saved records are retained across restarts and redeployments.

Before making future changes, run the automated tests and verify the live generation, save, and history workflows.

## Project Status

The application has been deployed successfully. The homepage and History page have been opened, and a generated marketing copy has been saved and verified in the History page. The repository was reported to be synchronized with `origin/main` with a clean working tree.

Final completion should be confirmed by running the tests against the latest code and verifying database persistence on Render.

## License

Add the appropriate license if the project is to be distributed or reused publicly.
