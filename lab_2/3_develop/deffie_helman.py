class Random:
    def __init__(self, seed=None):
        self.seed = seed
        self.index = 0

    def set_seed(self, seed):
        self.seed = seed

    def getrandbits(self, k):
        if self.seed is None:
            raise ValueError("Seed is not set")
        self.index += 1
        return (self.seed + self.index) % (2 ** k)

    def randrange(self, start, stop=None, step=1):
        if stop is None:
            start, stop = 0, start
        if step == 1:
            return start + self.getrandbits(self._bit_length(stop - start))
        else:
            return start + step * self.getrandbits(self._bit_length((stop - start) // step))

    def randint(self, a, b):
        return self.randrange(a, b + 1)

    def _bit_length(self, n):
        bits = 0
        while n:
            bits += 1
            n >>= 1
        return bits

    def generate_large_number(self, length):
        return self.randint(2 ** (length - 1), 2 ** length)


class Math:
    def __init__(self):
        pass

    def pow(self, x, y, z=None):
        if z is None:
            return x ** y
        result = 1
        while y:
            if y & 1:
                result = result * x % z
            x = x * x % z
            y >>= 1
        return result


class DiffieHellman:
    def __init__(self, key_length=512):
        self.key_length = key_length
        self.random = Random(seed=42)  # Установка начального значения для генератора случайных чисел
        self.math = Math()

    def is_prime(self, n, k=5):
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0:
            return False

        def miller_rabin(n, d):
            a = self.random.randint(2, n - 2)
            while self.gcd(a, n) != 1:
                a = self.random.randint(2, n - 2)
            x = self.math.pow(a, d, n)
            if x == 1 or x == n - 1:
                return True
            while d != n - 1:
                x = self.math.pow(x, 2, n)
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

    def generate_prime(self, length):
        while True:
            p = self.random.generate_large_number(length)
            if self.is_prime(p):
                return p

    def gcd(self, a, b):
        while b != 0:
            a, b = b, a % b
        return a

    def generate_keys(self, g, p):
        private_key = self.random.generate_large_number(self.key_length)
        public_key = self.math.pow(g, private_key, p)
        return private_key, public_key

    def generate_shared_secret(self, other_public_key, private_key, p):
        return self.math.pow(other_public_key, private_key, p)


if __name__ == '__main__':
    diffie_hellman = DiffieHellman()

    # Генерация простого числа p и примитивного корня g
    p = diffie_hellman.generate_prime(512)
    g = diffie_hellman.random.randint(2, p - 2)

    print("Открытые параметры:")
    print("p =", p)
    print("g =", g)

    print("\nAlice генерирует свой приватный и публичный ключи:")
    alice_private_key, alice_public_key = diffie_hellman.generate_keys(g, p)
    print("Приватный ключ Алисы:", alice_private_key)
    print("Публичный ключ Алисы:", alice_public_key)

    print("\nBob генерирует свой приватный и публичный ключи:")
    bob_private_key, bob_public_key = diffie_hellman.generate_keys(g, p)
    print("Приватный ключ Боба:", bob_private_key)
    print("Публичный ключ Боба:", bob_public_key)

    print("\nОбмен и расчет общего секретного ключа:")
    alice_shared_secret = diffie_hellman.generate_shared_secret(bob_public_key, alice_private_key, p)
    bob_shared_secret = diffie_hellman.generate_shared_secret(alice_public_key, bob_private_key, p)

    print("Общий секретный ключ у Алисы:", alice_shared_secret)
    print("Общий секретный ключ у Боба:", bob_shared_secret)