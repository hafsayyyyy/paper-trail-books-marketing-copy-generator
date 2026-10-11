
# Paper Trail Books Marketing Copy Generator

An AI-powered book marketing copy generator built with Python, Flask, and a Large Language Model (LLM) API. The application helps authors and publishers create marketing content based on book information and configured brand voice guidelines.

## 1. Project Overview

The Paper Trail Books Marketing Copy Generator is a Python-based application that automates the creation of promotional content for books.

Users provide information such as the book title, author, genre, description, and target audience. The application uses an LLM API to generate marketing content tailored to the selected content type and the project's brand voice configuration.

The project includes an interactive Flask web interface and a JSON-based HTTP API.

## 2. Objectives

- Automate book marketing content generation.
- Integrate an LLM API into a Python application.
- Maintain a consistent brand voice.
- Provide a user-friendly web interface.
- Provide an HTTP API for programmatic access.
- Validate input data and handle errors.
- Support automated testing.
- Document installation, usage, and deployment.

## 3. Features

- AI-powered marketing copy generation.
- Flask web application.
- JSON API endpoint.
- Configurable brand voice using `brand_voice.json`.
- Multiple marketing content types.
- Required-field validation.
- JSON request validation.
- Error handling for configuration and generation failures.
- Copy-to-clipboard functionality for generated content.
- Print-friendly results.
- Environment-variable-based API configuration.
- Automated tests using pytest.

### Supported Marketing Content Types

| Type | Description |
|---|---|
| `all` | All supported marketing content |
| `description` | Book marketing description |
| `headlines` | Promotional headlines |
| `social` | Social media marketing content |
| `keywords` | Marketing keywords |

The exact generated content depends on the configured generator and brand voice instructions.

## 4. Technologies Used

