"""Unit tests for books.py utilities."""

from __future__ import annotations

import json

import pytest

from books import _validate_book, add_book, load_books, save_books


# ---------------------------------------------------------------------------
# _validate_book
# ---------------------------------------------------------------------------

class TestValidateBook:
    def test_valid_book_returns_cleaned_dict(self):
        result = _validate_book({"title": "  Dune  ", "author": " Frank Herbert ", "year": 1965})
        assert result == {"title": "Dune", "author": "Frank Herbert", "year": 1965}

    def test_non_dict_raises_value_error(self):
        with pytest.raises(ValueError, match="must be an object"):
            _validate_book("not a dict")

    def test_non_dict_with_index_includes_index_in_message(self):
        with pytest.raises(ValueError, match="Book at index 2"):
            _validate_book("bad", index=2)

    def test_missing_title_raises_value_error(self):
        with pytest.raises(ValueError, match="title"):
            _validate_book({"author": "A", "year": 2000})

    def test_blank_title_raises_value_error(self):
        with pytest.raises(ValueError, match="title"):
            _validate_book({"title": "   ", "author": "A", "year": 2000})

    def test_non_string_title_raises_value_error(self):
        with pytest.raises(ValueError, match="title"):
            _validate_book({"title": 123, "author": "A", "year": 2000})

    def test_missing_author_raises_value_error(self):
        with pytest.raises(ValueError, match="author"):
            _validate_book({"title": "T", "year": 2000})

    def test_blank_author_raises_value_error(self):
        with pytest.raises(ValueError, match="author"):
            _validate_book({"title": "T", "author": "", "year": 2000})

    def test_missing_year_raises_value_error(self):
        with pytest.raises(ValueError, match="year"):
            _validate_book({"title": "T", "author": "A"})

    def test_float_year_raises_value_error(self):
        with pytest.raises(ValueError, match="year"):
            _validate_book({"title": "T", "author": "A", "year": 2000.5})

    def test_string_year_raises_value_error(self):
        with pytest.raises(ValueError, match="year"):
            _validate_book({"title": "T", "author": "A", "year": "2000"})


# ---------------------------------------------------------------------------
# load_books
# ---------------------------------------------------------------------------

class TestLoadBooks:
    def test_returns_empty_list_when_file_missing(self, tmp_path):
        result = load_books(tmp_path / "nonexistent.json")
        assert result == []

    def test_loads_valid_books(self, tmp_path):
        data = [{"title": "1984", "author": "Orwell", "year": 1949}]
        p = tmp_path / "books.json"
        p.write_text(json.dumps(data), encoding="utf-8")
        result = load_books(p)
        assert result == [{"title": "1984", "author": "Orwell", "year": 1949}]

    def test_raises_on_invalid_json(self, tmp_path):
        p = tmp_path / "books.json"
        p.write_text("{not valid json", encoding="utf-8")
        with pytest.raises(ValueError, match="Invalid JSON"):
            load_books(p)

    def test_raises_when_root_is_not_list(self, tmp_path):
        p = tmp_path / "books.json"
        p.write_text(json.dumps({"title": "T", "author": "A", "year": 2000}), encoding="utf-8")
        with pytest.raises(ValueError, match="must be a list"):
            load_books(p)

    def test_raises_on_invalid_book_in_list(self, tmp_path):
        data = [{"title": "", "author": "A", "year": 2000}]
        p = tmp_path / "books.json"
        p.write_text(json.dumps(data), encoding="utf-8")
        with pytest.raises(ValueError):
            load_books(p)


# ---------------------------------------------------------------------------
# save_books
# ---------------------------------------------------------------------------

class TestSaveBooks:
    def test_saves_valid_books(self, tmp_path):
        books = [{"title": "Dune", "author": "Herbert", "year": 1965}]
        p = tmp_path / "books.json"
        save_books(p, books)
        loaded = json.loads(p.read_text(encoding="utf-8"))
        assert loaded == books

    def test_creates_parent_directories(self, tmp_path):
        p = tmp_path / "deep" / "nested" / "books.json"
        save_books(p, [{"title": "T", "author": "A", "year": 2000}])
        assert p.exists()

    def test_output_ends_with_newline(self, tmp_path):
        p = tmp_path / "books.json"
        save_books(p, [{"title": "T", "author": "A", "year": 2000}])
        assert p.read_text(encoding="utf-8").endswith("\n")

    def test_raises_on_invalid_book(self, tmp_path):
        p = tmp_path / "books.json"
        with pytest.raises(ValueError):
            save_books(p, [{"title": "", "author": "A", "year": 2000}])


# ---------------------------------------------------------------------------
# add_book
# ---------------------------------------------------------------------------

class TestAddBook:
    def test_adds_book_to_empty_file(self, tmp_path):
        p = tmp_path / "books.json"
        result = add_book(p, "Brave New World", "Huxley", 1932)
        assert result == {"title": "Brave New World", "author": "Huxley", "year": 1932}
        loaded = load_books(p)
        assert len(loaded) == 1
        assert loaded[0] == result

    def test_appends_to_existing_books(self, tmp_path):
        p = tmp_path / "books.json"
        add_book(p, "Book One", "Author A", 2000)
        add_book(p, "Book Two", "Author B", 2001)
        loaded = load_books(p)
        assert len(loaded) == 2
        assert loaded[1]["title"] == "Book Two"

    def test_strips_whitespace_from_inputs(self, tmp_path):
        p = tmp_path / "books.json"
        result = add_book(p, "  Neuromancer  ", "  Gibson  ", 1984)
        assert result["title"] == "Neuromancer"
        assert result["author"] == "Gibson"

    def test_raises_on_invalid_year(self, tmp_path):
        p = tmp_path / "books.json"
        with pytest.raises(ValueError):
            add_book(p, "Title", "Author", "not-an-int")  # type: ignore[arg-type]
