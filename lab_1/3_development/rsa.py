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
        return self.randint(2**(length-1), 2**length)


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


class RSA:
    def __init__(self, key_length=512):
        self.key_length = key_length
        self.random = Random(seed=42) # Установка начального значения для генератора случайных чисел
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

    def mod_inverse(self, a, m):
        m0, x0, x1 = m, 0, 1
        while a > 1:
            q = a // m
            m, a = a % m, m
            x0, x1 = x1 - q * x0, x0
        return x1 + m0 if x1 < 0 else x1

    def generate_keys(self, e):
        p = self.generate_prime(self.key_length)
        q = self.generate_prime(self.key_length)

        n = p * q
        phi_n = (p - 1) * (q - 1)

        while self.gcd(e, phi_n) != 1:
            e = self.random.randrange(2, phi_n)
        d = self.mod_inverse(e, phi_n)

        return ((n, e), (n, d))

    def encrypt(self, data, public_key):
        n, e = public_key
        if not isinstance(data, int):
            raise TypeError("Data must be an integer")
        if data <= 0:
            raise ValueError("Data must be a positive integer")
        return self.math.pow(data, e, n)

    def decrypt(self, encrypted_data, private_key):
        n, d = private_key
        return self.math.pow(encrypted_data, d, n)


if __name__ == '__main__':
    rsa = RSA()

    print("Введите показатель степени e (открытый ключ):")
    e = int(input())

    public_key, private_key = rsa.generate_keys(e)
    print("Открытый ключ:", public_key)
    print("Закрытый ключ:", private_key)

    data = int(input("Введите данные для шифрования: "))
    encrypted_data = rsa.encrypt(data, public_key)
    print("Зашифрованные данные:", encrypted_data)

    decrypted_data = rsa.decrypt(encrypted_data, private_key)
    print("Расшифрованные данные:", decrypted_data)
