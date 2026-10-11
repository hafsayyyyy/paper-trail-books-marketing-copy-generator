

import json
import re
from pathlib import Path


BRAND_VOICE_PATH = (
    Path(__file__).resolve().parent.parent / "brand_voice.json"
)


def load_brand_voice():
    """Load the brand's writing tone, style, and guidelines."""

    try:
        with BRAND_VOICE_PATH.open("r", encoding="utf-8") as file:
            brand_voice = json.load(file)
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(
            "Brand voice configuration is missing or invalid."
        ) from exc

    if not isinstance(brand_voice, dict):
        raise ValueError("Brand voice configuration must be a JSON object.")

    if not isinstance(brand_voice.get("guidelines"), list):
        raise ValueError("Brand voice guidelines must be a list.")

    return brand_voice


def generate_marketing_copy(
    title,
    author,
    genre,
    description,
    audience,
    copy_type="all",
):
    """Generate reader-focused marketing copy using brand guidelines."""

    title = title.strip()
    author = author.strip()
    genre = genre.strip()
    description = re.sub(r"\s+", " ", description).strip()
    audience = audience.strip()

    if not all([title, author, genre, description, audience]):
        raise ValueError("All book details are required.")

    valid_types = [
        "all",
        "description",
        "headlines",
        "social",
        "keywords",
    ]

    if copy_type not in valid_types:
        raise ValueError("Invalid marketing content type.")

    brand_voice = load_brand_voice()
    brand_name = brand_voice.get("brand_name", "Paper Trail Books")
    tone = brand_voice.get("tone", "warm and reader-focused")
    style = brand_voice.get("style", "clear and engaging")
    guidelines = [
        str(item).lower()
        for item in brand_voice["guidelines"]
    ]

    # Follow the brand guideline against inventing plot details.
    short_description = description.rstrip(".!?")

    book_description = (
        f"Discover {title} by {author,} "
        f"a {genre.lower()} book for {audience}. "
        f"{short_description}. "
        f"Find your next reading experience with {brand_name}."
    ).replace(f"by {author,}", f"by {author}")

    headlines = [
        f"Discover {title}: Your Next Reading Adventure",
        f"Explore {title} by {author}",
        f"A New {genre} Read to Add to Your List",
        f"Meet Your Next Read: {title}",
        f"Discover {title} with {brand_name}",
    ]

    social_posts = [
        f"Looking for your next read? Discover {title} by {author}, "
        f"a {genre.lower()} book for {audience}. #BookLovers #Reading",
        f"Meet {title} by {author}. Add this book to your reading list! "
        f"#BookRecommendation #Readers",
        f"Your next reading choice could be {title}. Explore it with "
        f"{brand_name}. #BookCommunity",
        f"Readers, discover {title} by {author} and share what you think. "
        f"#ReadingTime #BookLovers",
        f"Searching for a {genre.lower()} book? Take a look at {title} "
        f"by {author}. #ReadersCorner #Books",
    ]

    keywords = [
        title,
        author,
        genre,
        f"{genre} books",
        f"books for {audience}",
        "book recommendations",
        "reading list",
        brand_name,
    ]

    # Use the configured tone and style in the brand context.
    brand_context = (
        f"Brand: {brand_name}. Tone: {tone}. Style: {style}."
    )

    # Respect configured guidelines when constructing copy.
    if any("avoid misleading promotional claims" in item
           for item in guidelines):
        headlines = [
            headline.replace("Best-Selling", "").strip()
            for headline in headlines
        ]

    if any("do not invent facts or plot details" in item
           for item in guidelines):
        # Descriptions use only the supplied book details.
        book_description = (
            f"{brand_name} invites {audience} to discover "
            f"{title} by {author}, a {genre.lower()} book. "
            f"{short_description}. "
            f"Explore the book and decide if it belongs on your reading list."
        )

    content = {
        "description": (
            "BOOK DESCRIPTION\n\n"
            + book_description
            + "\n\n"
            + brand_context
        ),
        "headlines": (
            "MARKETING HEADLINES\n\n"
            + "\n".join(
                f"{i}. {headline}"
                for i, headline in enumerate(headlines, 1)
            )
            + "\n\n"
            + brand_context
        ),
        "social": (
            "SOCIAL MEDIA POSTS\n\n"
            + "\n\n".join(
                f"{i}. {post}"
                for i, post in enumerate(social_posts, 1)
            )
            + "\n\n"
            + brand_context
        ),
        "keywords": (
            "MARKETING KEYWORDS\n\n"
            + ", ".join(keywords)
            + "\n\n"
            + brand_context
        ),
    }

    if copy_type == "all":
        return "\n\n".join(content[key] for key in content)

    return content[copy_type]
