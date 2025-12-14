from typing import List, Iterator, Optional
from src.books import Book

class BookCollection:
    """Класс колекция книг"""
    def __init__(self, start_books: Optional[List] = None):
        """
        Инициализация коллекции
        :param start_books: начальный список книг в коллекции (если нет, то просто пустой список,
        но симуляции нужно с чем то работать, поэтому передавать начальный список мы будем)
        """
        self.books = start_books if start_books else []

    def __getitem__(self, key:  int | slice):
        """
        Получение элементов по срезу или индексу
        :param key: индекс или срез
        :return: одна книга (если по индексу) или коллекция книг
        """
        # Возвращаем книгу по индексу
        if not isinstance(key, slice):
            return self.books[key]

        # Возвращаем срез BookCollection
        else:
            sliced = self.books[key]
            return BookCollection(sliced)

    def __iter__(self) -> Iterator:
        """
        :return: итератор для коллекции
        """
        return iter(self.books)

    def __len__(self) -> int:
        """
        :return: количество книг в коллекции
        """
        return len(self.books)

    def append(self, book) -> None:
        """
        Добавляет книгу
        :param book: Книга которую нужно добавить (класса Book)
        :return: None
        """
        self.books.append(book)

    def remove(self, book) -> None:
        """
        Удаляет книгу
        :param book: Книга которую нужно удалить (класса Book)
        :return: None
        """
        self.books.remove(book)

    def __add__(self, other: 'BookCollection') -> 'BookCollection':
        """
        Объединяет две коллекции книг (дубликаты убираются)
        :param other: другая коллекция, с которой хотим объединить текущую
        :return: новая коллекция с книгами из обеих коллекций
        """
        #  __hash__ и __eq__ в Book реализовано, так что set работает правильно
        comb_books = list(set(self.books + other.books))
        return BookCollection(comb_books)

    def extend(self, books: List['Book']) -> None:
        """
        Для добавления в коллекцию списка книг
        :param books: список книг которые нужно добавить
        :return: None
        """
        self.books.extend(books)

    def __repr__(self) -> str:
        """Возвращает строковое представление коллекции"""
        return f"Книги из коллекции: {self.books}"
