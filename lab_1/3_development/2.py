import random

# Функция для проверки простоты числа
def is_prime(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Выполняем тест Миллера-Рабина k раз
    for _ in range(k):
        a = random.randint(2, n - 2)
        if pow(a, n - 1, n) != 1:
            return False
    return True

# Функция для генерации простого числа заданной длины
def generate_prime(length):
    while True:
        p = random.getrandbits(length)
        if is_prime(p):
            return p

# Функция для нахождения НОД
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Функция для нахождения обратного по модулю
def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

# Функция для генерации ключей
def generate_keys(e):
    # Генерация двух простых чисел p и q
    p = generate_prime(512)
    q = generate_prime(512)

    # Вычисление модуля n и функции Эйлера от n
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Проверка взаимной простоты e и phi_n
    while gcd(e, phi_n) != 1:
        e = random.randrange(2, phi_n)
    d = mod_inverse(e, phi_n)

    return ((n, e), (n, d))

# Функция для шифрования данных
def encrypt(data, public_key):
    n, e = public_key
    return pow(data, e, n)

# Функция для расшифрования данных
def decrypt(encrypted_data, private_key):
    n, d = private_key
    return pow(encrypted_data, d, n)

# Пример использования

# Ввод открытого ключа
print("Введите показатель степени e (открытый ключ):")
e = int(input())

# Генерация ключей
public_key, private_key = generate_keys(e)
print("Открытый ключ:", public_key)
print("Закрытый ключ:", private_key)

# Шифрование данных
data = int(input("Введите данные для шифрования: "))
encrypted_data = encrypt(data, public_key)
print("Зашифрованные данные:", encrypted_data)

# Расшифрование данных
decrypted_data = decrypt(encrypted_data, private_key)
print("Расшифрованные данные:", decrypted_data)
