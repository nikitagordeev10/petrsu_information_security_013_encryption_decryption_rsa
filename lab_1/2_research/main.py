from decimal import Decimal, getcontext

# Установим точность для вычислений
getcontext().prec = 100

# Отправитель замка, владелец ключа
p1 = 53  # простое число 1
p2 = 59  # простое число 2
n = p1 * p2  # длинное, больше 300 цифр 3127
F_n = (p1 - 1) * (p2 - 1)  # разложение Эйлера 3016
print("Простые числа уже установлены.")
print("Введите показатель степени (нечетное число не имеющее делителей с F_n):")
while True:
    e = int(input())
    if F_n % e != 0:
        break

# Нахождение модульного обратного числа d по модулю F_n
def mod_inv(a, m):
    m0, x0, x1 = m, Decimal(0), Decimal(1)
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

d = mod_inv(Decimal(e), Decimal(F_n))

# отправляем два числа - открытый замок
print("Открытый ключ (n, e):", n, e)

# получатель замка
message = 89

# Зашифрованное сообщение
c = Decimal(message) ** Decimal(e) % Decimal(n)
print("Зашифрованное сообщение:", c)

# Отправитель замка - расшифрованное сообщение
x = Decimal(c) ** Decimal(d) % Decimal(n)
print("Расшифрованное сообщение:", x)
