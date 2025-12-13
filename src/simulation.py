import random
from src.library import Library
from src.books import Book
from src.logger import setup_logging

logger = setup_logging()

def random_book() -> Book:
    """Создает рандомную книгу"""

    titles = [
        "Гарри Поттер и философский камень",
        "1984", "Лолита", "Остров сокровищ", "Маленький принц",
        "Портрет Дориана Грея", "Властелин колец", "Коллекционер"
    ]

    authors = [
        "Лев Николаевич Толстой", "Фёдор Михайлович Достоевский",
        "Михаил Афанасьевич Булгаков", "Александр Сергеевич Пушкин",
        "Уильям Шекспир", "Джордж Оруэлл", "Рэй Брэдбери", "Джейн Остин"
    ]

    genres = [
        "Роман", "Драма", "Фэнтези", "Научпоп", "Нон-фикшн",
        "Детектив", "Поэзия", "Классика", "Трагедия"
    ]

    title = random.choice(titles)
    author = random.choice(authors)
    year = random.randint(1600, 2025)
    genre = random.choice(genres)
    isbn = f"{random.randint(1000000000, 9999999999)}"

    return Book(title=title, author=author, year=year, genre=genre, isbn=isbn)


def run_simulation(steps: int = 20, seed: int | None = None) -> None:
    """
    Симуляция библиотеки
    :param steps: сколько щагов будет выполнено
    :param seed: инициализации генератора псевдослучайных чисел
    :return: None
    """
    if seed is not None:
        random.seed(seed)

    library = Library()

    logger.info(f"Начало симуляции библиотеки ( будет выполнено {steps} шагов ) ")

    # Добавляем несколько начальных книг, чтобы было над чем производить действия
    start_books = [
        Book("Оно", "Стивен Кинг", 1986, "Ужасы", "978012345699"),
        Book("Сияние", "Стивен Кинг", 1977, "Роман", "978098765431"),
        Book("Метро 2033", "Дмитрий Глуховский", 2005, "Фантастика", "9780543210987"),
        Book("Властелин колец: Братство кольца", "Дж.Р.Р. Толкин", 1954, "Фэнтези", "978012345702"),
        Book("Убить пересмешника", "Харпер Ли", 1960, "Роман", "978012345703"),
        Book("Ромео и Джульетта", "Уильям Шекспир", 1597, "Трагедия", "978012345713"),
        Book("Граф Монте-Кристо", "Александр Дюма", 1844, "Приключения", "978012345710"),
        Book("Отрочество", "Лев Николаевич Толстой", 1854, "Роман", "978012345707"),

    ]

    # Подготовка к началу симуляции, добавляем стартовые книги
    for book in start_books:
        library.add_book(book)
        logger.info(f"Шаг 0: Добавлена начальная книга: {book}")

    # Основной цикл симуляции
    for step in range(1, steps + 1):

        type_of_event = random.choice([
            "Добавить книгу",
            "Удалить книгу",
            "Найти книги по автору",
            "Найти книги по жанру",
            "Найти книги по году",
            "Найти книгу по isbn",
            "Попытка получить книгу, которой нет"
        ])

        logger.info(f"Шаг {step}: {type_of_event}")

        if type_of_event == "Добавить книгу":
            new_book = random_book()
            library.add_book(new_book)
            logger.info(f"       Добавлена книга: {new_book}")

        elif type_of_event == "Удалить книгу" and len(library.get_all_books()) > 0:
            books_list = list(library.get_all_books())
            book_to_remove = random.choice(books_list)
            success = library.remove_book(book_to_remove)
            if success:
                logger.info(f"       Удалена книга: {book_to_remove}")
            else:
                logger.info(f"       Не удалось удалить книгу: {book_to_remove}")

        elif type_of_event == "Найти книги по автору":
            # Получаем список всех авторов
            stata = library.get_statistics()
            if stata['unique_authors'] > 0:

                authors = list(library.indexes['автор'].keys())

                if authors:
                    search_author = random.choice(authors)
                    found_books = library.search_by_author(search_author)
                    logger.info(f"       Поиск книг автора '{search_author}': найдено {len(found_books)} книг")

                    for i, book in enumerate(found_books):
                        logger.info(f"       {i+1}. {book}")
            else:
                logger.info("       Нет доступных авторов для поиска")

        elif type_of_event == "Найти книги по жанру":
            genres = ["Роман", "Драма", "Фэнтези", "Научпоп", "Нон-фикшн",
        "Детектив", "Поэзия", "Классика", "Трагедия"]
            search_genre = random.choice(genres)
            found_books = library.search_by_genre(search_genre)
            logger.info(f"       Поиск книг жанра '{search_genre}': найдено {len(found_books)} книг")
            # Показываем только первые 2 книги
            for i, book in enumerate(found_books):
                logger.info(f"       {i+1}. {book}")


        elif type_of_event == "Найти книги по году":

            stata = library.get_statistics()
            if stata['years_range']:
                search_year = random.choice(stata['years_range'])
                found_books = library.search_by_year(search_year)
                logger.info(f"       Поиск книг за {search_year} год: найдено {len(found_books)} книг")

                for i, book in enumerate(found_books):
                    logger.info(f"       {i+1}. {book}")

            else:
                logger.info("       Нет годов для поиска")

        elif type_of_event == "Найти книгу по isbn":
            if len(library.get_all_books()) > 0:
                books_list = list(library.get_all_books())
                book_to_search = random.choice(books_list)
                found_books = library.search_by_isbn(book_to_search.isbn)
                logger.info(f"       Поиск книги по ISBN '{book_to_search.isbn}': найдено {len(found_books)} книг")
                for book in found_books:
                    logger.info(f"      {book}")
            else:
                logger.info("       Нет книг для поиска по ISBN")

        elif type_of_event == "Попытка получить книгу, которой нет":

            unreal_isbn = "1234567891011"
            found_books = library.search_by_isbn(unreal_isbn)
            logger.info(f"       Поиск книги с несуществующим ISBN '{unreal_isbn}': найдено {len(found_books)} книг")
            if len(found_books) == 0:
                logger.info(f"       Книга с таким isbn {unreal_isbn} не найдена ")

