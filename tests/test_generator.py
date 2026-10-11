
import pytest

from src.generator import generate_marketing_copy


def test_generates_all_marketing_copy(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    result = generate_marketing_copy(
        title="The Hidden Garden",
        author="Ali Khan",
        genre="Fantasy",
        description="A magical adventure in a forgotten garden",
        audience="young adults",
    )

    assert "BOOK DESCRIPTION" in result
    assert "MARKETING HEADLINES" in result
    assert "SOCIAL MEDIA POSTS" in result
    assert "MARKETING KEYWORDS" in result


def test_generates_selected_content():
    result = generate_marketing_copy(
        title="The Hidden Garden",
        author="Ali Khan",
        genre="Fantasy",
        description="A magical adventure in a forgotten garden",
        audience="young adults",
        copy_type="headlines",
    )

    assert "MARKETING HEADLINES" in result
    assert "The Hidden Garden" in result


def test_missing_book_details():
    with pytest.raises(ValueError, match="All book details are required"):
        generate_marketing_copy(
            title="",
            author="Ali Khan",
            genre="Fantasy",
            description="A magical adventure",
            audience="young adults",
        )


def test_invalid_content_type():
    with pytest.raises(ValueError, match="Invalid marketing content type"):
        generate_marketing_copy(
            title="The Hidden Garden",
            author="Ali Khan",
            genre="Fantasy",
            description="A magical adventure",
            audience="young adults",
            copy_type="invalid",
        )