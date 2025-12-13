import unittest
from src.books import Book
from src.collection import BookCollection
from src.indexes import ISBNIndexDict, AuthorIndexDict, YearIndexDict
from src.library import Library


class TestBook(unittest.TestCase):
    """Тесты для класса Book"""

    def test_book_creation(self):
        """Тест создания книги, что все атрибуты записаны"""
        book = Book("Война и мир", "Лев Толстой", 1869, "Роман", "13022008")
        self.assertEqual(book.title, "Война и мир")
        self.assertEqual(book.author, "Лев Толстой")
        self.assertEqual(book.year, 1869)
        self.assertEqual(book.genre, "Роман")
        self.assertEqual(book.isbn, "13022008")

    def test_book_equality(self):
        """Тест равенства книг по ISBN"""
        book1 = Book("Война и мир", "Лев Толстой", 1869, "Роман", "13022008")
        book2 = Book("Другая книга", "Другой автор", 2000, "Фантастика", "13022008")
        book3 = Book("Третья книга", "Третий автор", 1900, "Драма", "01318102")

        self.assertEqual(book1, book2)  # Одинаковый ISBN
        self.assertNotEqual(book1, book3)  # Разные ISBN

    def test_book_hash(self):
        """Тест хэширования книги"""
        book1 = Book("Война и мир", "Лев Толстой", 1869, "Роман", "13022008")
        book2 = Book("Другая книга", "Другой автор", 2000, "Фантастика", "13022008")

        # Одинаковые ISBN дают одинаковый хеш-код
        self.assertEqual(hash(book1), hash(book2))


class TestBookCollection(unittest.TestCase):
    """Тесты для класса BookCollection."""

    def test_creation_empty(self):
        """Тест создания пустой коллекции."""
        collection = BookCollection()
        self.assertEqual(len(collection), 0)

    def test_creation_with_initial_books(self):
        """Тест создания коллекции с начальными книгами."""
        book1 = Book("Книга 1", "Автор 1", 2000, "Жанр", "1")
        book2 = Book("Книга 2", "Автор 2", 2001, "Жанр", "2")
        collection = BookCollection([book1, book2])

        self.assertEqual(len(collection), 2)
        self.assertEqual(collection[0], book1)
        self.assertEqual(collection[1], book2)

    def test_append(self):
        """Тест добавления книги."""
        collection = BookCollection()
        book = Book("Новая книга", "Новый автор", 2023, "Роман", "123")

        collection.append(book)

        self.assertEqual(len(collection), 1)
        self.assertEqual(collection[0], book)

    def test_remove(self):
        """Тест удаления книги."""
        book1 = Book("Книга 1", "Автор 1", 2000, "Жанр", "1")
        book2 = Book("Книга 2", "Автор 2", 2001, "Жанр", "2")
        collection = BookCollection([book1, book2])

        collection.remove(book1)

        self.assertEqual(len(collection), 1)
        self.assertEqual(collection[0], book2)

    def test_getitem_by_index(self):
        """Тест получения книги по индексу."""
        book1 = Book("Книга 1", "Автор 1", 2000, "Жанр", "1")
        book2 = Book("Книга 2", "Автор 2", 2001, "Жанр", "2")
        collection = BookCollection([book1, book2])

        self.assertEqual(collection[0], book1)
        self.assertEqual(collection[1], book2)

    def test_getitem_by_slice(self):
        """Тест получения среза."""
        book1 = Book("Книга 1", "Автор 1", 2000, "Жанр", "1")
        book2 = Book("Книга 2", "Автор 2", 2001, "Жанр", "2")
        book3 = Book("Книга 3", "Автор 3", 2002, "Жанр", "3")
        collection = BookCollection([book1, book2, book3])

        sliced_collection = collection[0:2]

        self.assertEqual(len(sliced_collection), 2)
        self.assertEqual(sliced_collection[0], book1)
        self.assertEqual(sliced_collection[1], book2)

    def test_contains(self):
        """Тест проверки нахождения книги в коллекции."""
        book1 = Book("Книга 1", "Автор 1", 2000, "Жанр", "1")
        book2 = Book("Книга 2", "Автор 2", 2001, "Жанр", "2")
        collection = BookCollection([book1])

        self.assertTrue(book1 in collection)
        self.assertFalse(book2 in collection)


