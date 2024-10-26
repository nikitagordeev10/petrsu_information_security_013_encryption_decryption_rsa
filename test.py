import unittest
from rsa import RSA

class TestRSA(unittest.TestCase):

    def setUp(self):
        self.rsa = RSA()
        self.rsa = RSA()

    def test_is_prime(self):
        # Проверяем, что функция is_prime корректно определяет простые числа
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        for prime in primes:
            self.assertTrue(self.rsa.math.is_prime(prime))

    def test_generate_prime(self):
        # Проверяем, что generate_prime возвращает простое число
        prime = self.rsa.random.generate_prime(512)
        self.assertTrue(self.rsa.math.is_prime(prime))

    def test_gcd(self):
        # Проверяем, что функция gcd возвращает наибольший общий делитель
        self.assertEqual(self.rsa.math.gcd(10, 15), 5)
        self.assertEqual(self.rsa.math.gcd(14, 63), 7)
        self.assertEqual(self.rsa.math.gcd(24, 36), 12)

    def test_mod_inverse(self):
        # Проверяем, что функция mod_inverse возвращает модульное обратное число
        self.assertEqual(self.rsa.math.mod_inverse(3, 11), 4)
        self.assertEqual(self.rsa.math.mod_inverse(17, 3120), 2753)

    def test_generate_keys(self):
        # Проверяем, что generate_keys возвращает корректные ключи
        e = 65537
        public_key, private_key = self.rsa.generate_keys(e)
        self.assertEqual(len(public_key), 2)
        self.assertEqual(len(private_key), 2)
        self.assertEqual(public_key[1], e)

    def test_encrypt_decrypt_1(self):
        # Проверяем, что данные можно зашифровать и расшифровать
        e = 65537
        public_key, private_key = self.rsa.generate_keys(e)
        data = 123456789
        encrypted_data = self.rsa.encrypt(data, public_key)
        decrypted_data = self.rsa.decrypt(encrypted_data, private_key)
        self.assertEqual(decrypted_data, data)

    def test_encrypt_decrypt_2(self):
        # Проверяем, что данные можно зашифровать и расшифровать
        # 12 ^ 3 mod 55 = 23
        # 23 ^ 27 mod55 = 12
        e = 3
        public_key, private_key = self.rsa.generate_keys(e)
        data = 12
        encrypted_data = self.rsa.encrypt(data, public_key)
        decrypted_data = self.rsa.decrypt(encrypted_data, private_key)
        self.assertEqual(decrypted_data, data)

    def test_encrypt_decrypt_2(self):
        # Проверяем, что данные можно зашифровать и расшифровать
        # 12 ^ 3 mod 55 = 23
        # 23 ^ 27 mod55 = 12
        e = 5
        public_key, private_key = self.rsa.generate_keys(e)
        data = 24
        encrypted_data = self.rsa.encrypt(data, public_key)
        decrypted_data = self.rsa.decrypt(encrypted_data, private_key)
        self.assertEqual(decrypted_data, data)

    def test_encrypt_decrypt_3(self):
        # Проверяем, что данные можно зашифровать и расшифровать
        e = 5
        public_key, private_key = self.rsa.generate_keys(e)
        data = 31
        encrypted_data = self.rsa.encrypt(data, public_key)
        decrypted_data = self.rsa.decrypt(encrypted_data, private_key)
        self.assertEqual(decrypted_data, data)

    def test_encrypt_decrypt_2(self):
        # Проверяем, что данные можно зашифровать и расшифровать
        e = 3
        public_key, private_key = self.rsa.generate_keys(e)
        data = 12
        encrypted_data = self.rsa.encrypt(data, public_key)
        decrypted_data = self.rsa.decrypt(encrypted_data, private_key)
        self.assertEqual(decrypted_data, data)
    def test_encrypt_decrypt_2(self):
        # Проверяем, что данные можно зашифровать и расшифровать
        e = 3
        public_key, private_key = self.rsa.generate_keys(e)
        data = 12
        encrypted_data = self.rsa.encrypt(data, public_key)
        decrypted_data = self.rsa.decrypt(encrypted_data, private_key)
        self.assertEqual(decrypted_data, data)

    def test_encrypt_decrypt_large_data(self):
        # Проверяем, что большие данные можно зашифровать и расшифровать
        e = 65537
        public_key, private_key = self.rsa.generate_keys(e)
        data = 12345678901234567890
        encrypted_data = self.rsa.encrypt(data, public_key)
        decrypted_data = self.rsa.decrypt(encrypted_data, private_key)
        self.assertEqual(decrypted_data, data)

    def test_encrypt_decrypt_negative_data(self):
        # Проверяем, что отрицательные данные можно зашифровать и расшифровать
        e = 65537
        public_key, private_key = self.rsa.generate_keys(e)
        data = -123456789
        with self.assertRaises(ValueError):
            self.rsa.encrypt(data, public_key)

    def test_encrypt_decrypt_zero_data(self):
        # Проверяем, что данные равные нулю вызывают исключение ValueError
        e = 65537
        public_key, private_key = self.rsa.generate_keys(e)
        data = 0
        with self.assertRaises(ValueError):
            self.rsa.encrypt(data, public_key)

    def test_encrypt_decrypt_string_data(self):
        # Проверяем, что строки можно зашифровать и расшифровать
        e = 65537
        public_key, private_key = self.rsa.generate_keys(e)
        data = "Hello, RSA!"
        with self.assertRaises(TypeError):
            self.rsa.encrypt(data, public_key)

    def test_encrypt_decrypt_empty_data(self):
        # Проверяем, что пустые данные можно зашифровать и расшифровать
        e = 65537
        public_key, private_key = self.rsa.generate_keys(e)
        data = ""
        with self.assertRaises(TypeError):
            self.rsa.encrypt(data, public_key)



    def test_encrypt_decrypt_large_key(self):
        # Проверяем, что данные можно зашифровать и расшифровать с очень большим ключом
        e = 2**16 + 1
        public_key, private_key = self.rsa.generate_keys(e)
        data = 123456789
        encrypted_data = self.rsa.encrypt(data, public_key)
        decrypted_data = self.rsa.decrypt(encrypted_data, private_key)
        self.assertEqual(decrypted_data, data)

    def test_encrypt_decrypt_different_keys(self):
        # Проверяем, что данные, зашифрованные с одним ключом, расшифровываются с другим ключом
        e1 = 65537
        public_key1, private_key1 = self.rsa.generate_keys(e1)
        e2 = 3
        public_key2, private_key2 = self.rsa.generate_keys(e2)
        data = 123456789
        encrypted_data = self.rsa.encrypt(data, public_key1)
        decrypted_data = self.rsa.decrypt(encrypted_data, private_key2)
        self.assertNotEqual(decrypted_data, data)

    def test_encrypt_decrypt_large_key_with_large_data(self):
        # Проверяем, что очень большие данные можно зашифровать и расшифровать с очень большим ключом
        e = 2**16 + 1
        public_key, private_key = self.rsa.generate_keys(e)
        data = 2**1000
        encrypted_data = self.rsa.encrypt(data, public_key)
        decrypted_data = self.rsa.decrypt(encrypted_data, private_key)
        self.assertEqual(decrypted_data, data)

    def test_encrypt_decrypt_random_data(self):
        # Проверяем, что случайные данные можно зашифровать и расшифровать
        import random
        e = 65537
        public_key, private_key = self.rsa.generate_keys(e)
        data = random.randint(0, 2**512)
        encrypted_data = self.rsa.encrypt(data, public_key)
        decrypted_data = self.rsa.decrypt(encrypted_data, private_key)
        self.assertEqual(decrypted_data, data)

    def test_encrypt_decrypt_float_data(self):
        # Проверяем, что вещественные данные можно зашифровать и расшифровать
        e = 65537
        public_key, private_key = self.rsa.generate_keys(e)
        data = 1234.5678
        with self.assertRaises(TypeError):
            self.rsa.encrypt(data, public_key)
    def test_encrypt_decrypt_negative_float_data(self):
        # Проверяем, что отрицательные вещественные данные можно зашифровать и расшифровать
        e = 65537
        public_key, private_key = self.rsa.generate_keys(e)
        data = -1234.5678
        with self.assertRaises(TypeError):
            self.rsa.encrypt(data, public_key)

    def test_encrypt_decrypt_fraction_data(self):
        # Проверяем, что дробные данные можно зашифровать и расшифровать
        e = 65537
        public_key, private_key = self.rsa.generate_keys(e)
        data = 1/3
        with self.assertRaises(TypeError):
            self.rsa.encrypt(data, public_key)

if __name__ == '__main__':
    unittest.main()
