"""Utilities for loading and storing book records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _validate_book(book: dict[str, Any], *, index: int | None = None) -> dict[str, Any]:
    if not isinstance(book, dict):
        prefix = f"Book at index {index}" if index is not None else "Book"
        raise ValueError(f"{prefix} must be an object.")

    title = book.get("title")
    author = book.get("author")
    year = book.get("year")

    if not isinstance(title, str) or not title.strip():
        raise ValueError("Book title must be a non-empty string.")
    if not isinstance(author, str) or not author.strip():
        raise ValueError("Book author must be a non-empty string.")
    if not isinstance(year, int):
        raise ValueError("Book year must be an integer.")

    return {"title": title.strip(), "author": author.strip(), "year": year}


def load_books(path: str | Path) -> list[dict[str, Any]]:
    """Load books from a JSON file.

    Returns an empty list when the file does not exist.
    Raises ValueError for invalid JSON or invalid book structures.
    """

    file_path = Path(path)
    if not file_path.exists():
        return []

    try:
        content = file_path.read_text(encoding="utf-8")
        raw_data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in '{file_path}': {exc.msg}") from exc
    except OSError as exc:
        raise OSError(f"Unable to read books file '{file_path}': {exc.strerror}") from exc

    if not isinstance(raw_data, list):
        raise ValueError("Books data must be a list.")

    return [_validate_book(book, index=index) for index, book in enumerate(raw_data)]


def save_books(path: str | Path, books: list[dict[str, Any]]) -> None:
    """Validate and save books to a JSON file."""

    file_path = Path(path)
    validated_books = [_validate_book(book, index=index) for index, book in enumerate(books)]

    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(
            json.dumps(validated_books, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    except OSError as exc:
        raise OSError(f"Unable to write books file '{file_path}': {exc.strerror}") from exc


def add_book(path: str | Path, title: str, author: str, year: int) -> dict[str, Any]:
    """Add a new validated book record to the JSON file."""

    new_book = _validate_book({"title": title, "author": author, "year": year})
    books = load_books(path)
    books.append(new_book)
    save_books(path, books)
    return new_book