class TestISBNIndexDict(unittest.TestCase):
    """Тесты для класса ISBNIndexDict."""

    def test_add_book(self):
        """Тест добавления книги по ISBN."""
        index = ISBNIndexDict()
        book = Book("Война и мир", "Лев Толстой", 1869, "Роман", "123")

        index.add_book(book)

        found_collection = index["123"]
        self.assertEqual(len(found_collection), 1)
        self.assertEqual(found_collection[0], book)

    def test_add_duplicate_book(self):
        """Тест добавления книги с уже существующим ISBN."""
        index = ISBNIndexDict()
        book1 = Book("Война и мир", "Лев Толстой", 1869, "Роман", "123")
        book2 = Book("Другая книга", "Другой автор", 2000, "Фантастика", "123")  # Тот же ISBN

        index.add_book(book1)
        # В реальной реализации это может вывести сообщение, но не заменит книгу
        # В зависимости от вашей реализации

        found_collection = index["123"]
        self.assertEqual(len(found_collection), 1)
        self.assertEqual(found_collection[0], book1)

    def test_remove_book(self):
        """Тест удаления книги по ISBN."""
        index = ISBNIndexDict()
        book = Book("Война и мир", "Лев Толстой", 1869, "Роман", "123")

        index.add_book(book)
        index.remove_book("123")

        with self.assertRaises(KeyError):
            index["123"]

    def test_get_nonexistent_book(self):
        """Тест получения несуществующей книги."""
        index = ISBNIndexDict()

        result = index.get("nonexistent")
        self.assertEqual(len(result), 0)


class TestAuthorIndexDict(unittest.TestCase):
    """Тесты для класса AuthorIndDict."""

    def test_add_book(self):
        """Тест добавления книги по автору."""
        index = AuthorIndexDict()
        book = Book("Война и мир", "Лев Толстой", 1869, "Роман", "123")

        index.add_book(book)

        found_collection = index.get_all_books_author("Лев Толстой")
        self.assertEqual(len(found_collection), 1)
        self.assertEqual(found_collection[0], book)

    def test_add_multiple_books_same_author(self):
        """Тест добавления нескольких книг одного автора."""
        index = AuthorIndexDict()
        book1 = Book("Война и мир", "Лев Толстой", 1869, "Роман", "1")
        book2 = Book("Анна Каренина", "Лев Толстой", 1877, "Роман", "2")

        index.add_book(book1)
        index.add_book(book2)

        found_collection = index.get_all_books_author("Лев Толстой")
        self.assertEqual(len(found_collection), 2)
        self.assertIn(book1, found_collection)
        self.assertIn(book2, found_collection)

    def test_remove_book(self):
        """Тест удаления книги по автору."""
        index = AuthorIndexDict()
        book = Book("Война и мир", "Лев Толстой", 1869, "Роман", "123")

        index.add_book(book)
        index.remove_book(book)

        found_collection = index.get_all_books_author("Лев Толстой")
        self.assertEqual(len(found_collection), 0)

    def test_remove_author_if_empty(self):
        """Тест удаления автора, если у него не осталось книг."""
        index = AuthorIndexDict()
        book = Book("Война и мир", "Лев Толстой", 1869, "Роман", "123")

        index.add_book(book)
        index.remove_book(book)

        self.assertNotIn("Лев Толстой", index.index)


class TestYearIndDict(unittest.TestCase):
    """Тесты для класса YearIndDict."""

    def test_add_book(self):
        """Тест добавления книги по году."""
        index = YearIndexDict()
        book = Book("Война и мир", "Лев Толстой", 1869, "Роман", "123")

        index.add_book(book)

        found_collection = index.get_all_books_year(1869)
        self.assertEqual(len(found_collection), 1)
        self.assertEqual(found_collection[0], book)

    def test_add_multiple_books_same_year(self):
        """Тест добавления нескольких книг одного года."""
        index = YearIndexDict()
        book1 = Book("Книга 1", "Автор 1", 2000, "Роман", "1")
        book2 = Book("Книга 2", "Автор 2", 2000, "Фантастика", "2")

        index.add_book(book1)
        index.add_book(book2)

        found_collection = index.get_all_books_year(2000)
        self.assertEqual(len(found_collection), 2)
        self.assertIn(book1, found_collection)
        self.assertIn(book2, found_collection)

    def test_remove_book(self):
        """Тест удаления книги по году."""
        index = YearIndexDict()
        book = Book("Война и мир", "Лев Толстой", 1869, "Роман", "123")

        index.add_book(book)
        index.remove_book(book)

        found_collection = index.get_all_books_year(1869)
        self.assertEqual(len(found_collection), 0)

    def test_remove_year_if_empty(self):
        """Тест удаления года, если в нем не осталось книг."""
        index = YearIndexDict()
        book = Book("Война и мир", "Лев Толстой", 1869, "Роман", "123")

        index.add_book(book)
        index.remove_book(book)

        self.assertNotIn(1869, index.index)


