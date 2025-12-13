class Book:
    def __init__(self,title, author, year, genre, isbn):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.isbn = isbn

    def __repr__(self) -> str:
        return f"{self.title} ({self.genre}, {self.author}, {self.year}, {self.isbn})"

    def __eq__(self,other) -> bool:
        """
        Проверяем равенство по isbn
        :param other: с чем сравниваем
        :return: True если равны isbn, иначе False
        """
        if isinstance(other, Book):
            return self.isbn == other.isbn
        return False

    def __hash__(self) -> int:
        """
        Хеширует по значению isbn (нужно для использования в set)
        :return:
        """
        return hash(self.isbn)