import os
from openai import OpenAI


COPY_TYPE_INSTRUCTIONS = {
    "all": """
        Generate all of the following:
        1. An engaging book description
        2. Three marketing headlines
        3. Five promotional social media captions
        4. Seven relevant marketing keywords
    """,
    "description": """
        Generate only one engaging book description suitable for
        a book listing. Do not include headlines, social media posts,
        or keywords.
    """,
    "headlines": """
        Generate only five catchy marketing headlines for the book.
        Do not include the book description, social media posts,
        or keywords.
    """,
    "social": """
        Generate only five promotional social media posts.
        Make them engaging and suitable for the target audience.
        Do not include the book description, headlines, or keywords.
    """,
    "keywords": """
        Generate only seven relevant marketing keywords or short
        keyword phrases for book discovery and search.
        Do not include the book description, headlines, or social posts.
    """,
}


def generate_marketing_copy(
    title,
    author,
    genre,
    description,
    audience,
    copy_type="all",
):
    """Generate book marketing content using the OpenAI API."""

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is missing. Please configure your API key."
        )

    if copy_type not in COPY_TYPE_INSTRUCTIONS:
        raise ValueError(
            f"Invalid copy_type: {copy_type}. "
            f"Choose from {', '.join(COPY_TYPE_INSTRUCTIONS)}."
        )

    client = OpenAI(api_key=api_key)

    prompt = f"""
Create marketing content for a book using these details.

Book title: {title}
Author: {author}
Genre: {genre}
Book description: {description}
Target audience: {audience}

Content to generate:
{COPY_TYPE_INSTRUCTIONS[copy_type]}

Keep the writing engaging, accurate, and suitable for the target
audience. Do not invent plot details that are not provided.
Use clear headings and readable formatting.
"""

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional book marketing copywriter."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content