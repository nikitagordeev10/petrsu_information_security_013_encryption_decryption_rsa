import unittest
from diffie_hellman import Random, Math, DiffieHellman

class TestRandom(unittest.TestCase):

    def setUp(self):
        self.random = Random(seed=42)

    def test_generate_prime(self):
        # Убеждаемся, что числа, сгенерированные методом generate_prime, действительно простые.
        self.assertTrue(Math().is_prime(self.random.generate_prime(512)))
        self.assertTrue(Math().is_prime(self.random.generate_prime(1024)))

class TestMath(unittest.TestCase):
    """Тесты для класса Math."""

    def setUp(self):
        self.math = Math()

    def test_pow(self):
        # Проверяем возведение в степень по модулю.
        self.assertEqual(self.math.pow(2, 3, 5), 3)
        self.assertEqual(self.math.pow(2, 10, 11), 1)
        self.assertEqual(self.math.pow(3, 4), 81)
        self.assertEqual(self.math.pow(5, 3, 7), 6)

    def test_gcd(self):
        # Проверяем нахождение наибольшего общего делителя.
        self.assertEqual(self.math.gcd(10, 25), 5)
        self.assertEqual(self.math.gcd(14, 28), 14)
        self.assertEqual(self.math.gcd(15, 17), 1)
        self.assertEqual(self.math.gcd(25, 100), 25)

    def test_is_prime(self):
        # Проверяем, что числа правильно определяются как простые или составные.
        self.assertTrue(self.math.is_prime(7))
        self.assertTrue(self.math.is_prime(13))
        self.assertTrue(self.math.is_prime(23))
        self.assertFalse(self.math.is_prime(9))
        self.assertFalse(self.math.is_prime(15))
        self.assertFalse(self.math.is_prime(21))

class TestDiffieHellman(unittest.TestCase):
    def setUp(self):
        self.diffie_hellman = DiffieHellman()

    def test_create_module_and_generator(self):
        # Проверяем корректность генерации простого модуля и генератора.
        p, g = self.diffie_hellman.create_module_and_generator()
        self.assertTrue(Math().is_prime(p))
        self.assertTrue(2 < g < p)

    def test_generate_keys(self):
        # Проверяем генерацию закрытого и открытого ключей.
        p, g = self.diffie_hellman.create_module_and_generator()
        private_key, public_key = self.diffie_hellman.generate_keys(g, p)
        self.assertTrue(1 < private_key < p - 1)

    def test_generate_shared_secret(self):
        # Тест метода generate_shared_secret
        p, g = 23, 5
        private_key_A, public_key_A = self.diffie_hellman.generate_keys(g, p)
        private_key_B, public_key_B = self.diffie_hellman.generate_keys(g, p)

        shared_secret_A = self.diffie_hellman.generate_shared_secret(public_key_B, private_key_A, p)
        shared_secret_B = self.diffie_hellman.generate_shared_secret(public_key_A, private_key_B, p)

        self.assertEqual(shared_secret_A, shared_secret_B)

if __name__ == '__main__':
    unittest.main()
