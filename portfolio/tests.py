import unittest
from django.test import TestCase
from .models import League, Portfolio, Transaction
from datetime import date

if __name__ == "__main__":
    unittest.main()


class TransactionTest(TestCase):

    def setUp(self):
        self.league_data = {
            "author": 1,
            "name": "Test League",
            "description": "Test description to Test League",
            "start_value": 1000,
        }
        self.portfolio_data = {"name": "Test Portfolio"}

    def test_book_save(self):
        # Test saving a Book object to the database
        book = Book(**self.book_data)
        book.save()  # Saving the book to the test database

        # Check if the book is saved correctly
        saved_book = Book.objects.get(id=book.id)
        self.assertEqual(saved_book.title, self.book_data["title"])
        self.assertEqual(saved_book.author, self.book_data["author"])
        self.assertEqual(saved_book.published_date, self.book_data["published_date"])

    def test_book_count(self):
        # Check how many books exist before and after saving
        book_count_before = Book.objects.count()
        book = Book(**self.book_data)
        book.save()
        book_count_after = Book.objects.count()

        self.assertEqual(book_count_after, book_count_before + 1)
