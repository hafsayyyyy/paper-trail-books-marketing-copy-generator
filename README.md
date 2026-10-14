# Paper Trail Books Marketing Copy Generator

A Flask-based web application that helps authors and publishers create promotional marketing copy for books. Users can enter book details, select a marketing format, generate copy, review the result, and save approved content with a review checklist.

## 1. Project Overview

The Paper Trail Books Marketing Copy Generator simplifies the process of preparing promotional content for books. It provides a web interface where users can enter book information and generate marketing copy suited to the selected format.

The application includes a Flask web interface, a JSON API, brand voice configuration, input validation, error handling, automated tests, and a local save workflow.

## 2. Objectives

- Generate promotional content for books.
- Provide a simple and user-friendly web interface.
- Maintain consistent brand voice guidelines.
- Accept book information through a web form and API.
- Validate user input and handle errors.
- Allow users to review generated copy before saving.
- Save marketing copy with its review checklist.
- Support automated testing and clear documentation.

## 3. Features

- Flask-based web application.
- Book title, author, genre, description, and target audience fields.
- Multiple marketing content formats.
- Brand voice configuration through `brand_voice.json`.
- Input validation and error handling.
- Editable generated marketing copy.
- Review checklist before saving.
- Save workflow for marketing copy and checklist data.
- Local JSON storage using `saved_copies.json`.
- JSON API endpoint: `POST /generate`.
- Automated tests using pytest.
- Git and GitHub version control.

### Marketing Formats

The web interface provides these marketing formats:

- Tweet / Social Post
- Email
- Flyer

The available formats and the generated content depend on the current application implementation.

## 4. Technologies Used

- Python
- Flask
- HTML
- CSS
- JavaScript
- Jinja2 templates
- JSON
- Pytest
- Git and GitHub

## 5. Project Structure

```text
paper-trail-books-marketing-copy-generator/
├── app.py
├── brand_voice.json
├── requirements.txt
├── README.md
├── .gitignore
├── src/
│   └── generator.py
├── templates/
│   └── index.html
└── tests/
    └── test_generator.py
```

Additional local files may exist during development. Backup files are not required for the normal application workflow.

## 6. Prerequisites

Before running the application, install:

- Python 3.10 or a compatible version supported by the dependencies.
- pip.
- Git.

Check your Python installation:

```powershell
python --version
```

## 7. Installation

### Step 1: Clone the repository

```powershell
git clone https://github.com/hafsayyyyy/paper-trail-books-marketing-copy-generator.git
```

### Step 2: Navigate to the project folder

```powershell
cd paper-trail-books-marketing-copy-generator
```

### Step 3: Create a virtual environment

```powershell
python -m venv .venv
```

### Step 4: Activate the virtual environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 5: Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 8. Running the Application

Start the Flask application:

```powershell
python app.py
```

Open the following address in your browser:

```text
http://127.0.0.1:5000
```

Keep the terminal open while using the application.

## 9. Using the Web Interface

1. Enter the book title.
2. Enter the author's name.
3. Select the book genre.
4. Enter the target audience.
5. Provide a description of the book.
6. Select a marketing format.
7. Generate the marketing copy.
8. Review and edit the generated content if needed.
9. Complete all required review checklist items.
10. Click **Save Copy** to save the copy and checklist.

The application validates required fields and provides feedback when generation or saving fails.

### Review Checklist

Before saving, users are asked to review the following:

- The tone matches the brand voice.
- The copy has an appropriate length.
- Brand keywords are included.

The save workflow requires all checklist items to be completed.

## 10. Saving Marketing Copy

The application provides a save endpoint:

`POST /save`

The save workflow accepts marketing copy, book details, the selected format, and the review checklist.

When the request is valid, the application stores the saved record in:

```text
saved_copies.json
```

The saved record includes information such as:

- Save timestamp.
- Book details.
- Selected marketing format.
- Marketing copy.
- Review checklist.

The JSON file is local application data and is excluded from Git version control through `.gitignore`.

**Note:** Local JSON storage is suitable for a simple development workflow. It is not a substitute for a production database, and files stored on temporary hosting instances may not persist across restarts or redeployments.

## 11. API Documentation

### Generate Marketing Copy

**Endpoint:** `POST /generate`

**Content-Type:** `application/json`

