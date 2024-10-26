class Random:
    def __init__(self, seed=None):
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
        return self.randint(2**(length-1), 2**length)

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


class Math:
    def __init__(self):
        self.random = Random(seed=42)

    def pow(self, x, y, z=None):
        """
        Возведение числа x в степень y по модулю z.
        :param x: Основание.
        :param y: Показатель степени.
        :param z: Модуль.
        :return: Результат возведения в степень по модулю.
        """
        if z is None:
            return x ** y
        result = 1
        while y:
            if y & 1:
                result = result * x % z
            x = x * x % z
            y >>= 1
        return result

    def gcd(self, a, b):
        """
        Нахождение наибольшего общего делителя чисел a и b.
        :param a: Первое число.
        :param b: Второе число.
        :return: НОД(a, b).
        """
        while b != 0:
            a, b = b, a % b
        return a

    def is_prime(self, n, k=5):
        """
        Проверка, является ли число простым.
        :param n: Число для проверки.
        :param k: Количество итераций теста Миллера-Рабина.
        :return: True, если число простое, иначе False.
        """
        if n <= 1:
            return False
        if n <= 3:
            return True
        def miller_rabin(n, d):
            a = self.random.randint(2, n - 2)
            while self.gcd(a, n) != 1:
                a = self.random.randint(2, n - 2)
            x = self.pow(a, d, n)
            if x == 1 or x == n - 1:
                return True
            while d != n - 1:
                x = self.pow(x, 2, n)
                d *= 2
                if x == 1:
                    return False
                if x == n - 1:
                    return True
            return False

        d = n - 1
        while d % 2 == 0:
            d //= 2

        for _ in range(k):
            if not miller_rabin(n, d):
                return False
        return True

    def mod_inverse(self, a, m):
        """
        Нахождение мультипликативно обратного числа a по модулю m.
        :param a: Число.
        :param m: Модуль.
        :return: Мультипликативно обратное к a по модулю m.
        """
        m0, x0, x1 = m, 0, 1
        while a > 1:
            q = a // m
            m, a = a % m, m
            x0, x1 = x1 - q * x0, x0
        return x1 + m0 if x1 < 0 else x1


class RSA:
    def __init__(self, key_length=512):
        """
        Инициализация объекта RSA.
        :param key_length: Длина ключа.
        """
        self.key_length = key_length
        self.random = Random(seed=42) # Установка начального значения для генератора случайных чисел
        self.math = Math()

    def generate_keys(self, e):
        """
        Генерация открытого и закрытого ключей.
        :param e: Показатель степени e.
        :return: Открытый и закрытый ключи.
        """

        # Выбираются два простых числа длины key_length
        p = self.random.generate_prime(self.key_length)
        q = self.random.generate_prime(self.key_length)

        # Вычисляется модуль, n = p * q
        n = p * q

        # Вычисляется значение функции Эйлера phi_n = (p - 1) * (q - 1)
        phi_n = (p - 1) * (q - 1)

        # Если phi_n не взаимно простое с e то выбирается новое phi_n
        while self.math.gcd(e, phi_n) != 1:
            p = self.random.generate_prime(self.key_length)
            q = self.random.generate_prime(self.key_length)
            n = p * q
            phi_n = (p - 1) * (q - 1)

        # Вычисляется число d, мультипликативно обратное к числу e
        d = self.math.mod_inverse(e, phi_n)

        print (p, q, n, phi_n, d)
        return ((n, e), (n, d))

    def encrypt(self, data, public_key):
        """
        Шифрование данных.
        :param data: Данные для шифрования.
        :param public_key: Открытый ключ.
        :return: Зашифрованные данные.
        """
        n, e = public_key
        if not isinstance(data, int):
            raise TypeError("Данные для шифрования должны быть целым числом")
        if data <= 0:
            raise ValueError("Данные для шифрования должны быть положительным целым числом")
        return self.math.pow(data, e, n)

    def decrypt(self, encrypted_data, private_key):
        """
        Расшифрование данных.
        :param encrypted_data: Зашифрованные данные.
        :param private_key: Закрытый ключ.
        :return: Расшифрованные данные.
        """
        n, d = private_key
        return self.math.pow(encrypted_data, d, n)


if __name__ == '__main__':
    rsa = RSA()

    e = int(input("Введите показатель степени e (открытый ключ): "))
    while not rsa.math.is_prime(e):
        print("e должно быть простым числом")
        e = int(input("Введите e: "))

    public_key, private_key = rsa.generate_keys(e)
    print("Открытый ключ P={n, e}:", public_key)

    data = int(input("Введите данные для шифрования, целое число: "))
    encrypted_data = rsa.encrypt(data, public_key)

    print("Зашифрованные данные:", encrypted_data)

    print("Закрытый ключ S={n, d}:", private_key)
    decrypted_data = rsa.decrypt(encrypted_data, private_key)

    print("Расшифрованные данные:", decrypted_data)
