import errno
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOOKS_MODULE_DIR = PROJECT_ROOT / "samples" / "book-app-project"
sys.path.insert(0, str(BOOKS_MODULE_DIR))

import books  # noqa: E402


class BooksModuleTests(unittest.TestCase):
    def test_load_books_returns_empty_list_for_missing_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            missing = Path(tmpdir) / "missing.json"
            self.assertEqual(books.load_books(missing), [])

    def test_load_books_returns_validated_books_with_trimmed_strings(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            data_path = Path(tmpdir) / "books.json"
            data_path.write_text(
                json.dumps(
                    [
                        {"title": "  Dune  ", "author": "  Frank Herbert  ", "year": 1965},
                        {"title": "1984", "author": "George Orwell", "year": 1949},
                    ]
                ),
                encoding="utf-8",
            )

            result = books.load_books(data_path)

            self.assertEqual(
                result,
                [
                    {"title": "Dune", "author": "Frank Herbert", "year": 1965},
                    {"title": "1984", "author": "George Orwell", "year": 1949},
                ],
            )

    def test_load_books_raises_value_error_for_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            data_path = Path(tmpdir) / "books.json"
            data_path.write_text("{ not json", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, r"Invalid JSON in '.+books\.json'"):
                books.load_books(data_path)

    def test_load_books_raises_value_error_when_data_is_not_list(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            data_path = Path(tmpdir) / "books.json"
            data_path.write_text(json.dumps({"title": "Dune"}), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Books data must be a list."):
                books.load_books(data_path)

    def test_load_books_raises_value_error_for_invalid_book_types(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            data_path = Path(tmpdir) / "books.json"
            data_path.write_text(json.dumps(["not-a-book"]), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Book at index 0 must be an object."):
                books.load_books(data_path)

    def test_load_books_raises_value_error_for_invalid_book_fields(self):
        invalid_books = [
            ({"title": " ", "author": "Author", "year": 2000}, "Book title must be a non-empty string."),
            ({"title": "Title", "author": "", "year": 2000}, "Book author must be a non-empty string."),
            ({"title": "Title", "author": "Author", "year": "2000"}, "Book year must be an integer."),
        ]

        for payload, message in invalid_books:
            with self.subTest(payload=payload):
                with tempfile.TemporaryDirectory() as tmpdir:
                    data_path = Path(tmpdir) / "books.json"
                    data_path.write_text(json.dumps([payload]), encoding="utf-8")

                    with self.assertRaisesRegex(ValueError, message):
                        books.load_books(data_path)

    def test_load_books_wraps_oserror_from_read(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            data_path = Path(tmpdir) / "books.json"
            data_path.write_text("[]", encoding="utf-8")

            with mock.patch.object(
                Path,
                "read_text",
                side_effect=OSError(errno.EACCES, "Permission denied"),
            ):
                with self.assertRaisesRegex(
                    OSError, r"Unable to read books file '.+books\.json': Permission denied"
                ):
                    books.load_books(data_path)

    def test_save_books_writes_validated_json_and_creates_parent_directories(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            data_path = Path(tmpdir) / "nested" / "books.json"

            books.save_books(
                data_path,
                [{"title": "  Hyperion ", "author": " Dan Simmons  ", "year": 1989}],
            )

            self.assertTrue(data_path.exists())
            content = data_path.read_text(encoding="utf-8")
            self.assertTrue(content.endswith("\n"))
            self.assertEqual(
                json.loads(content),
                [{"title": "Hyperion", "author": "Dan Simmons", "year": 1989}],
            )

    def test_save_books_raises_value_error_for_invalid_book(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            data_path = Path(tmpdir) / "books.json"

            with self.assertRaisesRegex(ValueError, "Book at index 0 must be an object."):
                books.save_books(data_path, ["invalid"])

            self.assertFalse(data_path.exists())

    def test_save_books_wraps_oserror_from_write(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            data_path = Path(tmpdir) / "books.json"

            with mock.patch.object(
                Path,
                "write_text",
                side_effect=OSError(errno.ENOSPC, "No space left on device"),
            ):
                with self.assertRaisesRegex(
                    OSError, r"Unable to write books file '.+books\.json': No space left on device"
                ):
                    books.save_books(
                        data_path,
                        [{"title": "Title", "author": "Author", "year": 2000}],
                    )

    def test_add_book_appends_book_and_returns_new_record(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            data_path = Path(tmpdir) / "books.json"
            data_path.write_text(
                json.dumps([{"title": "Dune", "author": "Frank Herbert", "year": 1965}]),
                encoding="utf-8",
            )

            new_book = books.add_book(data_path, "  Neuromancer ", " William Gibson ", 1984)
            saved_books = json.loads(data_path.read_text(encoding="utf-8"))

            self.assertEqual(new_book, {"title": "Neuromancer", "author": "William Gibson", "year": 1984})
            self.assertEqual(
                saved_books,
                [
                    {"title": "Dune", "author": "Frank Herbert", "year": 1965},
                    {"title": "Neuromancer", "author": "William Gibson", "year": 1984},
                ],
            )


if __name__ == "__main__":
    unittest.main()
