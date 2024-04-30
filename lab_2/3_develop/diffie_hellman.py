class Random:
    def __init__(self, seed=42):
        self.a = 1664525
        self.c = 1013904223
        self.m = 2 ** 32
        self.seed = seed

    def getrandbits(self, k):
        if self.seed is None:
            raise ValueError("Seed is not set")
        if k > 32:
            raise ValueError("k cannot be greater than 32")
        # Update seed for the next call
        self.seed = (self.a * self.seed + self.c) % self.m
        # Return the last k bits of the current seed value
        return self.seed >> (32 - k)

    def _bit_length(self, n):
        bits = 0
        while n:
            bits += 1
            n >>= 1
        return bits

    def randrange(self, start, stop=None, step=1):
        if stop is None:
            start, stop = 0, start
        range_size = (stop - start + step - 1) // step
        if range_size <= 0:
            raise ValueError('range_size cannot be zero or negative')

        if range_size == 0:
            return start

        bits = self._bit_length(range_size)
        while True:
            rand_bits = self.getrandbits(bits)
            if rand_bits < range_size:
                break

        return start + rand_bits * step

    def randint(self, a, b):
        return self.randrange(a, b + 1)

    def generate_large_number(self, length):
        return self.randrange(2 ** (length - 1), 2 ** length)

    def generate_prime(self, length):
        while True:
            p = self.generate_large_number(min(length, 32))  # Limiting k to 32
            if Math().is_prime(p):
                return p


class Math:
    def __init__(self):
        self.random = Random()

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


class DiffieHellman:
    def __init__(self, key_length=512):
        """
        Инициализация объекта DiffieHellman с указанной длиной ключа.
        :param key_length: Длина ключа (по умолчанию 512 бит).
        """
        self.key_length = key_length
        self.random = Random(seed=42)  # Установка начального значения для генератора случайных чисел
        self.math = Math()

    def create_module_and_generator(self):
        """
        Генерация простого числа p и генератора g.
        :return: Кортеж (p, g).
        """
        p = self.random.generate_prime(512)
        g = self.random.randint(2, p - 2)

        return p, g

    def generate_keys(self, g, p):
        """
        Генерация закрытого ключа и соответствующего ему открытого ключа.
        :param g: Генератор.
        :param p: Простое число.
        :return: Кортеж (private_key, public_key).
        """
        private_key = self.random.randrange(2, p - 1)
        public_key = self.math.pow(g, private_key, p)
        return private_key, public_key


    def generate_shared_secret(self, other_public_key, private_key, p):
        """
        Генерация общего секрета на основе открытого ключа другой стороны и собственного закрытого ключа.
        :param other_public_key: Открытый ключ другой стороны.
        :param private_key: Закрытый ключ.
        :param p: Простое число.
        :return: Общий секрет.
        """
        return self.math.pow(other_public_key, private_key, p)


if __name__ == '__main__':
    diffie_hellman = DiffieHellman()

    # Генерация простого числа p и примитивного корня g
    p, g = diffie_hellman.create_module_and_generator()

    print("Открытый канал связи:")
    print("простой модуль p =", p)
    print("генератор g =", g)

    print("\nПервый пользователь: генерирует свой приватный и публичный ключи:")
    first_private_key, first_public_key = diffie_hellman.generate_keys(g, p)
    print("Приватный ключ:", first_private_key)
    print("Публичный ключ:", first_public_key)

    print("\nПервый пользователь: отправляет публичный ключ")

    print("\nВторой пользователь: генерирует свой приватный и публичный ключи:")
    second_private_key, second_public_key = diffie_hellman.generate_keys(g, p)
    print("Приватный ключ:", second_private_key)
    print("Публичный ключ:", second_public_key)

    print("\nВторой пользователь: отправляет публичный ключ")

    print("\nРасчет общего секретного ключа:")
    first_shared_secret = diffie_hellman.generate_shared_secret(second_public_key, first_private_key, p)
    second_shared_secret = diffie_hellman.generate_shared_secret(first_public_key, second_private_key, p)

    print("Общий секретный ключ у Первого пользователя:", first_shared_secret)
    print("Общий секретный ключ у Второго пользователя:", second_shared_secret)

