
import os
from openai import OpenAI


def generate_marketing_copy(title, author, genre, description, audience):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing. Please configure it in your .env file.")

    client = OpenAI(api_key=api_key)

    prompt = f"""
    Create marketing copy for a book using these details:

    Book title: {title}
    Author: {author}
    Genre: {genre}
    Book description: {description}
    Target audience: {audience}

    Generate:
    1. An engaging book description
    2. Three marketing headlines
    3. Five promotional social media captions
    4. Seven relevant keywords

    Keep the writing engaging, accurate, and suitable for the target audience.
    Do not invent plot details that are not provided.
    """

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {
                "role": "system",
                "content": "You are a professional book marketing copywriter."
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content
