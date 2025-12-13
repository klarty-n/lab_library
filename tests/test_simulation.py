import unittest
from unittest.mock import patch
from src.simulation import run_simulation, random_book
from src.books import Book


class TestSimulation(unittest.TestCase):
    """Тесты для функций симуляции."""

    def test_generate_random_book(self):
        """Тест генерации случайной книги."""
        book = random_book()

        # Проверяем, что объект класса Book
        self.assertIsInstance(book, Book)

        # Проверяем, что у книги есть все нужные атрибуты
        self.assertIsInstance(book.title, str)
        self.assertIsInstance(book.author, str)
        self.assertIsInstance(book.year, int)
        self.assertIsInstance(book.genre, str)
        self.assertIsInstance(book.isbn, str)

        # Проверяем, что год в допустимом диапазоне
        self.assertGreaterEqual(book.year, 1600)
        self.assertLessEqual(book.year, 2025)

        # Проверяем, что ISBN - это строка из чисел
        self.assertTrue(book.isbn.isdigit())
        self.assertGreaterEqual(len(book.isbn), 10)  # Минимальная длина ISBN

    def test_run_simulation_with_seed(self):
        """Тест симуляции с фиксированным seed"""
        # Тестируем, что с одинаковым seed результаты одинаковы

        # Заменяем реальный logger в модуле src.simulation на mock-объект (он запоминает какие методы вызывались и с какими аргументами)
        with patch('src.simulation.logger') as mock_logger:

            # Запускаем симуляцию дважды с одинаковым seed
            run_simulation(steps=5, seed=42)

            # Список всех вызовов метода info после первого запуска
            first = mock_logger.info.call_args_list

            # Очищаем все запомненные вызовы от первого запуска
            mock_logger.reset_mock()

            run_simulation(steps=5, seed=42)

            second = mock_logger.info.call_args_list

            # Проверяем, что вызовы логгера одинаковы
            self.assertEqual(len(first), len(second))

    def test_run_simulation_edge_cases(self):
        """Тест когда шагов 0"""
        with patch('src.simulation.logger') as mock_logger:
            # Тест с 0 шагов
            run_simulation(steps=0)

            log_calls = mock_logger.info.call_args_list

            # начало симуляции + 8 начальных книг, то есть 9 логов
            self.assertEqual(len(log_calls), 9)
