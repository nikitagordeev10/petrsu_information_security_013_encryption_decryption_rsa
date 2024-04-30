import unittest
from diffie_hellman import Random, Math, DiffieHellman

class TestRandom(unittest.TestCase):
    def setUp(self):
        self.random = Random(seed=42)

    def test_getrandbits(self):
        self.assertEqual(self.random.getrandbits(5), 10)
        self.assertEqual(self.random.getrandbits(8), 170)
        self.assertEqual(self.random.getrandbits(10), 682)
        self.assertRaises(ValueError, self.random.getrandbits, 4)

    def test_randrange(self):
        self.assertEqual(self.random.randrange(5, 11), 7)
        self.assertEqual(self.random.randrange(5, 21, 5), 5)
        self.assertRaises(ValueError, self.random.randrange, 5)

    def test_randint(self):
        self.assertEqual(self.random.randint(5, 10), 7)
        self.assertEqual(self.random.randint(10, 10), 10)

    def test_generate_large_number(self):
        self.assertTrue(2 ** 511 <= self.random.generate_large_number(512) < 2 ** 512)
        self.assertTrue(2 ** 511 <= self.random.generate_large_number(1024) < 2 ** 1024)

    def test_generate_prime(self):
        self.assertTrue(Math().is_prime(self.random.generate_prime(512)))
        self.assertTrue(Math().is_prime(self.random.generate_prime(1024)))


class TestMath(unittest.TestCase):
    def setUp(self):
        self.math = Math()

    def test_pow(self):
        self.assertEqual(self.math.pow(2, 3, 5), 3)
        self.assertEqual(self.math.pow(2, 10, 11), 1)
        self.assertEqual(self.math.pow(3, 4), 81)
        self.assertEqual(self.math.pow(5, 3, 7), 6)

    def test_gcd(self):
        self.assertEqual(self.math.gcd(10, 25), 5)
        self.assertEqual(self.math.gcd(14, 28), 14)
        self.assertEqual(self.math.gcd(15, 17), 1)
        self.assertEqual(self.math.gcd(25, 100), 25)

    def test_is_prime(self):
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
        p, g = self.diffie_hellman.create_module_and_generator()
        self.assertTrue(Math().is_prime(p))
        self.assertTrue(2 < g < p)

    def test_generate_keys(self):
        p, g = self.diffie_hellman.create_module_and_generator()
        private_key, public_key = self.diffie_hellman.generate_keys(g, p)
        self.assertTrue(1 < private_key < p - 1)


    def test_generate_shared_secret(self):
        p, g = 23, 5  # example values for easier testing
        private_key_A, public_key_A = self.diffie_hellman.generate_keys(g, p)
        private_key_B, public_key_B = self.diffie_hellman.generate_keys(g, p)

        shared_secret_A = self.diffie_hellman.generate_shared_secret(public_key_B, private_key_A, p)
        shared_secret_B = self.diffie_hellman.generate_shared_secret(public_key_A, private_key_B, p)

        self.assertEqual(shared_secret_A, shared_secret_B)

if __name__ == '__main__':
    unittest.main()
