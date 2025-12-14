from typing import Any, Dict, Iterator
import copy
from src.collection import BookCollection
from src.books import Book

class IndexDict:
    """Базовый класс для индексации"""

    def __init__(self) -> None:
        """
        Инициализирует словарь для индексации (ключом может ыть как строка, так и число, например год изднаия ил автор)
        """
        self.index: Dict[Any, BookCollection] = {}

    def __getitem__(self, key: Any) -> BookCollection:
        """
        Вызывает ошибку если ключа нет
        :param key: ключ для получения значения
        :return: Список, в котором элементы из класса Book
        """
        if key not in self.index:
            raise KeyError(f"Ключ '{key}' не найден")
        else:
            return copy.deepcopy(self.index[key])

    def __setitem__(self, key: Any, value: BookCollection) -> None:
        """
        Устанавливает значение по ключу
        :param key: ключ
        :param value: значение
        :return: None
        """
        self.index[key] = value

    def __len__(self) -> int:
        """
        :return: количество элементов словаря
        """
        return len(self.index)

    def __iter__(self) -> Iterator:
        """
        Итератор
        :return: Итератор, который выдает элементы в виде кортежей
        """
        return iter(self.index)

    def get(self, key: Any, default: BookCollection | None = None) -> BookCollection:
        """
        :param key: ключ
        :param default: значение по умолчанию если не найден ключ (как в словарях)
        :return: Копия значения по ключу (для безопасности и инкапсуляции) или значение по умолчанию
        """
        if default is None:
            default = BookCollection([])

        if key in self.index:
            return copy.deepcopy(self.index[key])

        else:
            return copy.deepcopy(default)

    def items(self):
        """
        return: Пары ключ-значение
        """
        res= []
        for key, value in self.index.items():
            res.append((key, copy.deepcopy(value)))
        return res

    def keys(self):
        return self.index.keys()



class ISBNIndexDict (IndexDict):
    """
    Словарная коллекция для индексации книг по ISBN
    """

    def __init__(self):
        """Инициализирует индекс по ISBN"""
        super().__init__()

    def add_book(self, book: 'Book') -> None:
        """
        Добавляет книги по ISBN
        :param book: книга которую нужно добавить
        :return: None
        """
        if book.isbn in self.index:
            print(f"Книга с ISBN {book.isbn} уже существует")
            return
        self.index[book.isbn] = BookCollection([book])

    def remove_book(self, isbn: str) -> None:
        """
        Удаляет книгу по ISBN
        :param isbn: значение ISBN
        :return: None
        """
        if isbn not in self.index:
            print(f"Книга с ISBN '{isbn}' не найдена")
            return

        del self.index[isbn]

    def __repr__(self) -> str:
        if not self.index:
            return "Нет книги с таким ISBN"

        res =''
        for isbn, collection in self.index.items():
            for book in collection:
                res += f"{book.isbn}: {book.title} ({book.genre}, {book.author}, {book.year})\n"
        return res

class AuthorIndexDict(IndexDict):
    """
    Словарная коллекция для индексации книг по автору
    """
    def __init__(self):
        """Инициализирует индекс по автору"""
        super().__init__()

    def add_book(self, book: 'Book') -> None:
        """
        Добавляет книгу по автору
        :param book: книга которую нужно добавить
        :return: None
        """
        if book.author not in self.index:
            self.index[book.author] = BookCollection()

        if book not in self.index[book.author]:
            self.index[book.author].append(book)

    def remove_book(self, book: 'Book') -> None:
        """
        Удаляет книгу по автору
        :param book: книга которую нужно удалить
        :return: None
        """
        if book.author in self.index:
            if book in self.index[book.author]:
                self.index[book.author].remove(book)
                # Удаляем запись этого автора, если коллекция книг этого автора стала пустой
                if len(self.index[book.author]) == 0:
                    del self.index[book.author]
            else:
                print(f"Книга {book.title} не найдена в коллекции автора {book.author}")


    def get_all_books_author(self,author: str) -> BookCollection:
        """
        Получить все книги автора
        :param author: автор чьи книги хотим получить
        :return: коллекция книг этого автора (копия) / сообщение что нет книг с таким автором
        """
        if author in self.index:
            return copy.deepcopy(self.index[author])
        else:
            print(f" Книги автора {author} не найдены")
            return BookCollection([])

    def __repr__(self) ->  str :
        if not self.index:
            return "Нет книг с таким автором"

        res = ''
        for author, collection in self.index.items():
            res += f"Найдено {len(collection)} книг от автора {author}:\n\n"
            for book in collection:
                res += f"{book.isbn}: {book.title} ({book.genre}, {book.author}, {book.year})\n"
        return res


class YearIndexDict(IndexDict):
    """
    Словарная коллекция для индексации книг по году издания
    """

    def __init__(self):
        """Инициализирует индекс по году издания"""
        super().__init__()

    def add_book(self, book: 'Book') -> None:
        """
        Добавляет книгу по году издания
        :param book: книга которую нужно добавить
        :return: None
        """
        if book.year not in self.index:
            self.index[book.year] = BookCollection()

        if book not in self.index[book.year]:
            self.index[book.year].append(book)

    def remove_book(self, book: 'Book') -> None:
        """
        Удаляет книгу по оду издания
        :param book: книга которую нужно удалить
        :return: None
        """
        if book.year in self.index:
            if book in self.index[book.year]:
                self.index[book.year].remove(book)
                # Удаляем запись этого автора, если коллекция книг этого автора стала пустой
                if len(self.index[book.year]) == 0:
                    del self.index[book.year]
            else:
                print(f"Книга {book.title} не найдена в коллекции {book.year} года")


    def get_all_books_year(self, year: int) -> BookCollection:
        """
        Получить все книги этого года издания
        :param year: год издания книги которого мы хотим удалить
        :return: коллекция книг этого года / соо что нет книг с таким годом издания
        """
        if year in self.index:
            return copy.deepcopy(self.index[year])
        else:
            print(f" Книги {year} года издания не найдены")
            return BookCollection([])

    def __repr__(self) -> str:
        if not self.index:
            return "Нет книг с таким годом издания"

        res = ''
        for year, collection in self.index.items():
            res += f"Найдено {len(collection)} книг {year} года издания:\n\n"
            for book in collection:
                res += f"{book.isbn}: {book.title} ({book.genre}, {book.author}, {book.year})\n\n"
        return res
