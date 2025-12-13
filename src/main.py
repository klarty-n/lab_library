from src.simulation import run_simulation


def main():
    """
    Точка входа для запуска программы
    """
    print("Начинаем симуляцию библиотеки (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ ")

    while True:
        try:
            steps = int(input("Введите количество шагов симуляции: "))
            if steps < 0:
                print("Количество шагов не может быть отрицательным, введите корректное число")
                continue
            break
        except ValueError:
            print("Введено некорректное число")

    while True:
        seed_user = input("Введите seed для генератора случайных чисел: ")
        try:
            seed = int(seed_user)
            break
        except ValueError:
            print("Введите корректное число для seed")

    run_simulation(steps=steps, seed=seed)

if __name__ == "__main__":
    main()