- Python
- Flask
- Large Language Model API
- HTML and CSS
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
├── src/
│   └── generator.py
├── templates/
│   └── index.html
├── tests/
│   └── test_generator.py
└── .gitignore
```

The structure above illustrates the main project components. Additional source files, tests, and configuration files may be present in the repository.

## 6. Prerequisites

Before running the project, make sure you have:

- Python 3.10 or a compatible version supported by the dependencies.
- pip.
- Git.
- An API key for the configured LLM provider.
- An active provider account with sufficient API credits, if required.

## 7. Installation

### Step 1: Clone the Repository

```powershell
git clone https://github.com/hafsayyyyy/paper-trail-books-marketing-copy-generator.git
```

### Step 2: Navigate to the Project

```powershell
cd paper-trail-books-marketing-copy-generator
```

### Step 3: Create a Virtual Environment

```powershell
python -m venv .venv
```

### Step 4: Activate the Environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 5: Install Dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 8. Environment Configuration

The application may require an API key to communicate with the configured LLM provider.

For a Windows PowerShell session, set the required environment variable:

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

If the application supports model configuration through `OPENAI_MODEL`, set it as follows:

```powershell
$env:OPENAI_MODEL="gpt-4o-mini"
```

Replace the example API key with your own valid key.

These PowerShell environment variables apply to the current terminal session. Set them again in a new session when necessary.

### Security Notes

- Never publish API keys in source code or README examples.
- Never commit `.env` files containing secrets.
- Add local secret files to `.gitignore`.
- Configure deployment secrets through the hosting provider's environment-variable settings.
- Do not share API credentials in screenshots, logs, or public repositories.

## 9. Running the Web Application

After installing dependencies and configuring the required API credentials, start the application:

```powershell
python app.py
```

Open the following address in your browser:

```text
http://127.0.0.1:5000
```

### Using the Web Interface

1. Enter the book title.
2. Enter the author's name.
3. Select the book genre.
4. Enter the book description.
5. Specify the target audience.
6. Select the marketing content type.
7. Click **Generate Marketing Copy**.
8. Review the generated content or any displayed error message.
9. Use the copy or print options when results are available.

The application validates required fields before attempting generation.

Actual content generation depends on the configured LLM API, credentials, account credits, and provider availability.

## 10. API Documentation

### Endpoint

`POST /generate`

The endpoint accepts a JSON request and returns generated marketing content or an error response.

### Required Fields

| Field | Type | Description |
|---|---|---|
| `title` | String | Book title |
| `author` | String | Author name |
| `genre` | String | Book genre |
| `description` | String | Description of the book |
| `audience` | String | Intended target audience |

### Optional Field

| Field | Type | Default | Description |
|---|---|---|---|
| `copy_type` | String | `all` | Selects the marketing content type |

Supported `copy_type` values are `all`, `description`, `headlines`, `social`, and `keywords`.

### Example JSON Request

```json
{
  "title": "The Silent Garden",
  "author": "A. Khan",
  "genre": "Mystery",
  "description": "A mystery novel about secrets hidden in an old garden.",
  "audience": "Young adults",
  "copy_type": "headlines"
}
```

### Example PowerShell Request

Make sure the Flask application is running before sending this request.

```powershell
$body = @{
    title = "The Silent Garden"
    author = "A. Khan"
    genre = "Mystery"
    description = "A mystery novel about secrets hidden in an old garden."
    audience = "Young adults"
    copy_type = "headlines"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:5000/generate" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

### Successful Response Structure

A successful response has the following general structure:

```json
{
  "success": true,
  "copy_type": "headlines",
  "marketing_copy": "Generated marketing content appears here."
}
```

The example content is illustrative and is not a guaranteed generation result.

### Error Responses

The API validates the request and handles common failures.

| HTTP Status | Meaning |
|---|---|
| `200` | Request processed successfully |
| `400` | Invalid JSON object or missing/invalid required fields |
| `415` | Request is not sent as JSON |
| `500` | Configuration or unexpected internal error |
| `502` | Marketing content generation failed |
| `503` | Required API credentials are missing |

The exact response message depends on the error encountered.

## 11. Brand Voice Configuration

The project includes a `brand_voice.json` configuration file.

This file is intended to define writing guidelines that help keep generated marketing content consistent with the desired brand identity.

Depending on the current generator implementation, the configuration may specify:

- Preferred tone.
- Writing style.
- Brand personality.
- Language preferences.
- Content guidelines.

Update the configuration carefully to match the project's requirements. The effect of each setting depends on how the generator reads and applies it.

## 12. Input Validation and Error Handling

The application checks that required book fields are present and contain valid text before generation.

The JSON API also checks:

- Whether the request uses the expected content type.
- Whether the request body is a valid JSON object.
- Whether required fields contain non-empty strings.
- Whether `copy_type` is supported.

The application handles common generation problems, including:

- Missing API credentials.
- Invalid configuration.
- External API failures.
- Insufficient provider credits or usage limits.
- Unexpected generation errors.

Error messages are returned without intentionally exposing secret credentials.

## 13. Testing

The project uses pytest for automated testing.

Run the tests from the project directory:

```powershell
python -m pytest -q
```

To run the tests with more detailed output:

```powershell
python -m pytest -v
```

Tests should be run after code changes to verify supported functionality and prevent regressions.

Record only the test results that were actually observed. Passing automated tests do not necessarily confirm that the external LLM service is available or that a live API request will succeed.

## 14. Troubleshooting

### Application Does Not Start

Confirm that the virtual environment is activated and the dependencies are installed.

```powershell
python -m pip install -r requirements.txt
python app.py
```

### API Key Is Missing

Set the required environment variable in the terminal before starting the application.

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
python app.py
```

### Generation Fails

Check the following:

- The API key is valid.
- The configured model is available to the account.
- The account has sufficient API credits.
- The internet connection is working.
- The provider has not reported an outage or usage limit.

### Tests Fail

Run:

```powershell
python -m pytest -v
```

Review the error output and check whether a dependency, configuration setting, or source-code change caused the failure.

## 15. Deployment

The application can be prepared for deployment to a compatible Python hosting service.

A typical deployment process includes:

1. Push the project to a public GitHub repository.
2. Select a hosting provider that supports Python and Flask.
3. Configure the build and start commands according to the provider's instructions.
4. Add required environment variables through the provider's dashboard.
5. Deploy the application.
6. Open the deployed URL and test the web interface.
7. Test the API endpoint and review application logs.

A typical start command for a basic Flask setup is:

```text
python app.py
```

However, production hosting may require a production WSGI server and a hosting-specific start command. The application must also listen on the port supplied by the hosting environment.

**Deployment status:** Deployment has not been confirmed by this README. Add a live deployment URL only after the application has been successfully deployed and tested.

## 16. Limitations

- Generation depends on an external LLM provider.
- A valid API key may be required.
- API usage limits and insufficient credits may prevent generation.
- Generated content may contain inaccurate or unsuitable claims.
- Output quality depends on the supplied book details and prompt instructions.
- Generated content should be reviewed before publication.
- A successful local test suite does not guarantee production readiness.
- Hosting availability, costs, and environment requirements depend on the selected provider.

## 17. Future Improvements

Potential improvements include:

- Additional marketing copy formats.
- More brand voice presets.
- Improved validation and feedback.
- More automated tests.
- Production-ready deployment configuration.
- Rate limiting and abuse protection.
- Better accessibility and responsive design.
- Saving and exporting generated content.
- Improved monitoring and error reporting.

## 18. Security Considerations

- Keep API keys outside the source code.
- Exclude `.env`, virtual environments, and cache files from version control.
- Validate incoming requests.
- Avoid exposing sensitive exception details to users.
- Configure secrets securely in deployment environments.
- Use a production-ready server for public deployments.
- Review generated content before using it commercially.

## 19. Conclusion

The Paper Trail Books Marketing Copy Generator demonstrates how Python, Flask, and an LLM API can be combined to automate book marketing content generation.

The project provides a web interface, a JSON API, configurable brand voice instructions, input validation, error handling, and automated testing. It offers a foundation for further improvements in content generation, usability, testing, and deployment.

## 20. Repository

GitHub repository:

https://github.com/hafsayyyyy/paper-trail-books-marketing-copy-generator