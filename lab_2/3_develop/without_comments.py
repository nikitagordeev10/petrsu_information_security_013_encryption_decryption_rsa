class Random:
    def __init__(self, seed=42):
        """
        Инициализация генератора случайных чисел.
        :param seed: Начальное значение для генерации случайных чисел.
        """
        self.seed = seed
        self.index = 0

    def getrandbits(self, k):
        """
        Генерация k случайных битов.
        :param k: Количество битов.
        :return: Случайное число с k битами.
        """
        if self.seed is None:
            raise ValueError("seed не установлено")
        self.index += 1
        return (self.seed + self.index) % (2 ** k)

    def _bit_length(self, n):
        """
        Вычисление количества битов в числе.
        :param n: Число.
        :return: Количество битов.
        """
        bits = 0
        while n:
            bits += 1
            n >>= 1
        return bits

    def randrange(self, start, stop=None, step=1):
        """
        Генерация случайного числа из диапазона.
        :param start: Начало диапазона.
        :param stop: Конец диапазона.
        :param step: Шаг.
        :return: Случайное число из диапазона.
        """
        if stop is None:
            start, stop = 0, start
        if step == 1:
            return start + self.getrandbits(self._bit_length(stop - start))
        else:
            return start + step * self.getrandbits(self._bit_length((stop - start) // step))

    def randint(self, a, b):
        """
        Генерация случайного целого числа из диапазона [a, b].
        :param a: Начало диапазона.
        :param b: Конец диапазона.
        :return: Случайное целое число.
        """
        return self.randrange(a, b + 1)

    def generate_large_number(self, length):
        """
        Генерация большого случайного числа длины length.
        :param length: Длина числа.
        :return: Случайное число.
        """
        return self.randrange(2 ** (length - 1), 2 ** length)

    def generate_prime(self, length):
        """
        Генерация случайного простого числа длины length.
        :param length: Длина числа.
        :return: Простое число.
        """
        while True:
            p = self.generate_large_number(length)
            if Math().is_prime(p):
                return p





