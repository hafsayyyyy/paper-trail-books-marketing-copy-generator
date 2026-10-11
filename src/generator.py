
import re


def generate_marketing_copy(
    title,
    author,
    genre,
    description,
    audience,
    copy_type="all",
):
    """Generate marketing copy without a paid API."""

    title = title.strip()
    author = author.strip()
    genre = genre.strip()
    description = description.strip()
    audience = audience.strip()

    if not all([title, author, genre, description, audience]):
        raise ValueError("All book details are required.")

    if copy_type not in [
        "all",
        "description",
        "headlines",
        "social",
        "keywords",
    ]:
        raise ValueError("Invalid marketing content type.")

    short_description = re.sub(r"\s+", " ", description).strip()
    short_description = short_description.rstrip(".!?")

    book_description = (
        f"Discover {title} by {author}, a {genre.lower()} book "
        f"created for {audience}. {short_description}. "
        f"Explore a story shaped by its unique ideas, themes, "
        f"and experiences. Add {title} to your reading list "
        f"and discover what makes this book worth exploring."
    )

    headlines = [
        f"Discover {title}: A Book to Remember",
        f"Your Next {genre} Read: {title}",
        f"Explore the World of {title} by {author}",
        f"A New Reading Journey Begins with {title}",
        f"Is {title} Your Next Favourite Book?",
    ]

    social_posts = [
        f"Looking for your next read? Discover {title} by {author}! "
        f"A {genre.lower()} book for {audience}. #BookLovers #Reading",
        f"Your next reading adventure starts with {title}. "
        f"Find your next favourite book! #BookRecommendation",
        f"Readers, meet {title} by {author}. "
        f"Add this {genre.lower()} title to your reading list. #MustRead",
        f"Every book offers something new to discover. "
        f"Explore {title} and share your thoughts! #BookCommunity",
        f"Searching for a book to explore? Check out {title} "
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
    ]

    content = {
        "description": (
            "BOOK DESCRIPTION\n\n" + book_description
        ),
        "headlines": (
            "MARKETING HEADLINES\n\n"
            + "\n".join(
                f"{i}. {headline}"
                for i, headline in enumerate(headlines, 1)
            )
        ),
        "social": (
            "SOCIAL MEDIA POSTS\n\n"
            + "\n\n".join(
                f"{i}. {post}"
                for i, post in enumerate(social_posts, 1)
            )
        ),
        "keywords": (
            "MARKETING KEYWORDS\n\n" + ", ".join(keywords)
        ),
    }

    if copy_type == "all":
        return "\n\n".join(content[key] for key in content)

    return content[copy_type]