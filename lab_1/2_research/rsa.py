import gmpy2
import random

def generate_p_q_n():
    # Генерация случайных простых чисел p и q
    p = generate_prime(512)
    q = generate_prime(512)
    # расчёт n
    n = p * q
    return p, q, n

def input_int_in_range(start, end):
    while True:
        try:
            n = int(input("Введите число: "))
        except ValueError:
            print("Вы ввели не число. Попробуйте снова.")
        else:
            if start <= n < end:
                return n
            print("Введённое число вне диапазона: [%d, %d)" % (start, end))

def generate_keypair(p, q, e):
    phi = (p - 1) * (q - 1)
    d = gmpy2.invert(e, phi)
    return ((e, n), (d, n))

def encrypt(public_key, plaintext):
    e, n = public_key
    cipher_text = gmpy2.powmod(plaintext, e, n)
    return cipher_text

def decrypt(private_key, ciphertext):
    d, n = private_key
    plain_text = gmpy2.powmod(ciphertext, d, n)
    return plain_text

def generate_prime(bits):
    while True:
        potential_prime = gmpy2.mpz_random(gmpy2.random_state(random.randint(0, 2**32-1)), bits)
        if gmpy2.is_prime(potential_prime):
            return potential_prime



if __name__ == "__main__":

    # Этап 1 - Выберите 2 простых числа, желательно больших, p и q
    p, q, n = generate_p_q_n()

    # Задание числа e
    # e = input_int_in_range()
    a = 8

    e = 65537  # Число Ферма
    # e = int(input("Введите число е"))
    # try:

    # Генерация ключей
    public_key, private_key = generate_keypair(p, q, e)

    # Пример шифрования и расшифрования
    plaintext = 42
    print("Исходный текст:", plaintext)

    ciphertext = encrypt(public_key, plaintext)
    print("Шифртекст:", ciphertext)

    decrypted_text = decrypt(private_key, ciphertext)
    print("Расшифрованный текст:", decrypted_text)