class TestLibrary(unittest.TestCase):
    """Тесты для класса Library."""

    def test_add_book(self):
        """Тест добавления книги в библиотеку."""
        library = Library()
        book = Book("Война и мир", "Лев Толстой", 1869, "Роман", "123")

        library.add_book(book)

        self.assertEqual(len(library.get_all_books()), 1)
        self.assertEqual(len(library.find_books_by_isbn("123")), 1)
        self.assertEqual(len(library.find_books_by_author("Лев Толстой")), 1)
        self.assertEqual(len(library.find_books_by_year(1869)), 1)

    def test_remove_book(self):
        """Тест удаления книги из библиотеки."""
        library = Library()
        book = Book("Война и мир", "Лев Толстой", 1869, "Роман", "123")

        library.add_book(book)
        success = library.remove_book(book)

        self.assertTrue(success)
        self.assertEqual(len(library.get_all_books()), 0)
        self.assertEqual(len(library.find_books_by_isbn("123")), 0)
        self.assertEqual(len(library.find_books_by_author("Лев Толстой")), 0)
        self.assertEqual(len(library.find_books_by_year(1869)), 0)

    def test_find_books_by_isbn(self):
        """Тест поиска книг по ISBN."""
        library = Library()
        book = Book("Война и мир", "Лев Толстой", 1869, "Роман", "123")

        library.add_book(book)
        found_books = library.find_books_by_isbn("123")

        self.assertEqual(len(found_books), 1)
        self.assertEqual(found_books[0], book)

    def test_find_books_by_author(self):
        """Тест поиска книг по автору."""
        library = Library()
        book1 = Book("Война и мир", "Лев Толстой", 1869, "Роман", "1")
        book2 = Book("Анна Каренина", "Лев Толстой", 1877, "Роман", "2")

        library.add_book(book1)
        library.add_book(book2)
        found_books = library.find_books_by_author("Лев Толстой")

        self.assertEqual(len(found_books), 2)
        self.assertIn(book1, found_books)
        self.assertIn(book2, found_books)

    def test_find_books_by_year(self):
        """Тест поиска книг по году."""
        library = Library()
        book1 = Book("Книга 1", "Автор 1", 2000, "Роман", "1")
        book2 = Book("Книга 2", "Автор 2", 2000, "Фантастика", "2")

        library.add_book(book1)
        library.add_book(book2)
        found_books = library.find_books_by_year(2000)

        self.assertEqual(len(found_books), 2)
        self.assertIn(book1, found_books)
        self.assertIn(book2, found_books)

    def test_find_books_by_genre(self):
        """Тест поиска книг по жанру."""
        library = Library()
        book1 = Book("Война и мир", "Лев Толстой", 1869, "Роман", "1")
        book2 = Book("Преступление и наказание", "Достоевский", 1866, "Роман", "2")
        book3 = Book("1984", "Оруэлл", 1949, "Антиутопия", "3")

        library.add_book(book1)
        library.add_book(book2)
        library.add_book(book3)
        found_books = library.find_books_by_genre("Роман")

        self.assertEqual(len(found_books), 2)
        self.assertIn(book1, found_books)
        self.assertIn(book2, found_books)
        self.assertNotIn(book3, found_books)

    def test_get_statistics(self):
        """Тест получения статистики."""
        library = Library()
        book1 = Book("Война и мир", "Лев Толстой", 1869, "Роман", "1")
        book2 = Book("Преступление и наказание", "Достоевский", 1866, "Роман", "2")

        library.add_book(book1)
        library.add_book(book2)

        stats = library.get_statistics()

        self.assertEqual(stats['total_books'], 2)
        self.assertEqual(stats['unique_authors'], 2)
        self.assertIn(1869, stats['years_range'])
        self.assertIn(1866, stats['years_range'])


if __name__ == '__main__':
    unittest.main()