The endpoint accepts book information and a marketing content type. The application validates the input and returns generated copy or an error response.

### Example Request

```json
{
  "title": "The Silent Garden",
  "author": "A. Khan",
  "genre": "Mystery",
  "description": "A mystery novel about secrets hidden in an old garden.",
  "audience": "Young adults",
  "copy_type": "all"
}
```

The accepted fields and marketing type values depend on the current implementation of `app.py` and `src/generator.py`.

### Example PowerShell Request

Make sure the Flask application is running first.

```powershell
$body = @{
    title = "The Silent Garden"
    author = "A. Khan"
    genre = "Mystery"
    description = "A mystery novel about secrets hidden in an old garden."
    audience = "Young adults"
    copy_type = "all"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:5000/generate" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

### Example Response

The following is an illustrative example. Actual response fields and content depend on the application's implementation.

```json
{
  "success": true,
  "copy": "Example marketing copy for the book."
}
```

### Error Handling

The application validates requests and returns error responses for invalid input or generation failures. The exact HTTP status codes and response fields should match the implementation in `app.py`.

## 12. Brand Voice Configuration

The project includes a `brand_voice.json` file for configuring brand voice guidelines.

These guidelines may define the preferred tone, style, personality, and writing rules for marketing content.

Update the file carefully and test the application after making changes. The effect of each setting depends on how `src/generator.py` reads and applies the configuration.

## 13. Testing

The project uses pytest for automated tests.

Run the test suite:

```powershell
python -m pytest -q
```

For detailed test output:

```powershell
python -m pytest -v
```

Review the results after making code changes. Report only the test results that were actually observed.

## 14. Deployment

The project can be deployed to a compatible Python hosting service, such as Render.

A typical deployment workflow is:

1. Push the code to GitHub.
2. Create or select a compatible web service.
3. Configure the repository and build command.
4. Configure the appropriate start command.
5. Add any required environment variables.
6. Deploy the application.
7. Test the live web interface and API.
8. Review application logs if errors occur.

The local development command is:

```text
python app.py
```

For production, follow the hosting provider's instructions for the start command, port configuration, and production WSGI server.

A successful GitHub push does not automatically confirm that the latest changes have been deployed. Verify the deployment in the hosting dashboard.

## 15. Troubleshooting

### Application Does Not Start

Activate the virtual environment and install the dependencies:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

### Marketing Copy Does Not Generate

- Check that all required book fields are filled in.
- Check the terminal for error messages.
- Verify that `brand_voice.json` is present and valid.
- Review the current generator implementation and its configuration requirements.

### Saving Fails

- Confirm that marketing copy has been generated.
- Complete all required review checklist items.
- Check the response message in the web interface.
- Check the Flask terminal for errors.
- Ensure the application can write to its local project directory.

### Tests Fail

Run:

```powershell
python -m pytest -v
```

Review the failure details and check the relevant source code and dependencies.

## 16. Security and Data Considerations

- Do not commit API keys, passwords, or other secrets.
- Keep `.env` files out of Git version control.
- Do not commit local generated data such as `saved_copies.json`.
- Validate incoming API requests.
- Avoid exposing sensitive internal error details.
- Review generated content before publishing it commercially.
- Use persistent storage or a database if saved records must survive production redeployments.

## 17. Limitations

- Marketing copy quality depends on the configured generation method and supplied book details.
- Generated content should be reviewed before publication.
- Local JSON storage is not designed for concurrent multi-user production workloads.
- Deployment configuration may require adjustments for the selected hosting provider.
- Passing automated tests does not guarantee that every live deployment scenario works correctly.

## 18. Future Improvements

Potential improvements include:

- Additional marketing formats.
- More brand voice presets.
- Export options for saved content.
- Persistent database storage.
- Improved accessibility and responsive design.
- Additional automated tests.
- Production-ready deployment configuration.
- Improved logging and monitoring.

## 19. Conclusion

The Paper Trail Books Marketing Copy Generator demonstrates a Flask-based workflow for creating, reviewing, and saving promotional content for books.

The project combines a web interface, book information forms, brand voice configuration, input validation, a JSON API, a review checklist, local saving, and automated tests.

## 20. Repository

GitHub repository:

https://github.com/hafsayyyyy/paper-trail-books-marketing-copy-generator
