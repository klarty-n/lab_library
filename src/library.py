from src.collection import BookCollection
from src.indexes import  ISBNIndexDict, AuthorIndexDict, YearIndexDict
from src.books import Book
from typing import Dict, Any


class Library:
    """
    Класс библиотеки, содержит коллекцию всех книг и коллекции индексов
    """
    def __init__(self):
        """Инициализирует библиотеку с пустыми коллекциями"""
        self.books = BookCollection()  # Коллекция всех книг
        self.indexes = {
            'isbn': ISBNIndexDict(),
            'автор': AuthorIndexDict(),
            'год издания': YearIndexDict()
        }

    def add_book(self, book: Book) -> None:
        """
        Обновляет книгу в библиотеку и обновляет индексы
        :param book: книга которую нужно добавить
        :return: None
        """
        # Добавляем книгу в общую коллекцию
        self.books.append(book)

        # Обновляем все индексы
        self.indexes['isbn'].add_book(book)
        self.indexes['автор'].add_book(book)
        self.indexes['год издания'].add_book(book)

    def remove_book(self, book: Book) -> bool:
        """
        Удаляет книгу изз библиотеки и обновляет все индексы
        :param book: книга, которую нужно удалить
        :return: True сли удалилась и False сли произошла ошибка
        """
        try:
            # Удаляем книгу из общей коллекции
            self.books.remove(book)

            # Обновляем все индексы
            self.indexes['isbn'].remove_book(book.isbn)
            self.indexes['автор'].remove_book(book)
            self.indexes['год издания'].remove_book(book)

            return True
        except ValueError:
            print(f"Книга '{book.title}' автора {book.author} не найдена в библиотеке")
            return False

    def search_by_isbn(self, isbn: str) -> BookCollection:
        """
        Поиск книг по isbn
        :param isbn: isbn книги
        :return: коллекция найденных книг
        """
        # получаем объект ISBNIndexDict и вызываем get у него, передав ему ISBN, получаем книгу с этим isbn
        return self.indexes['isbn'].get(isbn)

    def search_by_author(self, author: str) -> BookCollection:
        """
        Поиск книг по автору
        :param author: автор, чьи книги нужно найти
        :return: коллекция найденных книг
        """
        return self.indexes['автор'].get_all_books_author(author)

    def search_by_year(self, year: int) -> BookCollection:
        """
        Поиск по году издания
        :param year: год издания, книги которого нужно найти
        :return: коллекция найденных книг
        """
        return self.indexes['год издания'].get_all_books_year(year)

    def search_by_genre(self, genre: str) -> BookCollection:
        """
        Поиск по жанру
        :param genre: жанр, в котором нужно найти книги
        :return: коллекция найденных книг
        """
        res = []
        for book in self.books:
            if book.genre.lower() == genre.lower():
                res.append(book)
        return BookCollection(res)

    def get_all_books(self) -> BookCollection:
        """
        :return: Коллекции всех книг в библиотеке
        """
        return BookCollection([book for book in self.books])

    def get_statistics(self) -> Dict[str, Any]:
        """
        Статистика библиотеки
        :return: Словарь со статистикой
        """
        authors_count = len(self.indexes['автор'])

        return {
            'total_books': len(self.books),
            'unique_authors': authors_count,
            'years_range': sorted(list(self.indexes['год издания'].keys())) if self.indexes['год издания'] else [],
            'books_per_author': {author: len(books) for author, books in self.indexes['автор'].items()}
        }

    def __repr__(self) -> str:
        """Возвращает строковое представление библиотеки"""
        res = f"Всего книг в библиотеке {len(self.books)}\n\n"
        for i, book in enumerate(self.books):
            res += f"{i + 1}. {book.title} ({book.genre}, {book.author}, {book.year})\n"

        return res
